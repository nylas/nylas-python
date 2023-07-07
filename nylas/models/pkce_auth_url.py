from typing import NamedTuple


class PkceAuthUrl(NamedTuple):
    secret: str
    secret_hash: str
    url: str
