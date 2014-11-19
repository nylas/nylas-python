from copy import copy

CHUNK_SIZE = 50
MAX_ITEMS = 500  # XXX


class RestfulModelCollectionIterator():
    def __init__(self, collection, offset=0, limit=MAX_ITEMS, **filters):
        self.collection = collection
        self.offset = offset
        self.limit = limit
        self.cache = []

    def next(self):
        if self.cache:
            return self.cache.pop()
        elif not self.limit:
            raise StopIteration()

        max_results = min(self.limit, CHUNK_SIZE)
        self.cache = self.collection.range(self.offset, max_results)

        if not self.cache:
            raise StopIteration()

        self.limit -= len(self.cache)
        self.offset += len(self.cache)

        return self.cache.pop()


class RestfulModelCollection():
    def __init__(self, cls, api, namespace, filter={}, offset=0,
                 limit=MAX_ITEMS, **filters):
        filters.update(filter)
        from inbox.client import APIClient
        if not isinstance(api, APIClient):
            raise Exception("Provided api was not an APIClient.")

        filters.setdefault('offset', 0)
        filters.setdefault('limit', MAX_ITEMS)

        self.model_class = cls
        self.filters = filters
        self.namespace = namespace
        self.api = api

    def __iter__(self):
        return RestfulModelCollectionIterator(self, **self.filters)

    def items(self):
        offset = 0
        while True:
            items = self._get_model_collection(offset)
            if not items:
                break

            for item in items:
                yield item

            offset += len(items)

    def first(self):
        results = self._get_model_collection(0, 1)
        if len(results):
            return results[0]
        return None

    def all(self):
        return self.range(self.filters['offset'],
                          self.filters['limit'])

    def where(self, filter={}, **filters):
        filters.update(filter)
        filters.setdefault('offset', 0)
        filters.setdefault('limit', MAX_ITEMS)
        collection = copy(self)
        collection.filters = filters
        return collection

    def range(self, offset=0, limit=CHUNK_SIZE):
        accumulated = []
        while len(accumulated) < limit:
            to_fetch = min(limit-len(accumulated), CHUNK_SIZE)
            results = self._get_model_collection(offset + len(accumulated),
                                                 to_fetch)
            accumulated.extend(results)

            # done if more than 'limit' items, less than asked for
            if not results or len(results) % to_fetch:
                break

        return accumulated

    def find(self, id):
        return self._get_model(id)

    def create(self, **args):
        return self.model_class.create(self.api, self.namespace, **args)

    def delete(self, id):
        return self.api._delete_resource(self.namespace, self.model_class, id)

    def __getitem__(self, offset):
        return self._get_model_collection(offset, 1)[0]

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
