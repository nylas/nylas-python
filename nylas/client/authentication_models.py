from copy import copy

from nylas.client.restful_model_collection import RestfulModelCollection, CHUNK_SIZE
from nylas.client.restful_models import NylasAPIObject
from nylas.utils import AuthMethod
from enum import Enum


class Integration(NylasAPIObject):
    attrs = (
        "name",
        "provider",
        "expires_in",
        "settings",
        "redirect_uris",
        "scope",
        "id",
    )
    read_only_attrs = {"provider", "id"}
    auth_method = AuthMethod.BASIC_CLIENT_ID_AND_SECRET
    collection_name = "connect/integrations"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Integration, api)
        self.settings = {}
        self.scope = []

    def set_client_id(self, client_id):
        """
        Set the client ID of the OAuth provider

        Args:
            client_id (str): Client ID of the OAuth provider
        """
        self.settings["client_id"] = client_id

    def set_client_secret(self, client_secret):
        """
        Set the client secret of the OAuth provider

        Args:
            client_secret (str): Client secret of the OAuth provider
        """
        self.settings["client_secret"] = client_secret

    @classmethod
    def create(cls, api, **kwargs):
        if "data" in kwargs:
            kwargs = kwargs.get("data")
        obj = super(Integration, cls).create(api, **kwargs)
        if "provider" in kwargs:
            obj["id"] = kwargs.get("provider")

        return obj

    def as_json(self):
        dct = super(Integration, self).as_json()
        if not self.id:
            if isinstance(self.provider, Authentication.Provider):
                dct["provider"] = self.provider.value
            else:
                dct["provider"] = self.provider

        return dct

    def _update_resource(self, **kwargs):
        provider = self.id or self.provider
        return self.api._patch_resource(self.cls, provider, self.as_json(), **kwargs)


class Grant(NylasAPIObject):
    attrs = (
        "id",
        "provider",
        "state",
        "email",
        "ip",
        "grant_status",
        "user_agent",
        "created_at",
        "updated_at",
        "settings",
        "metadata",
        "scope",
    )
    read_only_attrs = {
        "id",
        "email",
        "ip",
        "grant_status",
        "user_agent",
        "created_at",
        "updated_at",
    }
    auth_method = AuthMethod.BASIC_CLIENT_ID_AND_SECRET
    collection_name = "connect/grants"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Grant, api)
        self.settings = {}
        self.metadata = {}
        self.scope = []

    @classmethod
    def create(cls, api, **kwargs):
        if "data" in kwargs:
            kwargs = kwargs.get("data")
        obj = super(Grant, cls).create(api, **kwargs)
        return obj

    def as_json(self):
        dct = super(Grant, self).as_json()
        # provider and state can not be updated
        if self.id:
            del dct["provider"]
            del dct["state"]
        else:
            if isinstance(self.provider, Authentication.Provider):
                dct["provider"] = self.provider.value
            else:
                dct["provider"] = self.provider

        return dct

    def _update_resource(self, **kwargs):
        return self.api._patch_resource(self.cls, self.id, self.as_json(), **kwargs)


class Authentication(object):
    def __init__(self, api):
        self._app_name = "beta"
        self._region = Authentication.Region.US
        # Make a copy of the API as we need to change the base url for Integration calls
        self.api = copy(api)
        self._set_integrations_api_url()

    @property
    def app_name(self):
        return self._app_name

    @app_name.setter
    def app_name(self, value):
        """
        Set the name of the application to prefix the URL for all integration calls for this instance

        Args:
            value (str): The name of the application
        """
        self._app_name = value
        self._set_integrations_api_url()

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        """
        Set the region to prefix the URL for all integration calls for this instance

        Args:
            value (Integration.Region): The region
        """
        self._region = value
        self._set_integrations_api_url()

    @property
    def integrations(self):
        """
        Integrations API for integrating a provider to the Nylas application

        Returns:
            IntegrationRestfulModelCollection: The Integration API configured with the app_name and region
        """
        return IntegrationRestfulModelCollection(self.api)

    @property
    def grants(self):
        """
        Native Authentication for the integrated provider

        Returns:
            GrantRestfulModelCollection: The Grants API configured with the app_name and region
        """
        return GrantRestfulModelCollection(self.api)

    def hosted_authentication(
        self,
        provider,
        redirect_uri,
        grant_id=None,
        login_hint=None,
        state=None,
        expires_in=None,
        settings=None,
        metadata=None,
        scope=None,
    ):
        """
        Hosted Authentication for the integrated provider

        Args:
            provider (Authentication.Provider): OAuth provider
            redirect_uri (str): The URI for the final redirect
            grant_id (str): Existing Grant ID to trigger a re-authentication
            login_hint (str): Hint to simplify the login flow
            state (str): State value to return after authentication flow is completed
            expires_in (int): How long this request (and the attached login) ID will remain valid before the link expires
            settings (dict[str, str]): Settings required by provider
            metadata (dict[str, any]): Metadata to store as part of the grant
            scope (list[str]): OAuth provider-specific scopes

        Returns:
            dict[str, any]: The login information
        """
        request = {"provider": provider, "redirect_uri": redirect_uri}
        if grant_id:
            request["grant_id"] = grant_id
        if login_hint:
            request["login_hint"] = login_hint
        if state:
            request["state"] = state
        if expires_in:
            request["expires_in"] = expires_in
        if settings:
            request["settings"] = settings
        if metadata:
            request["metadata"] = metadata
        if scope:
            request["scope"] = scope

        response = self.api._post_resource(Grant, "auth", None, request, path="connect")
        if "data" in response:
            response = response["data"]

        return response

    def _set_integrations_api_url(self):
        self.api.api_server = "https://{app_name}.{region}.nylas.com".format(
            app_name=self.app_name, region=self.region.value
        )

    class Region(str, Enum):
        """
        This is an Enum the regions supported by the Integrations API
        """

        US = "us"
        EU = "eu"

    class Provider(str, Enum):
        """
        This is an Enum representing all the available providers for integrations
        """

        GOOGLE = "google"
        MICROSOFT = "microsoft"
        IMAP = "imap"
        ZOOM = "zoom"


class AuthenticationRestfulModelCollection(RestfulModelCollection):
    def __init__(self, model_class, api):
        RestfulModelCollection.__init__(self, model_class, api)

    def _get_model_collection(self, offset=0, limit=CHUNK_SIZE):
        filters = copy(self.filters)
        filters["offset"] = offset
        if not filters.get("limit"):
            filters["limit"] = limit

        response = self.api._get_resource_raw(self.model_class, None, **filters).json()
        if "data" not in response or response["data"] is None:
            return []

        return [
            self.model_class.create(self, **x)
            for x in response["data"]
            if x is not None
        ]


class IntegrationRestfulModelCollection(AuthenticationRestfulModelCollection):
    def __init__(self, api):
        AuthenticationRestfulModelCollection.__init__(self, Integration, api)

    def get(self, provider):
        """
        Get an existing integration for a provider

        Args:
            provider (Authentication.Provider): The provider

        Returns:
            Integration: The existing integration
        """
        return super(IntegrationRestfulModelCollection, self).get(provider.value)

    def delete(self, provider, data=None, **kwargs):
        """
        Deletes an existing integration for a provider

        Args:
            provider (Authentication.Provider): The provider
        """
        super(IntegrationRestfulModelCollection, self).delete(
            provider.value, data=data, **kwargs
        )


class GrantRestfulModelCollection(AuthenticationRestfulModelCollection):
    def __init__(self, api):
        AuthenticationRestfulModelCollection.__init__(self, Grant, api)

    def on_demand_sync(self, grant_id, sync_from=None):
        """
        Trigger a grant sync on demand

        Args:
            grant_id (str): The grant ID to sync
            sync_from (int): Epoch timestamp when the sync starts from

        Returns:
            Grant: The grant after triggering the sync
        """
        path = "sync"
        if sync_from:
            path = path + "?sync_from={}".format(sync_from)
        response = self.api._post_resource(Grant, grant_id, path, data=None)
        return self.model_class.create(self, **response)
