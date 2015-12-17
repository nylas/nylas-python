import os
import sys
sys.path.append('nylas/')

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from _client_sdk_version import __VERSION__


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = '--junitxml ./tests/output tests/'

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def main():
    # A few handy release helpers.
    if len(sys.argv) > 1:
        if sys.argv[1] == 'publish':
            os.system('git push --follow-tags && python setup.py sdist upload')
            sys.exit()
        elif sys.argv[1] == 'release':
            if len(sys.argv) < 3:
                type_ = 'patch'
            else:
                type_ = sys.argv[2]
            os.system('bumpversion --current-version {} {}'
                      .format(__VERSION__, type_))
            sys.exit()

    setup(
        name="nylas",
        version=__VERSION__,
        packages=find_packages(),

        install_requires=[
            "requests>=2.4.2",
            "six>=1.4.1",
            "bumpversion>=0.5.0",
            # needed for SNI support, required by api.nylas.com
            "pyOpenSSL",
            "ndg-httpsclient",
            "pyasn1",
        ],
        dependency_links=[],
        tests_require=["pytest", "coverage", "responses", "httpretty"],
        cmdclass={'test': PyTest},
        author="Nylas Team",
        author_email="support@nylas.com",
        description='Python bindings for Nylas, the next-generation email platform.',
        license="MIT",
        keywords="inbox app appserver email nylas",
        url='https://github.com/nylas/nylas-python'
    )


if __name__ == '__main__':
    sys.exit(main())
