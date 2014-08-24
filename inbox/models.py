from restful_model_collection import RestfulModelCollection


class InboxAPIObject(dict):
    attrs = []

    def __init__(self, cls, api, namespace):
        self.dct = {'id': None}
        self.cls = cls
        self.api = api
        self.namespace = namespace

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    @classmethod
    def from_dict(cls, api, namespace, dct):
        obj = cls(api, namespace)
        obj.cls = cls
        for attr in cls.attrs:
            if attr in dct:
                obj[attr] = dct[attr]

        return obj

    def as_json(self):
        dct = {}
        for attr in cls.attrs:
            dct[attr] = getattr(self, attr)
        return dct

    def child_collection(self, cls, filters = {}):
      return RestfulModelCollection(cls, self.api, self.namespace, filters)

    def save(self):
        if self.id:
            self.api._update_resource(self.namespace, self.cls, self.id, self.as_json())
        else:
            self.api._create_resource(self.namespace, self.cls, self.id, self.as_json())

    def update(self):
        self.api._update_resource(self.namespace, self.cls, self.id, self.as_json())


class Message(InboxAPIObject):
    attrs = ["bcc", "body", "date", "files", "from", "id", "namespace",
             "object", "subject", "thread", "to", "unread"]
    collection_name='messages'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Message, api, namespace)


class Tag(InboxAPIObject):
    attrs = ["id", "name", "namespace", "object"]
    collection_name = 'tags'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Tag, api, namespace)


class Thread(InboxAPIObject):
    attrs = ["drafts", "id", "messages", "namespace", "object", "participants",
             "snippet", "subject", "subject_date", "tags"]
    collection_name = 'threads'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Thread, api, namespace)

    @property
    def messages(self):
        return self.child_collection(Message, {'thread': self.id})

    @property
    def drafts(self):
        return self.child_collection(Draft, {'thread': self.id})

    def update_tags(self, tags_to_add = [], tags_to_remove = []):
        update = {'add_tags': tags_to_add, 'remove_tags': tags_to_remove}
        self.api._update_resource(self.namespace, self.cls, self.id, update)

    def mark_as_read(self):
      self.update_tags([], ['unread'])

    def mark_as_seen(self):
      self.update_tags([], ['unseen'])

    def archive(self):
      self.update_tags(['archive'], ['inbox'])

    def unarchive(self):
      self.update_tags(['inbox'], ['archive'])

    def star(self):
      self.update_tags(['starred'], [''])

    def unstar(self):
      self.update_tags([], ['starred'])


class Draft(Message):
    attrs = Message.attrs + ["state", "reply_to_thread"]
    collection_name = 'drafts'

    def __init__(self, api, namespace):
        Message.__init__(self, api, namespace)
        InboxAPIObject.__init__(self, Thread, api, namespace)


class File(InboxAPIObject):
    attrs = ["content_type", "filename", "id", "is_embedded", "message",
             "namespace", "object", "size"]
    collection_name = 'files'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, File, api, namespace)

class Event(InboxAPIObject):
    attrs = ["id", "namespace", "subject", "body", "location", "read_only",
             "start", "end", "participants"]
    collection_name = 'events'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Event, api, namespace)

class Namespace(InboxAPIObject):
    attrs = ["account", "email_address", "id", "namespace", "object",
             "provider"]
    collection_name = 'n'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Namespace, api, namespace)

    def child_collection(self, cls, filters = {}):
      return RestfulModelCollection(cls, self.api, self.id, filters)

    @property
    def threads(self):
      return self.child_collection(Thread)

    @property
    def tags(self):
      return self.child_collection(Tag)

    @property
    def messages(self):
      return self.child_collection(Message)

    @property
    def files(self):
      return self.child_collection(File)

    @property
    def drafts(self):
      return self.child_collection(Draft)

    @property
    def contacts(self):
      return self.child_collection(Contact)
