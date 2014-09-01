from os import environ
import requests
import six
import json
from base64 import b64encode
from six.moves.urllib.parse import urlencode
from .util import url_concat, generate_id
from .restful_model_collection import RestfulModelCollection
from .models import Namespace, File
from .errors import (APIClientError, ConnectionError, NotAuthorizedError, APIError,
                     NotFoundError, ConflictError)
from requests.exceptions import ConnectionError as RequestsConnectionError

API_SERVER = "https://api.inboxapp.com"

def _validate(response):
    status_code_to_exc = {400: APIError, 404: NotFoundError, 409: ConflictError}
    request = response.request
    url = request.url
    status_code = response.status_code
    data = request.body

    try:
        data = json.loads(data) if data else None
    except (ValueError, TypeError):
        pass

    if status_code == 200:
        return response
    elif status_code == 401:
        raise NotAuthorizedError(url=url, status_code=status_code, data=data)
    elif status_code in [400, 404, 409]:
        cls = status_code_to_exc[status_code]
        try:
            response = json.loads(response.text)
            if 'message' in response:
                raise cls(url=url, status_code=status_code,
                          data=data, message=response['message'])
            else:
                raise cls(url=url, status_code=status_code,
                          data=data, message="N/A")
        except (ValueError, TypeError):
            raise cls(url=url, status_code=status_code,
                      data=data, message="Malformed")
    else:
        raise APIClientError(url=url, status_code=status_code,
                             data=data, message="Uknown status code.")


def inbox_excepted(f):
    def caught(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except RequestsConnectionError as e:
            server = args[0].api_server
            raise ConnectionError(url=server)
    return caught


class APIClient(json.JSONEncoder):
    """API client for the Inbox API."""

    def __init__(self, app_id=environ.get('INBOX_APP_ID'),
                 app_secret=environ.get('INBOX_APP_SECRET'),
                 access_token=environ.get('INBOX_ACCESS_TOKEN'),
                 api_server=API_SERVER):
        if "://" not in api_server:
            raise Exception("When overriding the Inbox API server address, you"
                            " must include https://")
        self.set_api_server(api_server)
        self.session = requests.Session()
        self.session.headers = {'X-Inbox-API-Wrapper': 'python'}
        self.access_token = access_token
        self.app_secret = app_secret
        self.app_id = app_id

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value
        if value:
            self.session.headers.update({'Authorization': 'Basic ' +
                                         b64encode(value + ':')})

    def set_api_server(self, api_server):
        self.api_server = api_server
        self.authorize_url = self.api_server+"/oauth/authorize"
        self.access_token_url = self.api_server+"/oauth/token"

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

    @property
    def namespaces(self):
        return RestfulModelCollection(Namespace, self, None)

    @inbox_excepted
    def _get_resources(self, namespace, cls, filters={}):
        prefix = "/n/{}".format(namespace) if namespace else ''
        url = "{}{}/{}".format(self.api_server, prefix, cls.collection_name)
        url = url_concat(url, filters)

        results = _validate(self.session.get(url)).json()
        return map(lambda x: cls.from_dict(self, namespace, x), results)

    @inbox_excepted
    def _get_resource_raw(self, namespace, cls, id, filters={}, extra=''):
        """Get an individual REST resource"""
        prefix = "/n/{}".format(namespace) if namespace else ''
        postfix = "/{}".format(extra) if extra else ''
        url = "{}{}/{}/{}{}".format(self.api_server, prefix,
                                    cls.collection_name, id, postfix)
        url = url_concat(url, filters)

        return _validate(self.session.get(url))

    def _get_resource(self, namespace, cls, id, filters={}, extra=''):
        response = self._get_resource_raw(namespace, cls, id, filters, extra)
        result = response.json()
        return cls.from_dict(self, namespace, result)

    def _get_resource_data(self, namespace, cls, id, filters={}, extra=''):
        response = self._get_resource_raw(namespace, cls, id, filters, extra)
        return response.content

    @inbox_excepted
    def _create_resource(self, namespace, cls, data):
        prefix = "/n/{}".format(namespace) if namespace else ''
        url = "{}{}/{}/".format(self.api_server, prefix, cls.collection_name)

        if cls == File:
            response = self.session.post(url, files=data)
        else:
            data=json.dumps(data)
            headers = {'content_type': 'json'}.update(self.session.headers)
            response = self.session.post(url, data=data, headers=headers)

        result = _validate(response).json()
        return cls.from_dict(self, namespace, result)

    @inbox_excepted
    def _create_resources(self, namespace, cls, data):
        prefix = "/n/{}".format(namespace) if namespace else ''
        url = "{}{}/{}/".format(self.api_server, prefix, cls.collection_name)

        if cls == File:
            response = self.session.post(url, files=data)
        else:
            data=json.dumps(data)
            headers = {'content_type': 'json'}.update(self.session.headers)
            response = self.session.post(url, data=data, headers=headrs)

        results = _validate(response).json()
        return map(lambda x: cls.from_dict(self, namespace, x), results)

    @inbox_excepted
    def _delete_resource(self, namespace, cls, id):
        prefix = "/n/{}".format(namespace) if namespace else ''
        name = cls.collection_name
        url = "{}{}/{}/{}".format(self.api_server, prefix, name, id)
        _validate(self.session.delete(url))

    @inbox_excepted
    def _update_resource(self, namespace, cls, id, data):
        prefix = "/n/{}".format(namespace) if namespace else ''
        name = cls.collection_name
        url = "{}{}/{}/{}".format(self.api_server, prefix, name, id)

        response = self.session.put(url, data=json.dumps(data))

        result = _validate(response).json()
        return cls.from_dict(self, namespace, result)
