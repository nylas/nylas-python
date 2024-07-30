import os
import shutil
import sys
import re
import subprocess
from setuptools import setup, find_packages, Command


VERSION = ""
with open("nylas/_client_sdk_version.py", "r") as fd:
    VERSION = re.search(
        r'^__VERSION__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

RUN_DEPENDENCIES = [
    "requests[security]>=2.31.0",
    "requests-toolbelt>=1.0.0",
    "dataclasses-json>=0.5.9",
    "typing_extensions>=4.7.1",
]

TEST_DEPENDENCIES = ["pytest>=7.4.0", "pytest-cov>=4.1.0", "setuptools>=69.0.3"]

DOCS_DEPENDENCIES = [
    "mkdocs>=1.5.2",
    "mkdocstrings[python]>=0.22.0",
    "mkdocs-material>=9.2.6",
    "mkdocs-gen-files>=0.5.0",
    "mkdocs-literate-nav>=0.6.0",
]

RELEASE_DEPENDENCIES = ["bumpversion>=0.6.0", "twine>=4.0.2"]


class PyTest(Command):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        # pylint: disable=attribute-defined-outside-init
        self.pytest_args = [
            "--cov",
            "--cov-report=xml",
            "--junitxml",
            "./tests/output",
            "tests/",
        ]
        self.lint = False

    def finalize_options(self):
        # pylint: disable=attribute-defined-outside-init
        self.test_args = []
        self.test_suite = True

    def run(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def main():
    # A few handy release helpers.
    # For publishing you should install the extra 'release' dependencies
    # by running: pip install nylas['release']
    if len(sys.argv) > 1:
        if sys.argv[1] == "publish":
            try:
                subprocess.check_output(["git", "push", "--follow-tags"])
                subprocess.check_output(["python", "setup.py", "sdist"])
                subprocess.check_output(["twine", "upload", "-r", "testpypi", "dist/*"])
                subprocess.check_output(["twine", "upload", "dist/*"])
            except FileNotFoundError as e:
                print("Error encountered: {}.\n\n".format(e))
            sys.exit()
        elif sys.argv[1] == "build-docs":
            if not os.path.exists("docs"):
                os.makedirs("docs")
            try:
                # Copy the README and other markdowns to the docs folder
                shutil.copy("README.md", "docs/index.md")
                shutil.copy("Contributing.md", "docs/contributing.md")
                shutil.copy("LICENSE", "docs/license.md")

                subprocess.check_output(["mkdocs", "build"])
            except FileNotFoundError as e:
                print("Error encountered: {}.\n\n".format(e))
            sys.exit()
        elif sys.argv[1] == "release":
            if len(sys.argv) < 3:
                type_ = "patch"
            else:
                type_ = sys.argv[2]
            try:
                subprocess.check_output(
                    ["bumpversion", "--current-version", VERSION, type_]
                )
            except FileNotFoundError as e:
                print(
                    "Error encountered: {}.\n\n".format(e),
                    "Did you install the extra 'release' dependencies? (pip install nylas['release'])",
                )
            sys.exit()

    setup(
        name="nylas",
        version=VERSION,
        python_requires=">=3.8",
        packages=find_packages(),
        install_requires=RUN_DEPENDENCIES,
        dependency_links=[],
        tests_require=TEST_DEPENDENCIES,
        extras_require={
            "test": TEST_DEPENDENCIES,
            "docs": DOCS_DEPENDENCIES,
            "release": RELEASE_DEPENDENCIES,
        },
        cmdclass={"test": PyTest},
        author="Nylas Team",
        author_email="support@nylas.com",
        description="Python bindings for the Nylas API platform.",
        license="MIT",
        keywords="inbox app appserver email nylas contacts calendar",
        url="https://github.com/nylas/nylas-python",
        long_description_content_type="text/markdown",
        long_description=README,
    )


if __name__ == "__main__":
    main()
