import os
import sys

from setuptools import setup, find_packages
from inbox._version import __VERSION__


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
        name="inbox",
        version=__VERSION__,
        packages=find_packages(),

        install_requires=[
            "requests>=2.3.0",
            "six>=1.4.1",
            "bumpversion>=0.5.0",
            # needed for SNI support, required by api.nilas.com
            "pyOpenSSL",
            "ndg-httpsclient",
            "pyasn1",
        ],
        dependency_links=[],

        author="Inbox Team",
        author_email="support@nilas.com",
        description='Python bindings for Inbox, the next-generation email platform.',
        license="MIT",
        keywords="inbox app appserver email",
        url='https://github.com/inboxapp/inbox-python'
    )

if __name__ == '__main__':
    sys.exit(main())
