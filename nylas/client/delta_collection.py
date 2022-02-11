import json

from requests import ReadTimeout

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

    def since(self, cursor, view=None, include_types=None, excluded_types=None):
        """
        Get a list of delta cursors since a specified cursor

        Args:
            cursor (str): The first cursor to request from
            view (str): Value representing if delta expands thread and message objects.
            include_types (list[str] | str): The objects to exclusively include in the returned deltas. Note you cannot set both included and excluded types.
            excluded_types (list[str] | str): The objects to exclude in the returned deltas. Note you cannot set both included and excluded types.

        Returns:
            Deltas: The API response containing the list of deltas

        Raises:
            ValueError: If both include_types and excluded_types are set
        """

        include_types, excluded_types = _validate_types(include_types, excluded_types)
        response = self.api._get_resource_raw(
            Delta,
            None,
            path=self.path,
            cursor=cursor,
            view=view,
            include_types=include_types,
            excluded_types=excluded_types,
        ).json()
        return Deltas.create(self.api, **response)

    def stream(
        self,
        cursor,
        callback=None,
        timeout=None,
        view=None,
        include_types=None,
        excluded_types=None,
    ):
        """
        Stream deltas

        Args:
            cursor (str): The cursor to stream from
            callback: A callable function to invoke on each delta received. No callback is set by default.
            timeout (int): The number of seconds to stream for before timing out. No timeout is set by default.
            view (str): Value representing if delta expands thread and message objects.
            include_types (list[str] | str): The objects to exclusively include in the returned deltas. Note you cannot set both included and excluded types.
            excluded_types (list[str] | str): The objects to exclude in the returned deltas. Note you cannot set both included and excluded types.

        Returns:
            list[Delta]: The list of streamed deltas

        Raises:
            ValueError: If both include_types and excluded_types are set
        """

        deltas = []
        include_types, excluded_types = _validate_types(include_types, excluded_types)
        emit_deltas = False
        if callback and callable(callback):
            emit_deltas = True

        try:
            response = self.api._get_resource_raw(
                Delta,
                "streaming",
                stream=True,
                path=self.path,
                stream_timeout=timeout,
                cursor=cursor,
                view=view,
                include_types=include_types,
                excluded_types=excluded_types,
            )
            for raw_rsp in response.iter_lines():
                if raw_rsp:
                    response_json = json.loads(raw_rsp)
                    delta = Delta.create(self.api, **response_json)
                    deltas.append(delta)
                    if emit_deltas:
                        callback(delta)
        except ReadTimeout:
            pass

        return deltas

    def longpoll(
        self,
        cursor,
        timeout,
        callback=None,
        view=None,
        include_types=None,
        excluded_types=None,
    ):
        """
        Long-poll for deltas

        Args:
            cursor (str): The cursor to poll from
            timeout (int): The number of seconds to poll for before timing out
            callback: A callable function to invoke on each delta received. No callback is set by default.
            view (str): Value representing if delta expands thread and message objects.
            include_types (list[str] | str): The objects to exclusively include in the returned deltas. Note you cannot set both included and excluded types.
            excluded_types (list[str] | str): The objects to exclude in the returned deltas. Note you cannot set both included and excluded types.

        Returns:
            Deltas: The API response containing the list of deltas

        Raises:
            ValueError: If both include_types and excluded_types are set
        """

        delta = {}
        include_types, excluded_types = _validate_types(include_types, excluded_types)
        emit_deltas = False
        if callback and callable(callback):
            emit_deltas = True

        buffer = bytearray()
        response = self.api._get_resource_raw(
            Delta,
            "longpoll",
            stream=True,
            path=self.path,
            timeout=timeout,
            cursor=cursor,
            view=view,
            include_types=include_types,
            excluded_types=excluded_types,
        )
        for raw_rsp in response.iter_lines():
            if raw_rsp:
                buffer.extend(raw_rsp)
                try:
                    buffer_json = json.loads(buffer.decode())
                    delta = Deltas.create(self.api, **buffer_json)
                    if emit_deltas:
                        callback(delta)
                except ValueError:
                    continue

        return delta


# Helper functions for validating type inputs
def _validate_types(include_types, excluded_types):
    if include_types and excluded_types:
        raise ValueError("You cannot set both include_types and excluded_types")

    return _join_types(include_types), _join_types(excluded_types)


def _join_types(types):
    if types:
        if isinstance(types, str):
            return types
        try:
            return ",".join(types)
        except TypeError:
            return None
