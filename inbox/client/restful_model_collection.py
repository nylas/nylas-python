from copy import copy

CHUNK_SIZE = 50

class RestfulModelCollection(object):
    def __init__(self, cls, api, namespace, filter={}, offset=0,
                 **filters):
        filters.update(filter)
        from inbox.client import APIClient
        if not isinstance(api, APIClient):
            raise Exception("Provided api was not an APIClient.")

        filters.setdefault('offset', 0)

        self.model_class = cls
        self.filters = filters
        self.namespace = namespace
        self.api = api

    def __iter__(self):
        return self.items()

    def items(self):
        offset = 0
        while True:
            items = self._get_model_collection(offset, CHUNK_SIZE)
            if not items:
                break

            for item in items:
                yield item

            if len(items) < CHUNK_SIZE:
                # This is only here because namespaces are
                # treated like other collections
                break

            offset += len(items)

    def first(self):
        results = self._get_model_collection(0, 1)
        if len(results):
            return results[0]
        return None

    def all(self, limit=float('infinity')):
        return self._range(self.filters['offset'], limit)

    def where(self, filter={}, **filters):
        if 'from_' in filters:
            filters['from'] = filters.get('from_')
            del filters['from_']
        filters.update(filter)
        filters.setdefault('offset', 0)
        collection = copy(self)
        collection.filters = filters
        return collection

    def find(self, id):
        return self._get_model(id)

    def create(self, **args):
        return self.model_class.create(self.api, self.namespace, **args)

    def delete(self, id):
        return self.api._delete_resource(self.namespace, self.model_class, id)

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
        filters['limit'] = limit

        return self.api._get_resources(self.namespace, self.model_class,
                                       **filters)

    def _get_model(self, id):
        return self.api._get_resource(self.namespace, self.model_class, id,
                                      **self.filters)

    def _range(self, offset=0, limit=CHUNK_SIZE):
        accumulated = []
        while len(accumulated) < limit:
            to_fetch = min(limit-len(accumulated), CHUNK_SIZE)
            results = self._get_model_collection(offset + len(accumulated),
                                                 to_fetch)
            accumulated.extend(results)

            # done if we run out of items to fetch
            if not results or len(results) < to_fetch:
                break

        return accumulated
