import os
import sys
from setuptools import setup, find_packages

# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


setup(
    name="inbox",
    version="0.1.2",
    packages=find_packages(),

    install_requires=[
        "requests>=2.3.0",
        "six>=1.4.1",
    ],
    dependency_links=[],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        # '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        # 'hello': ['*.msg'],
    },

    author="Inbox Team",
    author_email="admin@inboxapp.com",
    description='Python bindings for Inbox, the next-generation email platform.',
    license="MIT",
    keywords="inbox app appserver email",
    url='https://github.com/inboxapp/inbox-python'
)
