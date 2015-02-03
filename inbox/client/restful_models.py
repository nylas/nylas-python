from .restful_model_collection import RestfulModelCollection
from cStringIO import StringIO
import base64
import json


class InboxAPIObject(dict):
    attrs = []
    # The inbox API holds most objects under '/n/', but some of
    # them are under '/a' (mostly the account-management and billing code).
    # api_root is a tiny metaprogramming hack to let us use the same
    # code for both.
    api_root = 'n'

    def __init__(self, cls, api, namespace):
        self.id = None
        self.cls = cls
        self.api = api
        self.namespace = namespace

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    @classmethod
    def create(cls, api, namespace_, **kwargs):
        obj = cls(api, namespace_)
        obj.cls = cls
        for attr in cls.attrs:
            if attr in kwargs:
                obj[attr] = kwargs[attr]
        if 'id' not in kwargs:
            obj['id'] = None

        return obj

    def as_json(self):
        dct = {}
        for attr in self.cls.attrs:
            if hasattr(self, attr):
                dct[attr] = getattr(self, attr)
        return dct

    def child_collection(self, cls, **filters):
        return RestfulModelCollection(cls, self.api, self.namespace, **filters)

    def save(self):
        if self.id:
            new_obj = self.api._update_resource(self.namespace,
                                                self.cls, self.id,
                                                self.as_json())
        else:
            new_obj = self.api._create_resource(self.namespace, self.cls,
                                                self.as_json())
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))

    def update(self):
        new_obj = self.api._update_resource(self.namespace, self.cls,
                                            self.id, self.as_json())
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))


class Message(InboxAPIObject):
    attrs = ["bcc", "body", "date", "files", "from", "id", "namespace_id",
             "object", "subject", "thread_id", "to", "unread"]
    collection_name = 'messages'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Message, api, namespace)

    @property
    def attachments(self):
        return self.child_collection(File, message_id=self.id)

    @property
    def raw(self):
        data = self.api._get_resource_data(self.namespace, Message, self.id,
                                           extra='rfc2822')
        data = json.loads(data)
        return RawMessage.create(self.api, self.namespace, **data)


class RawMessage(InboxAPIObject):
    """a raw message, as returned by the /message/<id>/rfc2822 endpoint"""
    attrs = ["rfc2822"]

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, RawMessage, api, namespace)

    @property
    def rfc2822(self):
        # base64-decode the contents, for convenience
        return base64.b64decode(self['rfc2822'])


class Tag(InboxAPIObject):
    attrs = ["id", "name", "namespace_id", "object"]
    collection_name = 'tags'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Tag, api, namespace)


class Thread(InboxAPIObject):
    attrs = ["draft_ids", "id", "message_ids", "namespace_id", "object",
             "participants", "snippet", "subject", "subject_date", "tags"]
    collection_name = 'threads'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Thread, api, namespace)

    @property
    def messages(self):
        return self.child_collection(Message, thread_id=self.id)

    @property
    def drafts(self):
        return self.child_collection(Draft, thread_id=self.id)

    def update_tags(self, add=[], remove=[]):
        update = {'add_tags': add, 'remove_tags': remove}
        self.api._update_resource(self.namespace, self.cls, self.id, update)

    def remove_tags(self, tags):
        self.update_tags(remove=tags)

    def add_tags(self, tags):
        self.update_tags(add=tags)

    def mark_as_read(self):
        self.remove_tags(['unread'])

    def mark_as_seen(self):
        self.remove_tags(['unseen'])

    def archive(self):
        self.update_tags(['archive'], ['inbox'])

    def unarchive(self):
        self.update_tags(['inbox'], ['archive'])

    def trash(self):
        self.add_tags(['trash'])

    def star(self):
        self.add_tags(['starred'])

    def unstar(self):
        self.remove_tags(['starred'])

    def create_reply(self):
        d = self.drafts.create()
        d.thread_id = self.id
        d.subject = self.subject
        return d


# This is a dummy class that allows us to use the create_resource function
# and pass in a 'Send' object that will translate into a 'send' endpoint.
class Send(Message):
    collection_name = 'send'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Send, api, namespace)


class Draft(Message):
    attrs = ["bcc", "body", "date", "files", "from", "id",
             "namespace_id", "object", "subject", "thread_id", "to",
             "unread", "version", "file_ids"]
    collection_name = 'drafts'

    def __init__(self, api, namespace, thread_id=None):
        Message.__init__(self, api, namespace)
        InboxAPIObject.__init__(self, Thread, api, namespace)
        self.file_ids = []

    def attach(self, file):
        if not file.id:
            file.save()

        self.file_ids.append(file.id)

    def detach(self, file):
        if file.id in self.file_ids:
            self.file_ids.remove(file.id)

    def send(self):
        # self.files = self.file_ids
        if not self.id:
            self.save()

        d_params = {'draft_id': self.id}
        if hasattr(self, 'thread_id'):
            d_params['thread_id'] = self.thread_id
        if hasattr(self, 'version'):
            d_params['version'] = self.version

        self.api._create_resource(self.namespace, Send, d_params)


class File(InboxAPIObject):
    attrs = ["content_type", "filename", "id", "is_embedded", "message_id",
             "namespace_id", "object", "size"]
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
    attrs = ["id", "namespace_id", "name", "email"]
    collection_name = 'contacts'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Contact, api, namespace)


class Calendar(InboxAPIObject):
    attrs = ["id", "namespace_id", "name", "description", "event_ids"]
    collection_name = 'calendars'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Calendar, api, namespace)

    @property
    def events(self):
        return self.child_collection(Event, calendar_id=self.id)


class Event(InboxAPIObject):
    attrs = ["id", "namespace_id", "title", "description", "location",
             "read_only", "when", "participants", "calendar_id"]
    collection_name = 'events'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Event, api, namespace)

    def as_json(self):
        dct = InboxAPIObject.as_json(self)
        # Filter some parameters we got from the API
        if 'when' in dct:
            if 'object' in dct['when']:
                del dct['when']['object']

        return dct


class Namespace(InboxAPIObject):
    attrs = ["account", "email_address", "id", "namespace_id", "object",
             "provider", "name"]
    collection_name = 'n'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Namespace, api, namespace)

    def child_collection(self, cls, **filters):
        return RestfulModelCollection(cls, self.api, self.id, **filters)

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

    @property
    def calendars(self):
        return self.child_collection(Calendar)


class Account(InboxAPIObject):
    # The inbox API holds most objects under '/n/', but some of
    # them are under '/a' (mostly the account-management and billing code).
    # api_root is a tiny metaprogramming hack to let us use the same
    # code for both.
    api_root = 'a'

    attrs = ["account_id", "trial", "trial_expires", "sync_state",
             "billing_state", "namespace_id"]

    collection_name = 'accounts'

    def __init__(self, api, namespace):
        InboxAPIObject.__init__(self, Account, api, namespace)

    def as_json(self):
        dct = InboxAPIObject.as_json(self)
        return dct

    def upgrade(self):
        self.api._call_resource_method(self.namespace, self, self.account_id,
                                       'upgrade', None)

    def downgrade(self):
        self.api._call_resource_method(self.namespace, self, self.account_id,
                                       'downgrade', None)
