# Upgrading to the Nylas Python SDK v6.0

## Introduction

The Nylas Python SDK has been rewritten for the upcoming release of the Nylas API v3 to be more idiomatic and easier to use. This guide helps you upgrade your code to use the new SDK. The new SDK also includes [documentation for the SDK's functions and models,](https://nylas-python-sdk-reference.pages.dev/) so you can easily find the implementation details you need.

## Initial Setup

To upgrade to the new SDK, you update your dependencies to use the new version. Do this by installing the new version of the SDK using pip.

**Note:** The minimum Python version is now the lowest supported LTS, Python v3.8.

```bash
pip install nylas --pre
```

The first step to using the new SDK is to initialize a new instance of the Nylas SDK. Do this by passing in your API key to the constructor. The entry point of the SDK has changed to `Client`.

```python
from nylas import Client

nylas = Client(
    api_key="API_KEY",
)
```

From here, you can use the Nylas  `Client` instance to make API requests by accessing the different resources configured with your API Key.

## Models

Models in the Python SDK have completely changed in this new version. First, new Python SDK now includes a specific model for each request and response to/from the Nylas API. Let's take a Nylas calendar object for example. In the previous SDK version there was only one `Calendar` object, and it simultaneously represented a Calendar that:

- Is to be created
- Is to be updated
- Or is to be retrieved

This meant that the models like the `Calendar` model had to be configured with _all_ the possible fields that could ever be used in any of the above scenarios. This made object very large and hard to anticipate as a developer. The new Node SDK has split the `Calendar` model into three models, one for each of the scenarios above.

- `Calendar` (for retrieving a calendar)
- `CreateCalenderRequest` (for creating a calendar)
- `UpdateCalendarRequest` (for updating a calendar)

Furthermore, with the Python SDK dropping support for Python versions < 3.8, our models now take advantage of some new Python features. For the models that represent response objects, we are now utilizing [dataclasses](https://docs.python.org/3/library/dataclasses.html) to make the models more readable, easier to use, and provide some type hinting and in-IDE hinting as well. For response objects they also implement [dataclass-json](https://pypi.org/project/dataclasses-json/) which provides utility functions such as `to_dict()` and `to_json()` to allow you to utilize data in a variety of different formats.

For the models that represent request objects, we are now utilizing [TypedDicts](https://docs.python.org/3/library/typing.html#typing.TypedDict) to provide a guided but seamless experience to building objects for outgoing requests. Both sets of classes are all fully typed as well, ensuring that you have all the information you need to make a successful request.

## Making Requests to the Nylas API

You use the `Nylas` instance you configured earlier to make requests to the Nylas API. The SDK is organized into different resources corresponding to each of the different APIs provided by Nylas and each resource includes all the available methods to make requests to that API.

For example, to get a list of calendars, you can do so like:

```python
from nylas import Client

nylas = Client(
    api_key="API_KEY",
)

response = nylas.calendars.list(identifier="GRANT_ID")
```

This may look very similar to how the previous version of the Python SDK worked, but there are some key concepts which we will cover.

### Response Objects

The new Nylas API v3 now has standard response objects for all requests (excluding OAuth endpoints). There are generally two main types of response objects: `Response` and `ListResponse`.

The `Response` object is used for requests that return a single object, such as retrieving a single calendar. This returns a parameterized object of the type you are requesting (for example `Calendar`), and a string that represents the request ID.

The `ListResponse` object is used for requests that return a list of objects, such as retrieving a _list_ of calendars. This returns a list of parameterized objects of the type you are requesting (for example, `Calendar`), a string representing the request ID, and another string representing the token of the next page for paginating a request.

For both classes they also support destructuring, so you can do something like:

```python
from nylas import Client

nylas = Client(
    api_key="API_KEY",
)

response = nylas.calendars.list(identifier="GRANT_ID")
calendars = response.data # The list of calendars

# Or

calendars, request_id = nylas.calendars.list(identifier="CALENDAR_ID") # The list of calendars and the request ID
```

### Pagination

The new Nylas API v3 now uses a different way to paginate by returning a `next_cursor` field in a `ListResponse` object pointing to the next page, if one exists. Currently the Python SDK does not support pagination out of the box, but this is something we are looking to add in the future. To paginate a request, you can use the `next_cursor` field to make a request to the next page:

```python
from nylas import Client

nylas = Client(
    api_key="API_KEY",
)

response = nylas.calendars.list(identifier="GRANT_ID")
all_calendars = list(response)

while response.next_cursor:
    response = nylas.calendars.list(identifier="GRANT_ID", query_params={"page_token": response.next_cursor})
    all_calendars.extend(response)
```

### Error Objects

Like the response objects, Nylas v3 now has standard error objects for all requests (excluding OAuth endpoints). There are two superclass error classes, `AbstractNylasApiError`, used for errors returned by the API, and `AbstractNylasSdkError`, used for errors returned by the SDK.

The `AbstractNylasApiError` includes two subclasses: `NylasOAuthError`, used for API errors that are returned from the OAuth endpoints, and `NylasApiError`, used for any other Nylas API errors.

The SDK extracts the error details from the response and stores them in the error object, along with the request ID and the HTTP status code.

`AbstractNylasSdkError` is used for errors returned by the SDK. Right now there's only one type of error we return, and that's a `NylasSdkTimeoutError` which is thrown when a request times out.

## Authentication

The SDK's authentication methods reflect [the methods available in the new Nylas API v3](https://developer.nylas.com/docs/developer-guide/v3-authentication/). While you can only create and manage your application's connectors (formerly called integrations) in the dashboard, you can manage almost everything else directly from the SDK. This includes managing grants, redirect URIs, OAuth tokens, and authenticating your users.

There are two main methods to focus on when authenticating users to your application. The first is the `Auth#url_for_oath2` method, which returns the URL that you should redirect your users to in order to authenticate them using Nylas' OAuth 2.0 implementation.

The second is the `Auth#exchange_code_for_token` method. Use this method to exchange the code Nylas returned from the authentication redirect for an access token from the OAuth provider. Nylas's response to this request includes both the access token, and information about the grant that was created.  You don't _need_ to use the `grant_id` to make requests. Instead, you can use the authenticated email address directly as the identifier for the account. If you prefer to use the `grant_id`, you can extract it from the `CodeExchangeResponse` object and use that instead.

The following code shows how to authenticate a user into a Nylas application:

```python
from nylas import Client

nylas = Client(
    api_key="API_KEY",
)

# Build the URL for authentication
auth_url = nylas.auth.url_for_oauth2({
    "client_id": "CLIENT_ID",
    "redirect_uri": "abc",
    "login_hint": "example@email.com"
})

# Write code here to redirect the user to the url and parse the code
...

# Exchange the code for an access token

code_exchange_response = nylas.auth.exchange_code_for_token({
    "client_id": "CLIENT_ID",
    "client_secret": "CLIENT_SECRET",
    "code": "CODE",
    "redirect_uri": "abc"
})

# Now you can either use the email address that was authenticated or the grant ID in the response as the identifier

response_with_email = nylas.calendars.list(identifier="example@email.com")

# Or

response_with_grant = nylas.calendars.list(identifier=code_exchange_response.grant_id)
```
