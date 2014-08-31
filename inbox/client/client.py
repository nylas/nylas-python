from os import environ
import requests
import six
import json
from base64 import b64encode
from six.moves.urllib.parse import urlencode
from .util import url_concat, generate_id
from .restful_model_collection import RestfulModelCollection
from .models import Namespace, File
from .errors import ConnectionError, NotAuthorizedError, APIError

API_SERVER = "https://api.inboxapp.com"


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

    def _get_resources(self, namespace, cls, filters={}):
        prefix = "/n/{}".format(namespace) if namespace else ''
        url = "{}{}/{}".format(self.api_server, prefix, cls.collection_name)

        if filters:
            url = url_concat(url, filters)

        response = self.session.get(url)
        if response.status_code != 200:
            response.raise_for_status()

        results = response.json()
        return map(lambda x: cls.from_dict(self, namespace, x), results)

    def _get_resource_raw(self, namespace, cls, id, filters={}, extra=''):
        """Get an individual REST resource"""
        prefix = "/n/{}".format(namespace) if namespace else ''
        postfix = "/{}".format(extra) if extra else ''
        url = "{}{}/{}/{}{}".format(self.api_server, prefix,
                                    cls.collection_name, id, postfix)

        if filters:
            url = url_concat(url, filters)

        response = self.session.get(url)
        if response.status_code != 200:
            response.raise_for_status()

        return response

    def _get_resource(self, namespace, cls, id, filters={}, extra=''):
        response = self._get_resource_raw(namespace, cls, id, filters, extra)
        result = response.json()
        return cls.from_dict(self, namespace, result)

    def _get_resource_data(self, namespace, cls, id, filters={}, extra=''):
        response = self._get_resource_raw(namespace, cls, id, filters, extra)
        return response.content

    def _create_resource(self, namespace, cls, data):
        prefix = "/n/{}".format(namespace) if namespace else ''
        url = "{}{}/{}/".format(self.api_server, prefix, cls.collection_name)

        if cls == File:
            response = self.session.post(url, files=data)
        else:
            headers = {'content_type': 'json'}
            headers.update(self.session.headers)
            response = self.session.post(url, data=json.dumps(data),
                                         headers=headers)

        if response.status_code != 200:
            print "failing url: ", url
            print "Error: ", response.text
            response.raise_for_status()

        result = response.json()
        return cls.from_dict(self, namespace, result)

    def _create_resources(self, namespace, cls, data):
        prefix = "/n/{}".format(namespace) if namespace else ''
        url = "{}{}/{}/".format(self.api_server, prefix, cls.collection_name)

        if cls == File:
            response = self.session.post(url, files=data)
        else:
            headers = {'content_type': 'json'}
            headers.update(self.session.headers)
            response = self.session.post(url, data=json.dumps(data),
                                         headers=headers)

        if response.status_code != 200:
            print "failing url: ", url
            print "Error: ", response.text
            response.raise_for_status()

        results = response.json()
        return map(lambda x: cls.from_dict(self, namespace, x), results)

    def _delete_resource(self, namespace, cls, id):
        prefix = "/n/{}".format(namespace) if namespace else ''
        name = cls.collection_name
        url = "{}{}/{}/{}".format(self.api_server, prefix, name, id)

        response = self.session.delete(url)
        if response.status_code != 200:
            response.raise_for_status()

    def _update_resource(self, namespace, cls, id, data):
        prefix = "/n/{}".format(namespace) if namespace else ''
        name = cls.collection_name
        url = "{}{}/{}/{}".format(self.api_server, prefix, name, id)

        response = self.session.put(url, data=json.dumps(data))
        if response.status_code != 200:
            response.raise_for_status()

        result = response.json()
        return cls.from_dict(self, namespace, result)
