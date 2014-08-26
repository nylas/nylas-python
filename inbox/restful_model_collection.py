from copy import deepcopy

CHUNK_SIZE = 50


class RestfulModelCollection(list):
    def __init__(self, cls, api, namespace, filters = {}):
        from inbox import APIClient
        if not isinstance(api, APIClient):
            raise Exception("Provided api was not an APIClient.")

        self.model_class = cls
        self.filters = filters
        self.namespace = namespace
        self.api = api

    def items(self):
        offset = 0
        finished = False
        while not finished:
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
        maxint = 2**64-1    # XXX
        return self.range(0, maxint)

    def where(self, filters):
        collection = deepcopy(self)
        collection.filters = filters
        return collection

    def range(self, offset = 0, limit = CHUNK_SIZE):
        accumulated = []
        finished = False
        chunk_size = CHUNK_SIZE

        while len(accumulated) < limit:
            results = self._get_model_collection(offset + len(accumulated),
                                                chunk_size)
            accumulated.extend(results)

            # done if more than 'limit' items, less than asked for
            if not len(results) or len(results) % chunk_size:
                break

        return accumulated[0:limit]

    def find(self, id):
        return self._get_model(id)

    def build(self, args):
        return self.model_class.from_dict(self.api,
                                          self.namespace,
                                          args)

    def create(self):
        return self.build({})

    def __getitem__(self, offset):
        return self._get_model_collection(offset, 1)[0]

    # Private functions

    def _get_model_collection(self, offset = 0, limit = CHUNK_SIZE):
        filters = deepcopy(self.filters)
        filters['offset'] = offset
        filters['limit'] = limit

        return self.api._get_resources(self.namespace, self.model_class,
                                      filters)

    def _get_model(self, id):
        return self.api._get_resource(self.namespace, self.model_class, id,
                                      filters)
