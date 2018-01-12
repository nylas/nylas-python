from __future__ import print_function
import sys
from os import environ
from base64 import b64encode
import json

import requests
from urlobject import URLObject
from six.moves.urllib.parse import urlencode
from nylas._client_sdk_version import __VERSION__
from nylas.client.errors import MessageRejectedError
from nylas.client.restful_model_collection import RestfulModelCollection
from nylas.client.restful_models import (
    Calendar, Contact, Event, Message, Thread, File,
    Account, APIAccount, SingletonAccount, Folder,
    Label, Draft
)
from nylas.utils import convert_datetimes_to_timestamps

DEBUG = environ.get('NYLAS_CLIENT_DEBUG')
API_SERVER = "https://api.nylas.com"


def _validate(response):
    if DEBUG:  # pragma: no cover
        print("{method} {url} ({body}) => {status}: {text}".format(
            method=response.request.method,
            url=response.request.url,
            body=response.request.body,
            status=response.status_code,
            text=response.text,
        ))

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

    def __init__(self, app_id=environ.get('NYLAS_APP_ID'),
                 app_secret=environ.get('NYLAS_APP_SECRET'),
                 access_token=environ.get('NYLAS_ACCESS_TOKEN'),
                 api_server=API_SERVER):
        if not api_server.startswith("https://"):
            raise Exception("When overriding the Nylas API server address, you"
                            " must include https://")
        self.api_server = api_server
        self.authorize_url = api_server + '/oauth/authorize'
        self.access_token_url = api_server + '/oauth/token'
        self.revoke_url = api_server + '/oauth/revoke'

        self.app_secret = app_secret
        self.app_id = app_id

        self.session = requests.Session()
        self.version = __VERSION__
        major, minor, revision, _, __ = sys.version_info
        version_header = 'Nylas Python SDK {} - {}.{}.{}'.format(self.version,
                                                                 major, minor,
                                                                 revision)
        self.session.headers = {'X-Nylas-API-Wrapper': 'python',
                                'User-Agent': version_header}
        self._access_token = None
        self.access_token = access_token
        self.auth_token = None

        # Requests to the /a/ namespace don't use an auth token but
        # the app_secret. Set up a specific session for this.
        self.admin_session = requests.Session()

        if app_secret is not None:
            b64_app_secret = b64encode((app_secret + ':').encode('utf8'))
            authorization = 'Basic {secret}'.format(
                secret=b64_app_secret.decode('utf8')
            )
            self.admin_session.headers = {
                'Authorization': authorization,
                'X-Nylas-API-Wrapper': 'python',
                'User-Agent': version_header,
            }
        super(APIClient, self).__init__()

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value
        if value:
            authorization = 'Bearer {token}'.format(token=value)
            self.session.headers['Authorization'] = authorization
        else:
            if 'Authorization' in self.session.headers:
                del self.session.headers['Authorization']

    def authentication_url(self, redirect_uri, login_hint='', state=''):
        args = {'redirect_uri': redirect_uri,
                'client_id': self.app_id or 'None',  # 'None' for back-compat
                'response_type': 'code',
                'scope': 'email',
                'login_hint': login_hint,
                'state': state}

        url = URLObject(self.authorize_url).add_query_params(args.items())
        return str(url)

    def token_for_code(self, code):
        args = {'client_id': self.app_id,
                'client_secret': self.app_secret,
                'grant_type': 'authorization_code',
                'code': code}

        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}

        resp = requests.post(self.access_token_url, data=urlencode(args),
                             headers=headers).json()

        self.access_token = resp[u'access_token']
        return self.access_token

    def is_opensource_api(self):
        if self.app_id is None and self.app_secret is None:
            return True

        return False

    def revoke_token(self):
        resp = self.session.post(self.revoke_url)
        _validate(resp)
        self.auth_token = None
        self.access_token = None

    @property
    def account(self):
        return self._get_resource(SingletonAccount, '')

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
    def calendars(self):
        return RestfulModelCollection(Calendar, self)

    ##########################################################
    #   Private functions used by Restful Model Collection   #
    ##########################################################

    def _get_http_session(self, api_root):
        # Is this a request for a resource under the accounts/billing/admin
        # namespace (/a)? If the latter, pass the app_secret
        # instead of the secret_token
        if api_root == 'a':
            return self.admin_session
        return self.session

    def _get_resources(self, cls, extra=None, **filters):
        # FIXME @karim: remove this interim code when we've got rid
        # of the old accounts API.
        postfix = "/{}".format(extra) if extra else ''
        if cls.api_root != 'a':
            url = "{}/{}{}".format(
                self.api_server,
                cls.collection_name,
                postfix
            )
        else:
            url = "{}/a/{}/{}{}".format(
                self.api_server,
                self.app_id,
                cls.collection_name,
                postfix
            )

        converted_filters = convert_datetimes_to_timestamps(
            filters, cls.datetime_filter_attrs,
        )
        url = str(URLObject(url).add_query_params(converted_filters.items()))
        response = self._get_http_session(cls.api_root).get(url)
        results = _validate(response).json()
        return [
            cls.create(self, **x)
            for x in results
            if x is not None
        ]

    def _get_resource_raw(self, cls, id, extra=None,
                          headers=None, stream=False, **filters):
        """Get an individual REST resource"""
        headers = headers or {}
        headers.update(self.session.headers)

        postfix = "/{}".format(extra) if extra else ''
        if cls.api_root != 'a':
            url = "{}/{}/{}{}".format(self.api_server, cls.collection_name, id,
                                      postfix)
        else:
            url = "{}/a/{}/{}/{}{}".format(self.api_server, self.app_id,
                                           cls.collection_name, id, postfix)

        converted_filters = convert_datetimes_to_timestamps(
            filters, cls.datetime_filter_attrs,
        )
        url = str(URLObject(url).add_query_params(converted_filters.items()))

        response = self._get_http_session(cls.api_root).get(
            url, headers=headers, stream=stream,
        )
        return _validate(response)

    def _get_resource(self, cls, id, **filters):
        response = self._get_resource_raw(cls, id, **filters)
        result = response.json()
        if isinstance(result, list):
            result = result[0]
        return cls.create(self, **result)

    def _get_resource_data(self, cls, id,
                           extra=None, headers=None, **filters):
        response = self._get_resource_raw(cls, id, extra=extra,
                                          headers=headers, **filters)
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
            converted_data = convert_datetimes_to_timestamps(data, cls.datetime_attrs)
            headers = {'Content-Type': 'application/json'}
            headers.update(self.session.headers)
            response = session.post(url, json=converted_data, headers=headers)

        result = _validate(response).json()
        if cls.collection_name == 'send':
            return result
        return cls.create(self, **result)

    def _create_resources(self, cls, data):
        url = (
            URLObject(self.api_server)
            .with_path("/{name}/".format(name=cls.collection_name))
        )
        session = self._get_http_session(cls.api_root)

        if cls == File:
            response = session.post(url, files=data)
        else:
            converted_data = [
                convert_datetimes_to_timestamps(datum, cls.datetime_attrs)
                for datum in data
            ]
            headers = {'Content-Type': 'application/json'}
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

        converted_data = convert_datetimes_to_timestamps(data, cls.datetime_attrs)
        response = session.put(url, json=converted_data)

        result = _validate(response).json()
        return cls.create(self, **result)

    def _call_resource_method(self, cls, id, method_name, data):
        """POST a dictionary to an API method,
        for example /a/.../accounts/id/upgrade"""

        if cls.api_root != 'a':
            url_path = "/{name}/{id}/{method}".format(
                name=cls.collection_name, id=id, method=method_name
            )
        else:
            # Management method.
            url_path = "/a/{app_id}/{name}/{id}/{method}".format(
                app_id=self.app_id,
                name=cls.collection_name,
                id=id,
                method=method_name,
            )

        url = (
            URLObject(self.api_server)
            .with_path(url_path)
        )
        converted_data = convert_datetimes_to_timestamps(data, cls.datetime_attrs)

        session = self._get_http_session(cls.api_root)
        response = session.post(url, json=converted_data)

        result = _validate(response).json()
        return cls.create(self, **result)
