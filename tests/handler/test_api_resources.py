from unittest.mock import patch, Mock

import pytest
from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)

from nylas.handler.http_client import (
    HttpClient,
)
from nylas.models.calendars import Calendar
from nylas.models.response import (
    ListResponse,
    Response,
    DeleteResponse,
    RequestIdOnlyResponse,
)


class MockResource(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    pass


class TestApiResource:
    def test_list_resource(self, http_client_list_response):
        resource = MockResource(http_client_list_response)

        response = resource.list(
            path="/foo",
            response_type=Calendar,
            headers={"test": "header"},
            query_params={"query": "param"},
            request_body={"foo": "bar"},
        )

        assert type(response) is ListResponse
        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/foo",
            {"test": "header"},
            {"query": "param"},
            {"foo": "bar"},
        )

    def test_find_resource(self, http_client_response):
        resource = MockResource(http_client_response)

        response = resource.find(
            path="/foo",
            response_type=Calendar,
            headers={"test": "header"},
            query_params={"query": "param"},
            request_body={"foo": "bar"},
        )

        assert type(response) is Response
        http_client_response._execute.assert_called_once_with(
            "GET",
            "/foo",
            {"test": "header"},
            {"query": "param"},
            {"foo": "bar"},
        )

    def test_create_resource(self, http_client_response):
        resource = MockResource(http_client_response)

        response = resource.create(
            path="/foo",
            response_type=Calendar,
            headers={"test": "header"},
            query_params={"query": "param"},
            request_body={"foo": "bar"},
        )

        assert type(response) is Response
        http_client_response._execute.assert_called_once_with(
            "POST",
            "/foo",
            {"test": "header"},
            {"query": "param"},
            {"foo": "bar"},
        )

    def test_update_resource(self, http_client_response):
        resource = MockResource(http_client_response)

        response = resource.update(
            path="/foo",
            response_type=Calendar,
            headers={"test": "header"},
            query_params={"query": "param"},
            request_body={"foo": "bar"},
        )

        assert type(response) is Response
        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/foo",
            {"test": "header"},
            {"query": "param"},
            {"foo": "bar"},
        )

    def test_destroy_resource(self, http_client_delete_response):
        resource = MockResource(http_client_delete_response)

        response = resource.destroy(
            path="/foo",
            response_type=RequestIdOnlyResponse,
            headers={"test": "header"},
            query_params={"query": "param"},
            request_body={"foo": "bar"},
        )

        assert type(response) is RequestIdOnlyResponse
        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/foo",
            {"test": "header"},
            {"query": "param"},
            {"foo": "bar"},
        )

    def test_destroy_resource_default_type(self, http_client_delete_response):
        resource = MockResource(http_client_delete_response)

        response = resource.destroy(
            path="/foo",
            headers={"test": "header"},
            query_params={"query": "param"},
            request_body={"foo": "bar"},
        )

        assert type(response) is DeleteResponse
        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/foo",
            {"test": "header"},
            {"query": "param"},
            {"foo": "bar"},
        )
