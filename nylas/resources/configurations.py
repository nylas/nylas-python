from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    CreatableApiResource,
    DestroyableApiResource,
    FindableApiResource,
    ListableApiResource,
    UpdatableApiResource,
)
from nylas.models.list_query_params import ListQueryParams
from nylas.models.response import DeleteResponse, ListResponse, Response
from nylas.models.scheduler import (
    Configuration,
    CreateConfigurationRequest,
    UpdateConfigurationRequest,
)


class ListConfigurationsParams(ListQueryParams):
    """
    Interface of the query parameters for listing configurations.

    Attributes:
            limit: The maximum number of objects to return.
                    This field defaults to 50. The maximum allowed value is 200.
            page_token: An identifier that specifies which page of data to return.
                    This value should be taken from a ListResponse object's next_cursor parameter.
            identifier: The identifier of the Grant to act upon.
    """

    identifier: str


class Configurations(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Configuration API

    The Nylas configuration API allows you to create new configurations or manage existing ones, as well as getting
    configurations details for a user.

    Nylas Scheduler stores Configuration objects in the Scheduler database and loads
                them as Scheduling Pages in the Scheduler UI.
    """

    def list(
        self,
        identifier: str,
        query_params: ListConfigurationsParams = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Configuration]:
        """
        Return all Configurations.

        Args:
                identifier: The identifier of the Grant to act upon.
                overrides: The request overrides to use for the request.

        Returns:
                The list of Configurations.
        """
        # import pdb; pdb.set_trace();
        res = super().list(
            path=f"/v3/grants/{identifier}/scheduling/configurations",
            overrides=overrides,
            response_type=Configuration,
            query_params=query_params,
        )
        return res

    def find(
        self, identifier: str, config_id: str, overrides: RequestOverrides = None
    ) -> Response[Configuration]:
        """
        Return a Configuration.

        Args:
                identifier: The identifier of the Grant to act upon.
                config_id: The identifier of the Configuration to get.
                overrides: The request overrides to use for the request.

        Returns:
                The Configuration object.
        """
        return super().find(
            path=f"/v3/grants/{identifier}/scheduling/configurations/{config_id}",
            overrides=overrides,
            response_type=Configuration,
        )

    def create(
        self,
        identifier: str,
        request_body: CreateConfigurationRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Configuration]:
        """
        Create a new Configuration.

        Args:
                identifier: The identifier of the Grant to act upon.
                data: The data to create the Configuration with.
                overrides: The request overrides to use for the request.

        Returns:
                The Configuration object.
        """
        return super().create(
            path=f"/v3/grants/{identifier}/scheduling/configurations",
            request_body=request_body,
            overrides=overrides,
            response_type=Configuration,
        )

    def update(
        self,
        identifier: str,
        config_id: str,
        request_body: UpdateConfigurationRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Configuration]:
        """
        Update a Configuration.

        Args:
                identifier: The identifier of the Grant to act upon.
                config_id: The identifier of the Configuration to update.
                data: The data to update the Configuration with.
                overrides: The request overrides to use for the request.

        Returns:
                The Configuration object.
        """
        return super().update(
            path=f"/v3/grants/{identifier}/scheduling/configurations/{config_id}",
            request_body=request_body,
            overrides=overrides,
            response_type=Configuration,
        )

    def destroy(
        self, identifier: str, config_id: str, overrides: RequestOverrides = None
    ) -> DeleteResponse:
        """
        Delete a Configuration.

        Args:
                identifier: The identifier of the Grant to act upon.
                config_id: The identifier of the Configuration to delete.
                overrides: The request overrides to use for the request.
        """
        return super().destroy(
            path=f"/v3/grants/{identifier}/scheduling/configurations/{config_id}",
            overrides=overrides,
        )
