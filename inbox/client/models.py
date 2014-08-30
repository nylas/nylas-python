from .restful_model_collection import RestfulModelCollection
from cStringIO import StringIO


class InboxAPIObject(dict):
    attrs = []

    def __init__(self, cls, api, namespace):
        self.id = None
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
        if 'id' not in dct:
            obj['id'] = None

        return obj

    def as_json(self):
        dct = {}
        for attr in self.cls.attrs:
            if hasattr(self, attr):
                dct[attr] = getattr(self, attr)
        return dct

    def child_collection(self, cls, filters={}):
        return RestfulModelCollection(cls, self.api, self.namespace, filters)

    def save(self):
        if self.id:
            self.api._update_resource(self.namespace, self.cls, self.id,
                                      self.as_json())
        else:
            new_obj = self.api._create_resource(self.namespace, self.cls,
                                                self.as_json())
            for attr in self.cls.attrs:
                if hasattr(new_obj, attr):
                    setattr(self, attr, getattr(new_obj, attr))

    def update(self):
        self.api._update_resource(self.namespace, self.cls, self.id,
                                  self.as_json())


class Message(InboxAPIObject):
    attrs = ["bcc", "body", "date", "files", "from", "id", "namespace",
             "object", "subject", "thread", "to", "unread"]
    collection_name = 'messages'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Message, api, namespace)

    @property
    def attachments(self):
        return self.child_collection(File, {'message': self.id})


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

    def update_tags(self, tags_to_add=[], tags_to_remove=[]):
        update = {'add_tags': tags_to_add, 'remove_tags': tags_to_remove}
        self.api._update_resource(self.namespace, self.cls, self.id, update)

    def remove_tags(self, tags):
        self.update_tags([], tags)

    def add_tags(self, tags):
        self.update_tags(tags, [])

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

    def create_reply(self):
        d = self.drafts.create()
        d.reply_to_thread = self.id
        d.subject = self.subject
        return d


# This is a dummy class that allows us to use the create_resource function
# and pass in a 'Send' object that will translate into a 'send' endpoint.
class Send(Message):
    collection_name = 'send'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Send, api, namespace)


class Draft(Message):
    attrs = Message.attrs + ["state", "reply_to_thread", "version"]
    collection_name = 'drafts'

    def __init__(self, api, namespace, reply_to_thread=None):
        Message.__init__(self, api, namespace)
        InboxAPIObject.__init__(self, Thread, api, namespace)
        # We should probably move to using 'file_ids' instead of 'files'
        # self.file_ids = []
        self.files = []

    def attach(self, file):
        if not file.id:
            file.save()

        self.files.append(file.id)

    def send(self):
        # self.files = self.file_ids
        if not self.id:
            self.save()

        d_params = {'draft_id': self.id}
        if hasattr(self, 'reply_to_thread'):
            d_params['reply_to_thread'] = self.reply_to_thread
        if hasattr(self, 'version'):
            d_params['version'] = self.version

        self.api._create_resource(self.namespace, Send, d_params)


class File(InboxAPIObject):
    attrs = ["content_type", "filename", "id", "is_embedded", "message",
             "namespace", "object", "size"]
    collection_name = 'files'

    def save(self):
        if hasattr(self, 'stream'):
            data = {self.filename: self.stream}
        elif hasattr(self, 'data'):
            data = {self.filename: StringIO(self.data)}
        else:
            raise Exception("File object not properly formatted, must provide"
                            " either a stream or data.")

        new_obj = self.api._create_resources(self.namespace, File, data)
        new_obj = new_obj[0]
        for attr in self.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))

    def download(self):
        if not self.id:
            raise Exception("Can't download a file that hasn't been uploaded.")

        return self.api._get_resource_data(self.namespace, File, self.id,
                                           extra='download')

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, File, api, namespace)


class Contact(InboxAPIObject):
    attrs = ["id", "namespace", "name", "email"]
    collection_name = 'contacts'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Contact, api, namespace)


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

    def child_collection(self, cls, filters={}):
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

    @property
    def events(self):
        return self.child_collection(Event)
