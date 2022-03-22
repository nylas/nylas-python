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
        "id"
    )
    read_only_attrs = {"provider", "id"}
    auth_method = AuthMethod.BASIC_CLIENT_ID_AND_SECRET
    collection_name = "connect/integrations"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Integration, api)
        self.settings = {}
        self.scope = []

    def set_client_id(self, client_id):
        self.settings["client_id"] = client_id

    def set_client_secret(self, client_secret):
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
            if isinstance(self.provider, Integration.Provider):
                dct["provider"] = self.provider.value
            else:
                dct["provider"] = self.provider

        return dct

    def _update_resource(self, **kwargs):
        provider = self.id or self.provider
        return self.api._patch_resource(
            self.cls, provider, self.as_json(), **kwargs
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


class IntegrationRestfulModelCollection(RestfulModelCollection):
    def __init__(self, api):
        self._app_name = "beta"
        self._region = Integration.Region.US
        # Make a copy of the API as we need to change the base url for Integration calls
        integration_api = copy(api)
        RestfulModelCollection.__init__(self, Integration, integration_api)
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

    def get(self, provider):
        """
        Get an existing integration for a provider

        Args:
            provider (Integration.Provider): The provider

        Returns:
            Integration: The existing integration
        """
        return super(IntegrationRestfulModelCollection, self).get(provider.value)

    def delete(self, provider, data=None, **kwargs):
        """
        Deletes an existing integration for a provider

        Args:
            provider (Integration.Provider): The provider
        """
        super(IntegrationRestfulModelCollection, self).delete(provider.value, data=data, **kwargs)

    def _get_model_collection(self, offset=0, limit=CHUNK_SIZE):
        filters = copy(self.filters)
        filters["offset"] = offset
        if not filters.get("limit"):
            filters["limit"] = limit

        response = self.api._get_resource_raw(self.model_class, None, **filters).json()
        if "data" not in response or response["data"] is None:
            return []

        return [self.model_class.create(self, **x) for x in response["data"] if x is not None]

    def _set_integrations_api_url(self):
        self.api.api_server = "https://{app_name}.{region}.nylas.com".format(app_name=self.app_name, region=self.region.value)
