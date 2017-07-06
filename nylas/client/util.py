from six.moves.urllib.parse import urlencode


# From tornado.httputil
def url_concat(url, args, fragments=None):
    """Concatenate url and argument dictionary regardless of whether
    url has existing query parameters.

    >>> url_concat("http://example.com/foo?a=b", dict(c="d"))
    'http://example.com/foo?a=b&c=d'
    """

    if not args and not fragments:
        return url

    # Strip off hashes
    while url[-1] == '#':
        url = url[:-1]

    fragment_tail = ''
    if fragments:
        fragment_tail = '#' + urlencode(fragments)

    args_tail = ''
    if args:
        if url[-1] not in ('?', '&'):
            args_tail += '&' if ('?' in url) else '?'
        args_tail += urlencode(args)

    return url + args_tail + fragment_tail
