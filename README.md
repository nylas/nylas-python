<a href="https://www.nylas.com/">
    <img src="https://brand.nylas.com/assets/downloads/logo_horizontal_png/Nylas-Logo-Horizontal-Blue_.png" alt="Aimeos logo" title="Aimeos" align="right" height="60" />
</a>

# Nylas Python SDK

[![PyPI - Version](https://img.shields.io/pypi/v/nylas)](https://pypi.org/project/nylas/)
[![codecov](https://codecov.io/gh/nylas/nylas-python/branch/main/graph/badge.svg?token=HyxGAn5bJR)](https://codecov.io/gh/nylas/nylas-python)

This is the GitHub repository for the Nylas Python SDK. The repo is primarily for anyone who wants to install the SDK from source or make contributions to it.

If you're looking to use Python to access the Nylas Email, Calendar, or Contacts APIs, see our [Python SDK Quickstart guide](https://docs.nylas.com/docs/quickstart-python).

The Nylas platform provides REST APIs for [Email](https://docs.nylas.com/docs/quickstart-email), [Calendar](https://docs.nylas.com/docs/quickstart-calendar), and [Contacts](https://docs.nylas.com/docs/quickstart-contacts), and the Python SDK is the quickest way to build your integration using Python.

Here are some resources to help you get started:

- [Sign up for a free Nylas account](https://dashboard.nylas.com/register).
- Follow the [Nylas API v3 Quickstart guide](https://developer.nylas.com/docs/v3-beta/v3-quickstart/).
- Browse the [Nylas SDK reference docs](https://nylas-python-sdk-reference.pages.dev/).
- Browse the [Nylas API reference docs](https://developer.nylas.com/docs/api/).
- See our code samples in the [Nylas Samples repo](https://github.com/orgs/nylas-samples/repositories?q=&type=all&language=python).

If you have any questions about the Nylas platform, please reach out to support@nylas.com.

## ⚙️ Install

The Nylas Python SDK is available via pip:

```bash
pip install nylas --pre
```

To install the SDK from source, clone this repo and run the install script:

```bash
git clone https://github.com/nylas/nylas-python.git && cd nylas-python
python setup.py install
```

## ⚡️ Usage

Before you use the Nylas Python SDK, you must first [create a Nylas account](https://dashboard.nylas.com/register). Then, follow our [API v3 Quickstart guide](https://developer.nylas.com/docs/v3-beta/v3-quickstart/) to set up your first app and get your API keys.

For code samples and example applications, take a look at our [Python repos in the Nylas Samples collection](https://github.com/orgs/nylas-samples/repositories?q=&type=all&language=python).

### 🚀 Make your first request

After you've installed and set up the Nylas Python SDK, you can make your first API request. To do so, use the `Client` class from the `nylas` package.

The SDK is organized into different resources, each of which has methods to make requests to the Nylas API. Each resource is available through the `Client` object that you configured with your API key. For example, you can use this code to get a list of Calendars:

```python
from nylas import Client

nylas = Client(
    api_key="API_KEY",
)

calendars, request_id, next_cursor = nylas.calendars.list("GRANT_ID")

event, request_id = nylas.events.create(
    identifier="GRANT_ID",
    request_body={
        "title": "test title",
        "description": "test description",
        "when": {
            "start_time": start_unix_timestamp,
            "end_time": end_unix_timestamp,
        }
    },
    query_params={"calendar_id": "primary", "notify_participants": True},
    )
)

event, request_id = nylas.events.find(
    identifier="GRANT_ID",
    event_id=event.id,
    query_params={
        "calendar_id": "primary",
    },
)

nylas.events.destroy("GRANT_ID", event.id, {"calendar_id": "primary"})

```

## 📚 Documentation

This SDK makes heavy use of [Python 3 dataclasses](https://realpython.com/python-data-classes/) to define the REST resources and request/response schemas of the Nylas APIs. The Client object is a wrapper around all of these resources and is used to interact with the corresponding APIs. Basic CRUD operations are handled by the `create()`, `find()`, `list()`, `update()`, and `destroy()` methods on each resource. Resources may also have other methods which are all detailed in the [reference guide for the Python SDK](https://nylas-python-sdk-reference.pages.dev/). In the code reference, start at `client`, and then `resources` will give more info on available API call methods. `models` is the place to find schemas for requests, responses, and all Nylas object types.

While most resources are accessed via the top-level Client object, note that `auth` contains the sub-resource `grants` as well as a collection of other auth-related API calls.

You'll want to catch `nylas.models.errors.NylasAPIError` to handle errors.

Have fun!!

## ✨ Upgrade from v5.x

See [UPGRADE.md](UPGRADE.md) for instructions on upgrading from v5.x to v6.x.

## 💙 Contribute

Please refer to [Contributing](Contributing.md) for information about how to make contributions to this project. We welcome questions, bug reports, and pull requests.

## 🛠️  Debugging

It can sometimes be helpful to turn on request logging during development. Adding the following snippet to your code that calls the SDK should get you sorted:

```
import logging
import requests

# Set up logging to print out HTTP request information
logging.basicConfig(level=logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
```

## 📝 License

This project is licensed under the terms of the MIT license. Please refer to [LICENSE](LICENSE) for the full terms.
