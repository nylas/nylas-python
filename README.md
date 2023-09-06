<a href="https://www.nylas.com/">
    <img src="https://brand.nylas.com/assets/downloads/logo_horizontal_png/Nylas-Logo-Horizontal-Blue_.png" alt="Aimeos logo" title="Aimeos" align="right" height="60" />
</a>

# Nylas Python SDK

![PyPI - Version](https://img.shields.io/pypi/v/nylas)
[![codecov](https://codecov.io/gh/nylas/nylas-python/branch/main/graph/badge.svg?token=HyxGAn5bJR)](https://codecov.io/gh/nylas/nylas-python)

This is the GitHub repository for the Nylas Python SDK and this repo is primarily for anyone who wants to make contributions to the SDK or install it from source. If you are looking to use Python to access the Nylas Email, Calendar, or Contacts API you should refer to our official [Python SDK Quickstart Guide](https://docs.nylas.com/docs/quickstart-python).

The Nylas Communications Platform provides REST APIs for [Email](https://docs.nylas.com/docs/quickstart-email), [Calendar](https://docs.nylas.com/docs/quickstart-calendar), and [Contacts](https://docs.nylas.com/docs/quickstart-contacts), and the Python SDK is the quickest way to build your integration using Python.

Here are some resources to help you get started:

- [Sign up for your free Nylas account](https://dashboard.nylas.com/register)
- [Nylas API v3 Quickstart Guide](https://developer.nylas.com/docs/v3-beta/v3-quickstart/)
- [Nylas SDK Reference](https://nylas-python-sdk-reference.pages.dev/)
- [Nylas API Reference](https://developer.nylas.com/docs/api/)
- [Nylas Samples repo for code samples and example applications](https://github.com/orgs/nylas-samples/repositories?q=&type=all&language=python)

If you have a question about the Nylas Communications Platform, please reach out to support@nylas.com to get help.

## ⚙️ Install

The Nylas Python SDK is available via pip:

```bash
pip install nylas --pre
```

To install the SDK from source, clone this repo and run the install script.

```bash
git clone https://github.com/nylas/nylas-python.git && cd nylas-python
python setup.py install
```

## ⚡️ Usage

To use this SDK, you must first [get a free Nylas account](https://dashboard.nylas.com/register).

Then, follow the Quickstart guide to [set up your first app and get your API keys](https://developer.nylas.com/docs/v3-beta/v3-quickstart/).

For code examples that demonstrate how to use this SDK, take a look at our [Python repos in the Nylas Samples collection](https://github.com/orgs/nylas-samples/repositories?q=&type=all&language=python).

### 🚀 Making Your First Request

You use the `Client` class from the `nylas` package, to make requests to the Nylas API. The SDK is organized into different resources, each of which has methods to make requests to the API. Each resource is available through the `Client` object configured with your API key.

For example, to get a list of calendars, you can use the following code:


```python
from nylas import Client

nylas = Client(
    api_key="API_KEY",
)

calendars = nylas.calendars.list("GRANT_ID")
```

## 📚 Documentation

Nylas maintains a [reference guide for the Python SDK](https://nylas-python-sdk-reference.pages.dev/) to help you get familiar with the available functions and classes.

## ✨ Upgrading from 1.x

See [UPGRADE.md](UPGRADING.md) for instructions on upgrading from 5.x to 6.x.

## 💙 Contributing

Please refer to [Contributing](Contributing.md) for information about how to make contributions to this project. We welcome questions, bug reports, and pull requests.

## 📝 License

This project is licensed under the terms of the MIT license. Please refer to [LICENSE](LICENSE) for the full terms.
