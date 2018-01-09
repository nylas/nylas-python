from copy import copy

CHUNK_SIZE = 50

class RestfulModelCollection(object):
    def __init__(self, cls, api, filter=None, offset=0,
                 **filters):
        if filter:
            filters.update(filter)
        from nylas.client import APIClient
        if not isinstance(api, APIClient):
            raise Exception("Provided api was not an APIClient.")

        filters.setdefault('offset', offset)

        self.model_class = cls
        self.filters = filters
        self.api = api

    def __iter__(self):
        return self.values()

    def values(self):
        offset = self.filters['offset']
        while True:
            models = self._get_model_collection(offset, CHUNK_SIZE)
            if not models:
                break

            for model in models:
                yield model

            if len(models) < CHUNK_SIZE:
                break

            offset += len(models)

    def first(self):
        results = self._get_model_collection(0, 1)
        if results:
            return results[0]
        return None

    def all(self, limit=float('infinity')):
        return self._range(self.filters['offset'], limit)

    def where(self, filter=None, **filters):
        # Some API parameters like "from" and "in" also are
        # Python reserved keywords. To work around this, we rename
        # them to "from_" and "in_". The API still needs them in
        # their correct form though.
        reserved_keywords = ['from', 'in']
        for keyword in reserved_keywords:
            escaped_keyword = '{}_'.format(keyword)
            if escaped_keyword in filters:
                filters[keyword] = filters.get(escaped_keyword)
                del filters[escaped_keyword]

        if filter:
            filters.update(filter)
        filters.setdefault('offset', 0)
        collection = copy(self)
        collection.filters = filters
        return collection

    def get(self, id):
        return self._get_model(id)

    def create(self, **kwargs):
        return self.model_class.create(self.api, **kwargs)

    def delete(self, id, data=None, **kwargs):
        return self.api._delete_resource(self.model_class, id, data=data, **kwargs)

    def search(self, q):  # pylint: disable=invalid-name
        from nylas.client.restful_models import Message, Thread  # pylint: disable=cyclic-import
        if self.model_class is Thread or self.model_class is Message:
            kwargs = {'q': q}
            return self.api._get_resources(self.model_class, extra="search", **kwargs)
        else:
            raise Exception("Searching is only allowed on Thread and Message models")

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.step is not None:
                raise ValueError("'step' not supported for slicing "
                                 "RestfulModelCollection objects "
                                 "(e.g. messages[::step])")
            elif key.start < 0 or key.stop < 0:
                raise ValueError("slice indices must be positive")
            elif key.stop - key.start < 0:
                raise ValueError("ending slice index cannot be less than "
                                 "starting index")
            return self._range(key.start, key.stop-key.start)
        else:
            return self._get_model_collection(key, 1)[0]

    # Private functions

    def _get_model_collection(self, offset=0, limit=CHUNK_SIZE):
        filters = copy(self.filters)
        filters['offset'] = offset
        if not filters.get('limit'):
            filters['limit'] = limit

        return self.api._get_resources(self.model_class,
                                       **filters)

    def _get_model(self, id):
        return self.api._get_resource(self.model_class, id,
                                      **self.filters)

    def _range(self, offset=0, limit=CHUNK_SIZE):
        accumulated = []
        while len(accumulated) < limit:
            to_fetch = min(limit-len(accumulated), CHUNK_SIZE)
            results = self._get_model_collection(offset + len(accumulated),
                                                 to_fetch)
            accumulated.extend(results)

            # done if we run out of data to fetch
            if not results or len(results) < to_fetch:
                break

        return accumulated
