from __future__ import print_function
import sys
from os import environ
from base64 import b64encode
import json
from datetime import datetime, timedelta
from itertools import chain

import requests
from urlobject import URLObject
import six
from six.moves.urllib.parse import urlencode
from nylas._client_sdk_version import __VERSION__
from nylas.client.errors import MessageRejectedError
from nylas.client.restful_model_collection import RestfulModelCollection
from nylas.client.restful_models import (
    Calendar,
    Contact,
    Event,
    RoomResource,
    Message,
    Thread,
    File,
    Account,
    APIAccount,
    SingletonAccount,
    Folder,
    Label,
    Draft,
)
from nylas.client.neural_api_models import Neural
from nylas.utils import timestamp_from_dt, create_request_body

DEBUG = environ.get("NYLAS_CLIENT_DEBUG")
API_SERVER = "https://api.nylas.com"
SUPPORTED_API_VERSION = "2.2"


def _validate(response):
    if DEBUG:  # pragma: no cover
        print(
            "{method} {url} ({body}) => {status}: {text}".format(
                method=response.request.method,
                url=response.request.url,
                body=response.request.body,
                status=response.status_code,
                text=response.text,
            )
        )

    if response.status_code == 402:
        # HTTP status code 402 normally means "Payment Required",
        # but when Nylas uses that status code, it means something different.
        # Usually it indicates an upstream error on the provider.
        # We let Requests handle most HTTP errors, but for this one,
        # we will handle it separate and handle a _different_ exception
        # so that users don't think they need to pay.
        raise MessageRejectedError(response)

    response.raise_for_status()
    return response


class APIClient(json.JSONEncoder):
    """API client for the Nylas API."""

    def __init__(
        self,
        client_id=environ.get("NYLAS_CLIENT_ID"),
        client_secret=environ.get("NYLAS_CLIENT_SECRET"),
        access_token=environ.get("NYLAS_ACCESS_TOKEN"),
        api_server=API_SERVER,
        api_version=SUPPORTED_API_VERSION,
    ):
        if not api_server.startswith("https://"):
            raise Exception(
                "When overriding the Nylas API server address, you"
                " must include https://"
            )
        self.api_server = api_server
        self.api_version = api_version
        self.authorize_url = api_server + "/oauth/authorize"
        self.access_token_url = api_server + "/oauth/token"
        self.revoke_url = api_server + "/oauth/revoke"
        self.revoke_all_url = (
            api_server + "/a/{client_id}/accounts/{account_id}/revoke-all"
        )
        self.ip_addresses_url = api_server + "/a/{client_id}/ip_addresses"
        self.token_info_url = (
            api_server + "/a/{client_id}/accounts/{account_id}/token-info"
        )

        self.client_secret = client_secret
        self.client_id = client_id

        self.session = requests.Session()
        self.version = __VERSION__
        major, minor, revision, _, __ = sys.version_info
        version_header = "Nylas Python SDK {} - {}.{}.{}".format(
            self.version, major, minor, revision
        )
        self.session.headers = {
            "X-Nylas-API-Wrapper": "python",
            "X-Nylas-Client-Id": self.client_id,
            "Nylas-API-Version": self.api_version,
            "User-Agent": version_header,
        }
        self._access_token = None
        self.access_token = access_token
        self.auth_token = None

        # Requests to the /a/ namespace don't use an auth token but
        # the client_secret. Set up a specific session for this.
        self.admin_session = requests.Session()

        if client_secret is not None:
            b64_client_secret = b64encode((client_secret + ":").encode("utf8"))
            authorization = "Basic {secret}".format(
                secret=b64_client_secret.decode("utf8")
            )
            self.admin_session.headers = {
                "Authorization": authorization,
                "X-Nylas-API-Wrapper": "python",
                "X-Nylas-Client-Id": self.client_id,
                "Nylas-API-Version": self.api_version,
                "User-Agent": version_header,
            }
        super(APIClient, self).__init__()

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value
        if value:
            authorization = "Bearer {token}".format(token=value)
            self.session.headers["Authorization"] = authorization
        else:
            if "Authorization" in self.session.headers:
                del self.session.headers["Authorization"]

    def authentication_url(
        self,
        redirect_uri,
        login_hint="",
        state="",
        scopes=("email", "calendar", "contacts"),
    ):
        args = {
            "redirect_uri": redirect_uri,
            "client_id": self.client_id or "None",  # 'None' for back-compat
            "response_type": "code",
            "login_hint": login_hint,
            "state": state,
        }

        if scopes:
            if isinstance(scopes, str):
                scopes = [scopes]
            args["scopes"] = ",".join(scopes)

        url = URLObject(self.authorize_url).add_query_params(args.items())
        return str(url)

    def token_for_code(self, code):
        args = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
        }

        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain",
        }

        resp = requests.post(
            self.access_token_url, data=urlencode(args), headers=headers
        ).json()

        self.access_token = resp[u"access_token"]
        return self.access_token

    def is_opensource_api(self):
        if self.client_id is None and self.client_secret is None:
            return True

        return False

    def revoke_token(self):
        resp = self.session.post(self.revoke_url)
        _validate(resp)
        self.auth_token = None
        self.access_token = None

    def revoke_all_tokens(self, keep_access_token=None):
        revoke_all_url = self.revoke_all_url.format(
            client_id=self.client_id, account_id=self.account.id
        )
        data = {}
        if keep_access_token is not None:
            data["keep_access_token"] = keep_access_token

        headers = {"Content-Type": "application/json"}
        headers.update(self.admin_session.headers)
        resp = self.admin_session.post(revoke_all_url, json=data, headers=headers)
        _validate(resp).json()
        if keep_access_token != self.access_token:
            self.auth_token = None
            self.access_token = None

    def ip_addresses(self):
        ip_addresses_url = self.ip_addresses_url.format(client_id=self.client_id)
        resp = self.admin_session.get(ip_addresses_url)
        _validate(resp).json()
        return resp.json()

    def token_info(self):
        token_info_url = self.token_info_url.format(
            client_id=self.client_id, account_id=self.account.id
        )
        self.admin_session.headers["Content-Type"] = "application/json"
        resp = self.admin_session.post(
            token_info_url, json={"access_token": self.access_token}
        )
        _validate(resp).json()
        return resp.json()

    def free_busy(self, emails, start_at, end_at):
        if isinstance(emails, six.string_types):
            emails = [emails]
        if isinstance(start_at, datetime):
            start_time = timestamp_from_dt(start_at)
        else:
            start_time = start_at
        if isinstance(end_at, datetime):
            end_time = timestamp_from_dt(end_at)
        else:
            end_time = end_at
        url = "{api_server}/calendars/free-busy".format(api_server=self.api_server)
        data = {
            "emails": emails,
            "start_time": start_time,
            "end_time": end_time,
        }
        resp = self.session.post(url, json=data)
        _validate(resp)
        return resp.json()

    def open_hours(self, emails, days, timezone, start, end):
        if isinstance(emails, six.string_types):
            emails = [emails]
        if isinstance(days, int):
            days = [days]
        if isinstance(start, datetime):
            start = "{hour}:{minute}".format(hour=start.hour, minute=start.minute)
        if isinstance(start, datetime):
            end = "{hour}:{minute}".format(hour=end.hour, minute=end.minute)
        return {
            "emails": emails,
            "days": days,
            "timezone": timezone,
            "start": start,
            "end": end,
            "object_type": "open_hours",
        }

    def availability(
        self,
        emails,
        duration,
        interval,
        start_at,
        end_at,
        buffer=None,
        round_robin=None,
        free_busy=None,
        open_hours=None,
    ):
        if isinstance(emails, six.string_types):
            emails = [emails]
        if isinstance(duration, timedelta):
            duration_minutes = int(duration.total_seconds() // 60)
        else:
            duration_minutes = int(duration)
        if isinstance(interval, timedelta):
            interval_minutes = int(interval.total_seconds() // 60)
        else:
            interval_minutes = int(interval)
        if isinstance(start_at, datetime):
            start_time = timestamp_from_dt(start_at)
        else:
            start_time = start_at
        if isinstance(end_at, datetime):
            end_time = timestamp_from_dt(end_at)
        else:
            end_time = end_at
        if open_hours is not None:
            self._validate_open_hours(emails, open_hours, free_busy)

        url = "{api_server}/calendars/availability".format(api_server=self.api_server)
        data = {
            "emails": emails,
            "duration_minutes": duration_minutes,
            "interval_minutes": interval_minutes,
            "start_time": start_time,
            "end_time": end_time,
            "buffer": buffer,
            "round_robin": round_robin,
            "free_busy": free_busy or [],
            "open_hours": open_hours or [],
        }
        resp = self.session.post(url, json=data)
        _validate(resp)
        return resp.json()

    def consecutive_availability(
        self,
        emails,
        duration,
        interval,
        start_at,
        end_at,
        buffer=None,
        free_busy=None,
        open_hours=None,
    ):
        if isinstance(emails, six.string_types):
            emails = [[emails]]
        elif isinstance(emails[0], list) is False:
            raise ValueError("'emails' must be a list of lists.")
        if isinstance(duration, timedelta):
            duration_minutes = int(duration.total_seconds() // 60)
        else:
            duration_minutes = int(duration)
        if isinstance(interval, timedelta):
            interval_minutes = int(interval.total_seconds() // 60)
        else:
            interval_minutes = int(interval)
        if isinstance(start_at, datetime):
            start_time = timestamp_from_dt(start_at)
        else:
            start_time = start_at
        if isinstance(end_at, datetime):
            end_time = timestamp_from_dt(end_at)
        else:
            end_time = end_at
        if open_hours is not None:
            self._validate_open_hours(emails, open_hours, free_busy)

        url = "{api_server}/calendars/availability/consecutive".format(
            api_server=self.api_server
        )
        data = {
            "emails": emails,
            "duration_minutes": duration_minutes,
            "interval_minutes": interval_minutes,
            "start_time": start_time,
            "end_time": end_time,
            "buffer": buffer,
            "free_busy": free_busy or [],
            "open_hours": open_hours or [],
        }
        resp = self.session.post(url, json=data)
        _validate(resp)
        return resp.json()

    @property
    def account(self):
        return self._get_resource(SingletonAccount, "")

    @property
    def accounts(self):
        if self.is_opensource_api():
            return RestfulModelCollection(APIAccount, self)
        return RestfulModelCollection(Account, self)

    @property
    def threads(self):
        return RestfulModelCollection(Thread, self)

    @property
    def folders(self):
        return RestfulModelCollection(Folder, self)

    @property
    def labels(self):
        return RestfulModelCollection(Label, self)

    @property
    def messages(self):
        return RestfulModelCollection(Message, self)

    @property
    def files(self):
        return RestfulModelCollection(File, self)

    @property
    def drafts(self):
        return RestfulModelCollection(Draft, self)

    @property
    def contacts(self):
        return RestfulModelCollection(Contact, self)

    @property
    def events(self):
        return RestfulModelCollection(Event, self)

    @property
    def room_resources(self):
        return RestfulModelCollection(RoomResource, self)

    @property
    def calendars(self):
        return RestfulModelCollection(Calendar, self)

    @property
    def neural(self):
        return Neural(self)

    ##########################################################
    #   Private functions used by Restful Model Collection   #
    ##########################################################

    def _get_http_session(self, api_root):
        # Is this a request for a resource under the accounts/billing/admin
        # namespace (/a)? If the latter, pass the client_secret
        # instead of the secret_token
        if api_root == "a":
            return self.admin_session
        return self.session

    def _get_resources(self, cls, extra=None, **filters):
        # FIXME @karim: remove this interim code when we've got rid
        # of the old accounts API.
        postfix = "/{}".format(extra) if extra else ""
        if cls.api_root != "a":
            url = "{}/{}{}".format(self.api_server, cls.collection_name, postfix)
        else:
            url = "{}/a/{}/{}{}".format(
                self.api_server, self.client_id, cls.collection_name, postfix
            )

        converted_data = create_request_body(filters, cls.datetime_filter_attrs)
        url = str(URLObject(url).add_query_params(converted_data.items()))
        response = self._get_http_session(cls.api_root).get(url)
        results = _validate(response).json()
        return [cls.create(self, **x) for x in results if x is not None]

    def _get_resource_raw(
        self, cls, id, extra=None, headers=None, stream=False, **filters
    ):
        """Get an individual REST resource"""
        headers = headers or {}
        headers.update(self.session.headers)

        postfix = "/{}".format(extra) if extra else ""
        if cls.api_root != "a":
            url = "{}/{}/{}{}".format(self.api_server, cls.collection_name, id, postfix)
        else:
            url = "{}/a/{}/{}/{}{}".format(
                self.api_server, self.client_id, cls.collection_name, id, postfix
            )

        converted_data = create_request_body(filters, cls.datetime_filter_attrs)
        url = str(URLObject(url).add_query_params(converted_data.items()))
        response = self._get_http_session(cls.api_root).get(
            url, headers=headers, stream=stream
        )
        return _validate(response)

    def _get_resource(self, cls, id, **filters):
        response = self._get_resource_raw(cls, id, **filters)
        result = response.json()
        if isinstance(result, list):
            result = result[0]
        return cls.create(self, **result)

    def _get_resource_data(self, cls, id, extra=None, headers=None, **filters):
        response = self._get_resource_raw(
            cls, id, extra=extra, headers=headers, **filters
        )
        return response.content

    def _create_resource(self, cls, data, **kwargs):
        url = (
            URLObject(self.api_server)
            .with_path("/{name}/".format(name=cls.collection_name))
            .set_query_params(**kwargs)
        )

        session = self._get_http_session(cls.api_root)

        if cls == File:
            response = session.post(url, files=data)
        else:
            converted_data = create_request_body(data, cls.datetime_attrs)
            headers = {"Content-Type": "application/json"}
            headers.update(self.session.headers)
            response = session.post(url, json=converted_data, headers=headers)

        result = _validate(response).json()
        if cls.collection_name == "send":
            return result
        return cls.create(self, **result)

    def _create_resources(self, cls, data):
        url = URLObject(self.api_server).with_path(
            "/{name}/".format(name=cls.collection_name)
        )
        session = self._get_http_session(cls.api_root)

        if cls == File:
            response = session.post(url, files=data)
        else:
            converted_data = [
                create_request_body(datum, cls.datetime_attrs) for datum in data
            ]
            headers = {"Content-Type": "application/json"}
            headers.update(self.session.headers)
            response = session.post(url, json=converted_data, headers=headers)

        results = _validate(response).json()
        return [cls.create(self, **x) for x in results]

    def _delete_resource(self, cls, id, data=None, **kwargs):
        url = (
            URLObject(self.api_server)
            .with_path("/{name}/{id}".format(name=cls.collection_name, id=id))
            .set_query_params(**kwargs)
        )
        session = self._get_http_session(cls.api_root)
        if data:
            _validate(session.delete(url, json=data))
        else:
            _validate(session.delete(url))

    def _update_resource(self, cls, id, data, **kwargs):
        url = (
            URLObject(self.api_server)
            .with_path("/{name}/{id}".format(name=cls.collection_name, id=id))
            .set_query_params(**kwargs)
        )

        session = self._get_http_session(cls.api_root)

        converted_data = create_request_body(data, cls.datetime_attrs)
        response = session.put(url, json=converted_data)

        result = _validate(response).json()
        return cls.create(self, **result)

    def _call_resource_method(self, cls, id, method_name, data):
        """POST a dictionary to an API method,
        for example /a/.../accounts/id/upgrade"""

        if cls.api_root != "a":
            url_path = "/{name}/{id}/{method}".format(
                name=cls.collection_name, id=id, method=method_name
            )
        else:
            # Management method.
            url_path = "/a/{client_id}/{name}/{id}/{method}".format(
                client_id=self.client_id,
                name=cls.collection_name,
                id=id,
                method=method_name,
            )

        url = URLObject(self.api_server).with_path(url_path)
        converted_data = create_request_body(data, cls.datetime_attrs)

        session = self._get_http_session(cls.api_root)
        response = session.post(url, json=converted_data)

        result = _validate(response).json()
        return cls.create(self, **result)

    def _request_neural_resource(self, cls, data, path=None, method="PUT"):
        if path is None:
            path = cls.collection_name
        url = URLObject(self.api_server).with_path("/neural/{name}".format(name=path))

        session = self._get_http_session(cls.api_root)

        converted_data = create_request_body(data, cls.datetime_attrs)
        response = session.request(method, url, json=converted_data)

        result = _validate(response).json()
        if isinstance(result, list):
            object_list = []
            for obj in result:
                object_list.append(cls.create(self, **obj))
            return object_list

        return cls.create(self, **result)

    def _validate_open_hours(self, emails, open_hours, free_busy):
        if isinstance(open_hours, list) is False:
            raise ValueError("'open_hours' must be an array.")
        open_hours_emails = list(
            chain.from_iterable([oh["emails"] for oh in open_hours])
        )
        free_busy_emails = (
            [fb["email"] for fb in free_busy] if free_busy is not None else []
        )
        if isinstance(emails[0], list) is True:
            emails = list(chain.from_iterable(emails))
        for email in open_hours_emails:
            if (email in emails) is False and (email in free_busy_emails) is False:
                raise ValueError(
                    "Open Hours cannot contain an email not present in the main email list or the free busy email list."
                )
