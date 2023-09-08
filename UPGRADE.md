# Upgrade to the Nylas Python SDK v6.0

The Nylas Python SDK has been rewritten to prepare for the upcoming release of the Nylas API v3. The changes make the SDK more idiomatic and easier to use. We've also included [function and model documentation](https://nylas-python-sdk-reference.pages.dev/), so you can easily find the implementation details that you need.

This guide will help you upgrade your environment to use the new SDK.

## Initial setup

To upgrade to the new Python SDK, you must update your dependencies to use the new version. You can do this by installing the newest version of the SDK using pip:

```bash
pip install nylas --pre
```

**Note**: The minimum Python version is now the lowest supported LTS: Python v3.8.

The first step to using the new SDK is to initialize a new `nylas` instance. You can do this by passing your API key to the constructor:

```python
from nylas import Client

nylas = Client(
    api_key="API_KEY",
)
```

Note that the SDK's entry point has changed to `Client`.

From here, you can use the Nylas `Client` instance to make API requests by accessing the different resources configured with your API key.

## Models

Models have completely changed in the new version of the Nylas Python SDK. First, the SDK now includes a specific model for each request and response to/from the Nylas API. Let's take a Calendar object, for example. In the previous version of the SDK, there was only one `Calendar` object representing a Calendar in three states:

- It is to be created.
- It is to be updated.
- It is to be retrieved.

This meant that all models had to be configured with _all_ possible fields that could be used in any of these scenarios, making the object very large and difficult to anticipate as a developer.

The new SDK has split the `Calendar` model into three separate models, one for each of the previous scenarios:

- `Calendar`: Retrieve a Calendar.
- `CreateCalendarRequest`: Create a Calendar.
- `UpdateCalendarRequest`: Update a Calendar.

Because the new version of the SDK drops support for Python versions lower than v3.8, our models now take advantage of some new Python features. For the models that represent response objects, we now use [dataclasses](https://docs.python.org/3/library/dataclasses.html) to make them more readable, easier to use, and to provide some type hinting and in-IDE hinting. Response objects also implement [the `dataclasses-json` library](https://pypi.org/project/dataclasses-json/), which provides utility functions such as `to_dict()` and `to_json()` that allow you to use your data in a variety of formats.

For models that represent request objects, we're using [TypedDicts](https://docs.python.org/3/library/typing.html#typing.TypedDict) to provide a seamless guided experience to building objects for outgoing requests. Both sets of classes are fully typed as well, ensuring that you have all the information you need to make a successful API request.

## Make requests to the Nylas API

To make requests to the Nylas API, you use the `nylas` instance that you configured earlier.

The Python SDK is organized into different resources corresponding to each of the Nylas APIs. Each resource includes all of the available methods to make requests to its respective API. For example, you can use this code to get a list of Calendars:

```python
from nylas import Client

nylas = Client(
    api_key="API_KEY",
)

response = nylas.calendars.list(identifier="GRANT_ID")
```

This may look very similar to how you would get a list of Calendars in previous versions of the SDK, but there are some key differences that we'll cover in the following sections.

### Response objects

The Nylas API v3 has standard response objects for all requests, with the exception of OAuth endpoints. There are generally two main types of response objects:

- `Response`: Used for requests that return a single object, such as requests to retrieve a single Calendar. This returns a parameterized object of the type that you requested (for example, `Calendar`) and a string representing the request ID.
- `ListResponse`: Used for requests that return a list of objects, such as requests to retrieve a _list_ of Calendars. This returns a list of parameterized objects of the type that you requested (for example, `Calendar`), a string representing the request ID, and a string representing the token of the next page for paginating the request.

Both classes also support destructuring. This means you can use code like this to manipulate the data:

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

The Nylas API v3 uses a new way to paginate responses by returning a `next_cursor` parameter in `ListResponse` objects. The `next_cursor` points to the next page, if one exists.

Currently, the Nylas Python SDK doesn't support pagination out of the box, but this is something we're looking to add in the future. Instead, you can use `next_cursor` to make a request to the next page:

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

### Error objects

Similar to response objects, the Nylas API v3 has standard error objects for all requests, with the exception of OAuth endpoints. There are two superclass error classes:

- `AbstractNylasApiError`: Used for errors returned by the Nylas API.
- `AbstractNylasSdkError`: Used for errors returned by the Python SDK.

The `AbstractNylasApiError` superclass includes two subclasses:

- `NylasOAuthError`: Used for Nylas API errors returned from OAuth endpoints.
- `NylasApiError`: Used for all other Nylas API errors.

The Python SDK extracts error details from the response and stores them in the error object, along with the request ID and HTTP status code.

Currently, there is only one type of `AbstractNylasSdkError` that we return: the `NylasSdkTimeoutError`, which is thrown when a request times out.

## Authentication

The Nylas Python SDK's authentication methods reflect [those available in the Nylas API v3](https://developer.nylas.com/docs/developer-guide/v3-authentication/).

While you can only create and manage your application's connectors (formerly called "integrations") in the Dashboard, you can manage almost everything else directly from the Python SDK. This includes managing Grants, redirect URIs, OAuth tokens, and authenticating your users.

There are two main methods to focus on when authenticating users to your app:

- `Auth#url_for_oath2`: Returns the URL that you should direct your users to in order to authenticate them with OAuth 2.0.
- `Auth#exchange_code_for_token`: Exchanges the code Nylas returns from the authentication redirect for an access token from the OAuth provider. Nylas' response to this request returns both the access token and information about the new Grant.

Note that you don't need to use the `grant_id` to make requests. Instead, you can use the authenticated email address associated with the Grant as the identifier. If you prefer to use the `grant_id`, you can extract it from the `CodeExchangeResponse`.

This code demonstrates how to authenticate a user into a Nylas app:

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
