from nylas.client.restful_models import (
    RestfulModel,
    NylasAPIObject,
    Contact,
    File,
    Message,
    Draft,
    Thread,
    Event,
    Folder,
    Label,
)


class Deltas(RestfulModel):
    attrs = (
        "cursor_start",
        "cursor_end",
        "_deltas",
    )
    read_only_attrs = tuple(attrs)

    def __init__(self, api):
        RestfulModel.__init__(self, Deltas, api)

    @property
    def deltas(self):
        """
        Instantiate a Delta object from the API response

        Returns:
            list[Delta]: List of Delta instantiated objects
        """
        if self._deltas:
            deltas = []
            for delta in self._deltas:
                deltas.append(Delta.create(self.api, **delta))
            return deltas


class Delta(RestfulModel):
    attrs = (
        "id",
        "cursor",
        "event",
        "object",
        "_attributes",
    )
    read_only_attrs = tuple(attrs)
    class_mapping = {
        "contact": Contact,
        "file": File,
        "message": Message,
        "draft": Draft,
        "thread": Thread,
        "event": Event,
        "folder": Folder,
        "label": Label,
    }

    def __init__(self, api):
        RestfulModel.__init__(self, Delta, api)

    @property
    def attributes(self):
        """
        Instantiate the object provided in the Delta

        Returns:
            NylasAPIObject: The object of NylasAPIObject type represented in the Delta
        """
        if self._attributes and self.object and self.object in self.class_mapping:
            return self.class_mapping[self.object].create(self.api, **self._attributes)
