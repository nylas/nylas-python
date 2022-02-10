from nylas.client.delta_models import Delta, Deltas


class DeltaCollection:
    path = "delta"

    def __init__(self, api):
        self.api = api

    def latest_cursor(self):
        """
        Returns the latest delta cursor

        Returns:
            str: The latest cursor

        Raises:
            RuntimeError: If the server returns an object without a cursor
        """
        response = self.api._post_resource(
            Delta, "latest_cursor", None, None, path=self.path
        )
        if "cursor" not in response:
            raise RuntimeError(
                "Unexpected response from the API server. Returned 200 but no 'cursor' string found."
            )

        return response["cursor"]

    def since(self, cursor):
        """
        Get a list of delta cursors since a specified cursor

        Args:
            cursor (str): The first cursor to request from

        Returns:
            Deltas: String for writing directly into an ICS file
        """

        response = self.api._get_resource_raw(
            Delta, None, path=self.path, cursor=cursor
        ).json()
        return Deltas.create(self.api, **response)
