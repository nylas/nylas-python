from .restful_model_collection import RestfulModelCollection
from six import StringIO
import base64
import json


class NylasAPIObject(dict):
    attrs = []
    # The Nylas API holds most objects under '/n/', but some of
    # them are under '/a' (mostly the account-management and billing code).
    # api_root is a tiny metaprogramming hack to let us use the same
    # code for both.
    api_root = 'n'

    def __init__(self, cls, api, namespace):
        self.id = None
        self.cls = cls
        self.api = api
        self.namespace = namespace

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __getattr__ = dict.get

    @classmethod
    def create(cls, api, namespace_, **kwargs):
        if kwargs.get('object') and kwargs['object'] != cls.__name__.lower():
            # We were given a specific object type and we're trying to
            # instantiate something different; abort. (Relevant for folders
            # and labels API.)
            return
        obj = cls(api, namespace_)
        obj.cls = cls
        for attr in cls.attrs:
            # Support attributes we want to override with properties where
            # the property names overlap with the JSON names (e.g. folders)
            attr_name = attr
            if attr_name.startswith('_'):
                attr = attr_name[1:]
            if attr in kwargs:
                obj[attr_name] = kwargs[attr]
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


class Message(NylasAPIObject):
    attrs = ["bcc", "body", "cc", "date", "files", "from", "id",
             "namespace_id", "object", "subject", "thread_id", "to", "unread",
             "starred", "_folder", "_labels"]
    collection_name = 'messages'

    def __init__(self, api, namespace):
        NylasAPIObject.__init__(self, Message, api, namespace)

    @property
    def attachments(self):
        return self.child_collection(File, message_id=self.id)

    @property
    def folder(self):
        # Instantiate a Folder object from the API response
        if self._folder:
            return Folder.create(self.api, self.namespace, **self._folder)

    @property
    def labels(self):
        if self._labels:
            return [Label.create(self.api, self.namespace, **l)
                    for l in self._labels]
        else:
            return []

    def update_folder(self, folder_id):
        update = {'folder': folder_id}
        new_obj = self.api._update_resource(self.namespace,
            self.cls, self.id, update)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))
        return self.folder

    def update_labels(self, label_ids=[]):
        update = {'labels': label_ids}
        new_obj = self.api._update_resource(self.namespace,
            self.cls, self.id, update)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))
        return self.labels

    def add_labels(self, label_ids=[]):
        labels = [l.id for l in self.labels]
        labels = list(set(labels).union(set(label_ids)))
        return self.update_labels(labels)

    def add_label(self, label_id):
        return self.add_labels([label_id])

    def remove_labels(self, label_ids=[]):
        labels = [l.id for l in self.labels]
        labels = list(set(labels) - set(label_ids))
        return self.update_labels(labels)

    def remove_label(self, label_id):
        return self.remove_labels([label_id])

    def mark_as_read(self):
        update = {'unread': False}
        self.api._update_resource(self.namespace, self.cls, self.id, update)
        self.unread = False

    def star(self):
        update = {'starred': True}
        self.api._update_resource(self.namespace, self.cls, self.id, update)
        self.starred = True

    def unstar(self):
        update = {'starred': False}
        self.api._update_resource(self.namespace, self.cls, self.id, update)
        self.starred = False

    @property
    def raw(self):
        headers = {"Accept": "message/rfc822"}
        data = self.api._get_resource_data(self.namespace, Message, self.id,
                                           headers=headers)
        data = {'rfc822': data}
        return RawMessage.create(self.api, self.namespace, **data)


class RawMessage(NylasAPIObject):
    """
    a raw message, as returned by the /message/<id> endpoint when
    the "Accept" is set to "message/rfc822" in the request header
    """
    attrs = ["rfc822"]

    def __init__(self, api, namespace):
        NylasAPIObject.__init__(self, RawMessage, api, namespace)


class Tag(NylasAPIObject):
    attrs = ["id", "name", "namespace_id", "object"]
    collection_name = 'tags'

    def __init__(self, api, namespace):
        NylasAPIObject.__init__(self, Tag, api, namespace)


class Folder(NylasAPIObject):
    attrs = ["id", "display_name", "name"]
    collection_name = "folders"

    def __init__(self, api, namespace):
        NylasAPIObject.__init__(self, Folder, api, namespace)

    @property
    def threads(self):
        return self.child_collection({'in': self.id})

    @property
    def messages(self):
        return self.child_collection({'in': self.id})


class Label(NylasAPIObject):
    attrs = ["id", "display_name", "name"]
    collection_name = "labels"

    def __init__(self, api, namespace):
        NylasAPIObject.__init__(self, Label, api, namespace)

    @property
    def threads(self):
        return self.child_collection({'in': self.id})

    @property
    def messages(self):
        return self.child_collection({'in': self.id})


class Thread(NylasAPIObject):
    attrs = ["draft_ids", "id", "message_ids", "namespace_id", "object",
             "participants", "snippet", "subject", "subject_date", "tags",
             "last_message_timestamp", "first_message_timestamp",
             "unread", "starred", "version", "_folders", "_labels"]
    collection_name = 'threads'

    def __init__(self, api, namespace):
        NylasAPIObject.__init__(self, Thread, api, namespace)

    @property
    def messages(self):
        return self.child_collection(Message, thread_id=self.id)

    @property
    def drafts(self):
        return self.child_collection(Draft, thread_id=self.id)

    @property
    def folders(self):
        if self._folders:
            return [Folder.create(self.api, self.namespace, **f)
                    for f in self._folders]
        else:
            return []

    @property
    def labels(self):
        if self._labels:
            return [Label.create(self.api, self.namespace, **l)
                    for l in self._labels]
        else:
            return []

    def update_folder(self, folder_id):
        update = {'folder': folder_id}
        new_obj = self.api._update_resource(self.namespace,
            self.cls, self.id, update)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))
        return self.folder

    def update_labels(self, label_ids=[]):
        update = {'labels': label_ids}
        new_obj = self.api._update_resource(self.namespace,
            self.cls, self.id, update)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))
        return self.labels

    def add_labels(self, label_ids=[]):
        labels = [l.id for l in self.labels]
        labels = list(set(labels).union(set(label_ids)))
        return self.update_labels(labels)

    def add_label(self, label_id):
        return self.add_labels([label_id])

    def remove_labels(self, label_ids=[]):
        labels = [l.id for l in self.labels]
        labels = list(set(labels) - set(label_ids))
        return self.update_labels(labels)

    def remove_label(self, label_id):
        return self.remove_labels([label_id])

    def update_tags(self, add=[], remove=[]):
        # DEPRECATED
        update = {'add_tags': add, 'remove_tags': remove}
        self.api._update_resource(self.namespace, self.cls, self.id, update)

    def remove_tags(self, tags):
        # DEPRECATED
        self.update_tags(remove=tags)

    def add_tags(self, tags):
        # DEPRECATED
        self.update_tags(add=tags)

    def mark_as_read(self):
        update = {'unread': False}
        self.api._update_resource(self.namespace, self.cls, self.id, update)
        self.unread = False

    def mark_as_seen(self):
        self.mark_as_read()

    def archive(self):
        # DEPRECATED
        self.update_tags(['archive'], ['inbox'])

    def unarchive(self):
        # DEPRECATED
        self.update_tags(['inbox'], ['archive'])

    def trash(self):
        # DEPRECATED
        self.add_tags(['trash'])

    def star(self):
        update = {'starred': True}
        self.api._update_resource(self.namespace, self.cls, self.id, update)
        self.starred = True

    def unstar(self):
        update = {'starred': False}
        self.api._update_resource(self.namespace, self.cls, self.id, update)
        self.starred = False

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
        NylasAPIObject.__init__(self, Send, api, namespace)


class Draft(Message):
    attrs = ["bcc", "cc", "body", "date", "files", "from", "id",
             "namespace_id", "object", "subject", "thread_id", "to",
             "unread", "version", "file_ids"]
    collection_name = 'drafts'

    def __init__(self, api, namespace, thread_id=None):
        Message.__init__(self, api, namespace)
        NylasAPIObject.__init__(self, Thread, api, namespace)
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


class File(NylasAPIObject):
    attrs = ["content_type", "filename", "id", "is_embedded", "message_id",
             "namespace_id", "object", "size"]
    collection_name = 'files'

    def save(self):
        if hasattr(self, 'stream') and self.stream is not None:
            data = {self.filename: self.stream}
        elif hasattr(self, 'data') and self.data is not None:
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
        NylasAPIObject.__init__(self, File, api, namespace)


class Contact(NylasAPIObject):
    attrs = ["id", "namespace_id", "name", "email"]
    collection_name = 'contacts'

    def __init__(self, api, namespace):
        NylasAPIObject.__init__(self, Contact, api, namespace)


class Calendar(NylasAPIObject):
    attrs = ["id", "namespace_id", "name", "description", "read_only"]
    collection_name = 'calendars'

    def __init__(self, api, namespace):
        NylasAPIObject.__init__(self, Calendar, api, namespace)

    @property
    def events(self):
        return self.child_collection(Event, calendar_id=self.id)


class Event(NylasAPIObject):
    attrs = ["id", "namespace_id", "title", "description", "location",
             "read_only", "when", "busy", "participants", "calendar_id",
             "recurrence", "status", "master_event_id",
             "original_start_time"]
    collection_name = 'events'

    def __init__(self, api, namespace):
        NylasAPIObject.__init__(self, Event, api, namespace)

    def as_json(self):
        dct = NylasAPIObject.as_json(self)
        # Filter some parameters we got from the API
        if 'when' in dct:
            if 'object' in dct['when']:
                del dct['when']['object']

        return dct


class Namespace(NylasAPIObject):
    attrs = ["account", "email_address", "id", "namespace_id", "object",
             "provider", "name", "organization_unit"]
    collection_name = 'n'

    def __init__(self, api, namespace):
        NylasAPIObject.__init__(self, Namespace, api, namespace)

    def child_collection(self, cls, **filters):
        return RestfulModelCollection(cls, self.api, self.id, **filters)

    @property
    def threads(self):
        return self.child_collection(Thread)

    @property
    def tags(self):
        return self.child_collection(Tag)

    def has_folders(self):
        return self.organization_unit == 'folder'

    def has_labels(self):
        return self.organization_unit == 'label'

    @property
    def categories(self):
        if self.has_labels():
            return self.child_collection(Label)
        else:
            return self.child_collection(Folder)

    @property
    def folders(self):
        # folders and labels are served by the same underlying API
        return self.categories

    @property
    def labels(self):
        return self.categories

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


class Account(NylasAPIObject):
    # The Nylas API holds most objects under '/n/', but some of
    # them are under '/a' (mostly the account-management and billing code).
    # api_root is a tiny metaprogramming hack to let us use the same
    # code for both.
    api_root = 'a'

    attrs = ["account_id", "trial", "trial_expires", "sync_state",
             "billing_state", "namespace_id"]

    collection_name = 'accounts'

    def __init__(self, api, namespace):
        NylasAPIObject.__init__(self, Account, api, namespace)

    def as_json(self):
        dct = NylasAPIObject.as_json(self)
        return dct

    def upgrade(self):
        self.api._call_resource_method(self.namespace, self, self.account_id,
                                       'upgrade', None)

    def downgrade(self):
        self.api._call_resource_method(self.namespace, self, self.account_id,
                                       'downgrade', None)
