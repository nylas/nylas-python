# Contribute to Nylas
👍🎉 First off, thanks for taking the time to contribute! 🎉👍

The following is a set of guidelines for contributing to the Nylas Python SDK; these are guidelines, not rules, so please use your best judgement and feel free to propose changes to this document via pull request.

# Development Setup

To get started contributing to this repository, you'll need to set up a local development environment. Follow these steps:

## Prerequisites

- Python 3.8 or higher (the project supports Python 3.8+)
- Git
- A GitHub account

## Setup Steps

### 1. Fork and Clone the Repository

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/nylas-python.git
cd nylas-python

# Add the upstream repository as a remote
git remote add upstream https://github.com/nylas/nylas-python.git
```

### 2. Set Up Python Virtual Environment

We recommend using a virtual environment to isolate your development dependencies:

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate
```

### 3. Install Development Dependencies

Install the package in editable mode with all optional dependencies:

```bash
# Install the package in development mode with all optional dependencies
pip install -e ".[test,docs,release]"

# Or install specific dependency groups as needed:
# pip install -e ".[test]"     # For running tests
# pip install -e ".[docs]"     # For building documentation
# pip install -e ".[release]"  # For release management
```

### 4. Install Code Quality Tools

Install the linting and formatting tools used by the project:

```bash
pip install pylint black
```

### 5. Verify Your Setup

Run the tests to make sure everything is working correctly:

```bash
# Run the test suite
python setup.py test

# Or run tests with pytest directly
pytest

# Run with coverage
pytest --cov=nylas tests/
```

Check code formatting and linting:

```bash
# Check code formatting (this will modify files)
black .

# Run linting
pylint nylas
```

## Development Workflow

1. **Create a branch** for your feature or bug fix:
   ```bash
   git checkout -b your-feature-branch
   ```

2. **Make your changes** and write tests for any new functionality

3. **Run tests and linting**:
   ```bash
   python setup.py test
   black .
   pylint nylas
   ```

4. **Commit your changes** following [conventional commit practices](https://www.conventionalcommits.org/)

5. **Push to your fork** and create a pull request

## Project Structure

- `nylas/` - Main SDK source code
- `tests/` - Test files
- `examples/` - Example usage scripts
- `scripts/` - Build and development scripts
- `pyproject.toml` - Project configuration and dependencies
- `setup.py` - Legacy setup file (still used for some operations)

## Running Tests

The project uses pytest for testing:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=nylas tests/

# Run specific test files
pytest tests/test_specific_module.py

# Run tests matching a pattern
pytest -k "test_pattern"
```

## Documentation

To build the documentation locally:

```bash
# Make sure you have docs dependencies installed
pip install -e ".[docs]"

# Generate documentation (if there are scripts for this)
python scripts/generate-docs.py
```

# How to Ask a Question

If you have a question about how to use the Python SDK, please [create an issue](https://github.com/nylas/nylas-python/issues) and label it as a question. If you have more general questions about the Nylas Communications Platform, or the Nylas Email, Calendar, and Contacts API, please reach out to support@nylas.com to get help.

# How To Contribute
## Report a Bug or Request a Feature

If you encounter any bugs while using this software, or want to request a new feature or enhancement, please [create an issue](https://github.com/nylas/nylas-python/issues) to report it, and make sure you add a label to indicate what type of issue it is.

## Contribute Code

Pull requests are welcome for bug fixes. If you want to implement something new, [please request a feature](https://github.com/nylas/nylas-python/issues) first so we can discuss it.

While writing your code contribution, make sure you follow the testing conventions found in the [tests directory](https://github.com/nylas/nylas-python/tree/main/tests) for any components that you add. We use [codecov](https://codecov.io/gh/nylas/nylas-python) to test coverage, please ensure that your contributions don’t cause a decrease to test coverage.

## Creating a Pull Request

Please follow [best practices](https://github.com/trein/dev-best-practices/wiki/Git-Commit-Best-Practices) for creating git commits. When your code is ready to be submitted, you can [submit a pull request](https://help.github.com/articles/creating-a-pull-request/) to begin the code review process.

All PRs from contributors that aren't employed by Nylas must contain the following text in the PR description: "I confirm that this contribution is made under the terms of the MIT license and that I have the authority necessary to make this contribution on behalf of its copyright owner."
