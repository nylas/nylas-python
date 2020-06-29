# Nylas Python SDK ![Build Status](https://github.com/nylas/nylas-python/workflows/Test/badge.svg) [![Code Coverage](https://codecov.io/gh/nylas/nylas-python/branch/main/graph/badge.svg)](https://codecov.io/gh/nylas/nylas-python)

This is the GitHub repository for the Nylas Python SDK and this repo is primarily for anyone who wants to make contributions to the SDK or install it from source. If you are looking to use Python to access the Nylas Email, Calendar, or Contacts API you should refer to our official [Python SDK Quickstart Guide](https://docs.nylas.com/docs/quickstart-python).

The Nylas Communications Platform provides REST APIs for [Email](https://docs.nylas.com/docs/quickstart-email), [Calendar](https://docs.nylas.com/docs/quickstart-calendar), and [Contacts](https://docs.nylas.com/docs/quickstart-contacts), and the Python SDK is the quickest way to build your integration using Python

Here are some resources to help you get started:

- [Nylas SDK Tutorials](https://docs.nylas.com/docs/tutorials)
- [Get Started with the Nylas Communications Platform](https://docs.nylas.com/docs/getting-started)
- [Sign up for your Nylas developer account.](https://nylas.com/register)
- [Nylas API Reference](https://docs.nylas.com/reference)

If you have a question about the Nylas Communications Platform, please reach out to support@nylas.com to get help.

# Install

The Nylas Python SDK is available via pip:

`pip install nylas`

To install the SDK from source, clone this repo and run the install script.

    git clone https://github.com/nylas/nylas-python.git && cd nylas-python
    python setup.py install

# Usage

To use this SDK, you first need to [sign up for a free Nylas developer account](https://nylas.com/register).

Then, follow our guide to [setup your first app and get your API access keys](https://docs.nylas.com/docs/get-your-developer-api-keys).

Next, in your python script, import the `APIClient` class from the `nylas` package, and create a new instance of this class, passing the variables you gathered when you got your developer API keys. In the following example, replace `CLIENT_ID`, `CLIENT_SECRET`, and `ACCESS_TOKEN` with your values.


    from nylas import APIClient

    nylas = APIClient(
        CLIENT_ID,
        CLIENT_SECRET,
        ACCESS_TOKEN
    )

Now, you can use `nylas` to access full email, calendar, and contacts functionality. For example, here is how you would print the subject line for the most recent email message to the console.


    message = nylas.messages.first()
    print(message.subject)

To learn more about how to use the Nylas Python SDK, please refer to our [Python SDK QuickStart Guide](https://docs.nylas.com/docs/quickstart-python) and our [Python tutorials](https://docs.nylas.com/docs/tutorials).

# Contributing

Please refer to [Contributing](Contributing.md) for information about how to make contributions to this project. We welcome questions, bug reports, and pull requests.

# License

This project is licensed under the terms of the MIT license. Please refer to [LICENSE](LICENSE) for the full terms.
