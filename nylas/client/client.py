import sys
import requests
import json
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
from os import environ
from base64 import b64encode
from six.moves.urllib.parse import urlencode
from nylas._client_sdk_version import __VERSION__
from .util import url_concat, generate_id
from .restful_model_collection import RestfulModelCollection
from .restful_models import (Calendar, Contact, Event, Message, Thread, File,
                             Account, APIAccount, SingletonAccount, Folder,
                             Label, Draft)
from .errors import (APIClientError, ConnectionError, NotAuthorizedError,
                     InvalidRequestError, NotFoundError, MethodNotSupportedError,
                     ServerError, ServiceUnavailableError, ConflictError,
                     SendingQuotaExceededError, ServerTimeoutError,
                     MessageRejectedError)

DEBUG = environ.get('NYLAS_CLIENT_DEBUG')
API_SERVER = "https://api.nylas.com"


def _validate(response):
    status_code_to_exc = {400: InvalidRequestError,
                          401: NotAuthorizedError,
                          402: MessageRejectedError,
                          403: NotAuthorizedError,
                          404: NotFoundError,
                          405: MethodNotSupportedError,
                          409: ConflictError,
                          429: SendingQuotaExceededError,
                          500: ServerError,
                          503: ServiceUnavailableError,
                          504: ServerTimeoutError}
    request = response.request
    url = request.url
    status_code = response.status_code
    data = request.body

    if DEBUG:
        print("{} {} ({}) => {}: {}".format(request.method, url, data,
                                            status_code, response.text))

    try:
        data = json.loads(data) if data else None
    except (ValueError, TypeError):
        pass

    if status_code == 200:
        return response
    elif status_code in status_code_to_exc:
        cls = status_code_to_exc[status_code]
        try:
            response = json.loads(response.text)
            kwargs = dict(url=url, status_code=status_code,
                          data=data)

            for key in ['message', 'server_error']:
                if key in response:
                    kwargs[key] = response[key]

            raise cls(**kwargs)

        except (ValueError, TypeError):
            raise cls(url=url, status_code=status_code,
                      data=data, message="Malformed")
    else:
        raise APIClientError(url=url, status_code=status_code,
                             data=data, message="Unknown status code.")


def nylas_excepted(f):
    def caught(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            server = args[0].api_server
            raise ConnectionError(url=server)
    return caught


class APIClient(json.JSONEncoder):
    """API client for the Nylas API."""

    def __init__(self, app_id=environ.get('NYLAS_APP_ID'),
                 app_secret=environ.get('NYLAS_APP_SECRET'),
                 access_token=environ.get('NYLAS_ACCESS_TOKEN'),
                 api_server=API_SERVER,
                 auth_server=None):
        if "://" not in api_server:
            raise Exception("When overriding the Nylas API server address, you"
                            " must include https://")
        self.api_server = api_server
        self.authorize_url = api_server + '/oauth/authorize'
        self.access_token_url = api_server + '/oauth/token'

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
        self.access_token = access_token

        # Requests to the /a/ namespace don't use an auth token but
        # the app_secret. Set up a specific session for this.
        self.admin_session = requests.Session()

        if app_secret is not None:
            # In Python 3 b64encode only accepts bytes, so we need to ensure
            # we are not passing in a string for app_secret
            if isinstance(app_secret, str):
                app_secret_bytes = self.app_secret.encode()
            else:
                app_secret_bytes = self.app_secret
            app_secret_b64 = b64encode(app_secret_bytes + b':').decode()
            self.admin_session.headers = {'Authorization': 'Basic ' +
                                          app_secret_b64,
                                          'X-Nylas-API-Wrapper': 'python',
                                          'User-Agent': version_header}

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value
        # In Python 3 b64encode only accepts bytes, so we need to ensure we
        # are not passing in a string for value
        if value:
            if isinstance(value, str):
                value = value.encode()
            value_b64 = b64encode(value + b':').decode()
            self.session.headers.update({'Authorization': 'Basic ' +
                                         value_b64})

    def authentication_url(self, redirect_uri, login_hint=''):
        args = {'redirect_uri': redirect_uri,
                'client_id': self.app_id,
                'response_type': 'code',
                'scope': 'email',
                'login_hint': login_hint,
                'state': generate_id()}

        return url_concat(self.authorize_url, args)

    def token_for_code(self, code):
        args = {'client_id': self.app_id,
                'client_secret': self.app_secret,
                'grant_type': 'authorization_code',
                'code': code}

        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}

        resp = requests.post(self.access_token_url, data=urlencode(args),
                             headers=headers).json()

        self.auth_token = resp[u'access_token']
        return self.auth_token

    def is_opensource_api(self):
        if self.app_id is None and self.app_secret is None:
            return True

        return False

    @property
    def account(self):
        return self._get_resource(SingletonAccount, '')

    @property
    def accounts(self):
        if self.is_opensource_api():
            return RestfulModelCollection(APIAccount, self)
        else:
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
        else:
            return self.session

    @nylas_excepted
    def _get_resources(self, cls, **filters):
        # FIXME @karim: remove this interim code when we've got rid
        # of the old accounts API.
        if cls.api_root != 'a':
            url = "{}/{}".format(self.api_server, cls.collection_name)
        else:
            url = "{}/a/{}/{}".format(self.api_server, self.app_id,
                                      cls.collection_name)

        url = url_concat(url, filters)
        response = self._get_http_session(cls.api_root).get(url)
        results = _validate(response).json()
        return list(
            filter(
                lambda x: x is not None,
                map(lambda x: cls.create(self, **x), results)
                )
            )

    @nylas_excepted
    def _get_resource_raw(self, cls, id, extra=None,
                          headers=None, **filters):
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

        url = url_concat(url, filters)

        response = self._get_http_session(cls.api_root).get(url, headers=headers)
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

    @nylas_excepted
    def _create_resource(self, cls, data, **kwargs):
        url = "{}/{}/".format(self.api_server, cls.collection_name)

        if len(kwargs.keys()) > 0:
            url = "{}?{}".format(url, urlencode(kwargs))

        session = self._get_http_session(cls.api_root)

        if cls == File:
            response = session.post(url, files=data)
        else:
            data = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            headers.update(self.session.headers)
            response = session.post(url, data=data, headers=headers)

        result = _validate(response).json()
        if cls.collection_name == 'send':
            return result
        return cls.create(self, **result)

    @nylas_excepted
    def _create_resources(self, cls, data):
        url = "{}/{}/".format(self.api_server, cls.collection_name)
        session = self._get_http_session(cls.api_root)

        if cls == File:
            response = session.post(url, files=data)
        else:
            data = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            headers.update(self.session.headers)
            response = session.post(url, data=data, headers=headers)

        results = _validate(response).json()
        return list(map(lambda x: cls.create(self, **x), results))

    @nylas_excepted
    def _delete_resource(self, cls, id, data=None, **kwargs):
        name = cls.collection_name
        url = "{}/{}/{}".format(self.api_server, name, id)

        if len(kwargs.keys()) > 0:
            url = "{}?{}".format(url, urlencode(kwargs))
        session = self._get_http_session(cls.api_root)
        if data:
            _validate(session.delete(url, json=data))
        else:
            _validate(session.delete(url))

    @nylas_excepted
    def _update_resource(self, cls, id, data, **kwargs):
        name = cls.collection_name
        url = "{}/{}/{}".format(self.api_server, name, id)

        if len(kwargs.keys()) > 0:
            url = "{}?{}".format(url, urlencode(kwargs))

        session = self._get_http_session(cls.api_root)

        response = session.put(url, json=data)

        result = _validate(response).json()
        return cls.create(self, **result)

    @nylas_excepted
    def _call_resource_method(self, cls, id, method_name, data):
        """POST a dictionnary to an API method,
        for example /a/.../accounts/id/upgrade"""
        name = cls.collection_name
        if cls.api_root != 'a':
            url = "{}/{}/{}/{}".format(self.api_server, name, id, method_name)
        else:
            # Management method.
            url = "{}/a/{}/{}/{}/{}".format(self.api_server, self.app_id,
                                      cls.collection_name, id, method_name)


        session = self._get_http_session(cls.api_root)
        response = session.post(url, json=data)

        return _validate(response).json()
