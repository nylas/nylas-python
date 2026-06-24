<div align="center">
  <a href="https://www.nylas.com/">
    <img width="100%" alt="Nylas" src="https://github.com/user-attachments/assets/137517ae-244d-47a5-8ca7-b12984971fc4" />
  </a>

  <h1>Nylas Python SDK</h1>

  <p>
    <strong>The official Python SDK for Nylas — the infrastructure that powers communications</strong>
  </p>

  <p>
    <a href="https://pypi.org/project/nylas/"><img src="https://img.shields.io/pypi/v/nylas" alt="version" /></a>
    <a href="https://codecov.io/gh/nylas/nylas-python"><img src="https://codecov.io/gh/nylas/nylas-python/branch/main/graph/badge.svg?token=HyxGAn5bJR" alt="code coverage" /></a>
    <a href="https://pypi.org/project/nylas/"><img src="https://img.shields.io/pypi/dm/nylas" alt="downloads" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="license" /></a>
  </p>

  <p>
    <a href="https://developer.nylas.com/docs/v3/sdks/python/">📖 SDK Guide</a> ·
    <a href="https://developer.nylas.com/docs/api/v3/">📚 API Reference</a> ·
    <a href="https://dashboard-v3.nylas.com/register">🚀 Sign up</a> ·
    <a href="https://github.com/orgs/nylas-samples/repositories?q=python">💡 Samples</a> ·
    <a href="https://forums.nylas.com">💬 Forum</a>
  </p>
</div>

<br />

The official Python SDK for [Nylas](https://developer.nylas.com/docs/v3/) — the infrastructure that powers communications. Integrate with Gmail, Microsoft, IMAP, Zoom, and 250+ email, calendar, and meeting providers in 5 minutes. Covers [Email](https://developer.nylas.com/docs/v3/email/), [Calendar](https://developer.nylas.com/docs/v3/calendar/), [Contacts](https://developer.nylas.com/docs/v3/email/contacts/), [Scheduler](https://developer.nylas.com/docs/v3/scheduler/), [Notetaker](https://developer.nylas.com/docs/v3/notetaker/), and [Agent Accounts](https://developer.nylas.com/docs/v3/agent-accounts/).

This repository is for contributors and anyone installing the SDK from source. If you just want to use the SDK in your app, head straight to the [**Python SDK guide**](https://developer.nylas.com/docs/v3/sdks/python/) on developer.nylas.com.

## Get started

1. [Sign up for a free Nylas account](https://dashboard-v3.nylas.com/register) and grab your API key from the [Nylas Dashboard](https://dashboard-v3.nylas.com/).
2. Read the [Getting started guide](https://developer.nylas.com/docs/v3/getting-started/) for the core concepts (applications, grants, API keys).
3. Install the SDK and make your first request — see below.

You can also bootstrap from the terminal:

```bash
brew install nylas/nylas-cli/nylas
nylas init
```

More options in the [CLI getting-started guide](https://cli.nylas.com/guides/getting-started).

## ⚙️ Install

> **Requirements:** Python 3.8 or later.

```bash
pip install nylas
```

To install from source:

```bash
git clone https://github.com/nylas/nylas-python.git
cd nylas-python
pip install -e .
```

### Runtime support

Tested on CPython 3.8+. Runs on standard servers as well as serverless platforms like AWS Lambda, Google Cloud Functions, and Vercel — install `nylas` like any other dependency in your deployment package.

## ⚡️ Usage

You access Nylas resources (messages, calendars, events, contacts, …) through an instance of `Client`. Initialize it with your API key — and optionally an `api_uri` matching your [data residency](https://developer.nylas.com/docs/dev-guide/platform/data-residency/).

```python
import os
from nylas import Client

nylas = Client(
    api_key=os.environ["NYLAS_API_KEY"],
    api_uri=os.environ.get("NYLAS_API_URI", "https://api.us.nylas.com"),
    timeout=30,  # optional, in seconds
)
```

Once initialized, use it to make requests against a [grant](https://developer.nylas.com/docs/v3/auth/) (an authenticated end-user account):

```python
calendars, request_id, next_cursor = nylas.calendars.list(
    identifier=os.environ["NYLAS_GRANT_ID"],
)
print(calendars)
```

Resources expose a consistent CRUD surface — `create()`, `find()`, `list()`, `update()`, `destroy()` — plus resource-specific methods (e.g. `messages.send()`, `events.send_rsvp()`). Request and response models are [`dataclasses-json`](https://github.com/lidatong/dataclasses-json) dataclasses, so every payload is fully type-hinted and supports `to_dict()` / `from_dict()`.

### Error handling

The SDK raises typed exceptions you can catch and inspect. Every API error carries a `request_id` and `status_code` — include both when filing a support ticket so we can trace the request end-to-end.

```python
from nylas import Client
from nylas.models.errors import (
    NylasApiError,
    NylasOAuthError,
    NylasSdkTimeoutError,
)

try:
    nylas.calendars.list(identifier=grant_id)
except NylasApiError as err:
    print(err.status_code, err.type, str(err), err.request_id)
except NylasOAuthError as err:
    print(err.error, err.error_code, err.error_description)
except NylasSdkTimeoutError as err:
    print("Timed out:", err.url, err.timeout)
```

Step-by-step walkthroughs in the SDK guide:

- [Send messages](https://developer.nylas.com/docs/v3/sdks/python/send-email/)
- [Read messages and threads](https://developer.nylas.com/docs/v3/sdks/python/read-messages-threads/)
- [Manage events on a calendar](https://developer.nylas.com/docs/v3/sdks/python/manage-events/)
- [Manage contacts](https://developer.nylas.com/docs/v3/sdks/python/manage-contacts/)
- [Manage folders and labels](https://developer.nylas.com/docs/v3/sdks/python/manage-folders-labels/)

### Debugging

To inspect the raw HTTP traffic the SDK sends, turn on `requests`-level logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)
```

## 💡 Examples

Runnable examples live in [`examples/`](examples/) — including [send email](examples/send_email_demo/), [inline attachments](examples/inline_attachment_demo/), [folders](examples/folders_demo/), [import events](examples/import_events_demo/), [Notetaker API](examples/notetaker_api_demo/), [Notetaker calendar](examples/notetaker_calendar_demo/), [message fields](examples/message_fields_demo/), [metadata fields](examples/metadata_field_demo/), [provider errors](examples/provider_error_demo/), [response headers](examples/response_headers_demo/), [`select` parameter](examples/select_param_demo/), [special characters](examples/special_characters_demo/), [hidden folders](examples/include_hidden_folders_demo/), and [plain text](examples/is_plaintext_demo/).

For full sample apps and product quickstarts, browse [**nylas-samples** on GitHub](https://github.com/orgs/nylas-samples/repositories?q=python) — every official SDK has Email, Calendar, Contacts, Scheduler, and Webhooks quickstarts.

## 🤖 AI agents

[nylas/skills](https://github.com/nylas/skills) drops Nylas into Claude Code, Cursor, Codex, and other agents that support the skills format:

```bash
npx skills add nylas/skills
/plugin marketplace add nylas/skills   # Claude Code
```

The CLI also installs an MCP server for Claude Desktop, Claude Code, Cursor, Windsurf, or VS Code:

```bash
brew install nylas/nylas-cli/nylas
nylas mcp install
```

Walkthrough: [give AI agents email access via MCP](https://cli.nylas.com/guides/give-ai-agents-email-access-via-mcp).

## 📚 Reference

- **SDK guide:** [developer.nylas.com/docs/v3/sdks/python](https://developer.nylas.com/docs/v3/sdks/python/)
- **API reference:** [developer.nylas.com/docs/api/v3](https://developer.nylas.com/docs/api/v3/)
- **Python SDK reference:** [nylas-python-sdk-reference.pages.dev](https://nylas-python-sdk-reference.pages.dev/) — generated method/class docs for this SDK
- **Webhooks (notifications):** [developer.nylas.com/docs/v3/notifications](https://developer.nylas.com/docs/v3/notifications/)
- **Auth flows:** [developer.nylas.com/docs/v3/auth](https://developer.nylas.com/docs/v3/auth/)
- **Dev guide & best practices:** [developer.nylas.com/docs/dev-guide](https://developer.nylas.com/docs/dev-guide/)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)

## ✨ Upgrading

See [`CHANGELOG.md`](CHANGELOG.md) for per-release notes. Older upgrade guidance (v5.x → v6.x) lives in [`UPGRADE.md`](UPGRADE.md).

## 💙 Contributing

Issues, ideas, and pull requests welcome — see [Contributing.md](Contributing.md). Before opening a large change, please open an issue or post in the [forum](https://forums.nylas.com) so we can sanity-check the direction.

## 🔒 Security

Found a vulnerability? Please **don't** open a public issue. Report it through our [Vulnerability Disclosure Policy](https://www.nylas.com/security/vulnerability-disclosure-policy/).

## 🔗 Other Nylas SDKs

- [nylas-nodejs](https://github.com/nylas/nylas-nodejs) · `npm install nylas`
- [nylas-ruby](https://github.com/nylas/nylas-ruby) · `gem install nylas`
- [nylas-java](https://github.com/nylas/nylas-java) · Maven / Gradle (Kotlin too)

## 📝 License

MIT — see [LICENSE](LICENSE).
