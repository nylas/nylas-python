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

calendars = nylas.calendars.list("GRANT_ID")
```

## 📚 Documentation

Nylas maintains a [reference guide for the Python SDK](https://nylas-python-sdk-reference.pages.dev/) to help you get familiar with the available functions and classes.

## ✨ Upgrade from v5.x

See [UPGRADE.md](UPGRADE.md) for instructions on upgrading from v5.x to v6.x.

## 💙 Contribute

Please refer to [Contributing](Contributing.md) for information about how to make contributions to this project. We welcome questions, bug reports, and pull requests.

## 📝 License

This project is licensed under the terms of the MIT license. Please refer to [LICENSE](LICENSE) for the full terms.
