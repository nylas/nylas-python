#!/usr/bin/env python

from collections import defaultdict
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

from nylas import APIClient
from nylas.client.errors import NotFoundError

nylasfs='ibxfs'
refresh_s=30


class Memory(LoggingMixIn, Operations):
    """Example memory filesystem. Supports only one level of files."""

    def __init__(self):
        self.c = APIClient(api_server='http://localhost:5555')
        self.files = {}
        self.data = defaultdict(str)
        self.fd = 0
        now = time()
        self.updated = 0
        self.files['/'] = dict(st_mode=(S_IFDIR | 0755), st_ctime=now,
            st_mtime=now, st_atime=now, st_nlink=2)
        self.__refresh__()

    def __refresh__(self):
        now = time()
        if now - self.updated < refresh_s:
            return
        self.updated = now

        for th in self.c.threads.where(tag=nylasfs):
            in_dr = th.drafts[0]
            self.files[str("/" + in_dr.subject)] = dict(st_mode=(S_IFDIR | 0755), st_ctime=now,
                                       st_mtime=now, st_atime=now, st_nlink=2,
                                       in_dr=in_dr)

            for dir_file in in_dr.attachments:
                print dir_file
                self.files[str("/" + in_dr.subject + "/" + dir_file.filename)] = dict(st_mode=(S_IFREG | 0755), st_ctime=now,
                                           st_mtime=now, st_atime=now, st_nlink=2,
                                           st_size=dir_file.size,
                                           in_file=dir_file, in_dr=in_dr)

        for root_file in self.c.files.where(is_attachment=False):
            name = root_file.filename
            self.files[str("/" + name)] = dict(st_mode=(S_IFREG | 0755), st_ctime=now,
                                       st_mtime=now, st_atime=now, st_nlink=2,
                                       st_size=root_file.size,
                                       in_file=root_file)


    def chmod(self, path, mode):
        self.files[path]['st_mode'] &= 0770000
        self.files[path]['st_mode'] |= mode
        return 0

    def chown(self, path, uid, gid):
        self.files[path]['st_uid'] = uid
        self.files[path]['st_gid'] = gid

    def create(self, path, mode):
        # root path
        if path[0] == '/':
            if '/' not in path[1:]:
                in_file = self.c.files.create(filename=path[1:])
                in_file.data = ""
                in_file.save()

                self.files[path] = dict(st_mode=(S_IFREG | mode), st_nlink=1,
                    st_size=in_file.size, st_ctime=time(), st_mtime=time(), st_atime=time(),
                    in_file=in_file)
            elif len(path[1:].split('/')) > 2:
                print "Can't handle nested dirs."
                return -1
            else:
                dirname, fname = path[1:].split('/')
                in_th = self.c.threads.where(subject=dirname).first()
                in_dr = in_th.drafts[0]

                in_file = self.c.files.create(filename=fname)
                in_file.data = ""
                in_file.save()
                in_dr.attach(in_file)
                in_dr.save()
                print "created: ", fname

                self.files[path] = dict(st_mode=(S_IFREG | mode), st_nlink=1,
                    st_size=0, st_ctime=time(), st_mtime=time(), st_atime=time(),
                    in_file=in_file, in_dr=in_dr)

        self.fd += 1
        return self.fd

    def getattr(self, path, fh=None):
        if path not in self.files:
            raise FuseOSError(ENOENT)
        st = self.files[path]
        return st

    def getxattr(self, path, name, position=0):
        attrs = self.files[path].get('attrs', {})
        try:
            return attrs[name]
        except KeyError:
            return ''       # Should return ENOATTR

    def listxattr(self, path):
        attrs = self.files[path].get('attrs', {})
        return attrs.keys()

    def mkdir(self, path, mode):
        self.files[path] = dict(st_mode=(S_IFDIR | mode), st_nlink=2,
                st_size=0, st_ctime=time(), st_mtime=time(), st_atime=time())

        if path != '/':
            if path[0] == '/' and '/' not in path[1:]:
                path = path[1:]
                c = self.c
                draft = c.drafts.create(subject=path)
                draft.save()
                thread = c.threads.where(thread_id=draft.thread_id).first()
                try:
                    thread.add_tags([nylasfs])
                except NotFoundError as e:
                    print "didn't find inbox tag, creating."
                    if "No tag found" in e.message:
                        c.tags.create(name=nylasfs).save()
                        thread.add_tags([nylasfs])

        self.files['/']['st_nlink'] += 1

    def read(self, path, size, offset, fh):
        if path not in self.data:
            if path in self.files:
                in_file = self.files[path]['in_file']
                self.data[path] = in_file.download()
        return self.data[path][offset:offset + size]

    def readdir(self, path, fh):
        self.__refresh__()

        if path == '/':
            return ['.', '..'] + [x[1:] for x in self.files if x != '/' and len(x[1:].split('/')) == 1]
        elif len(path[1:].split('/')) > 2:
            print "Can't handle nested dirs."
            return -1
        else:
            return ['.', '..'] + [x.split('/')[2] for x in self.files if x != '/' and len(x[1:].split('/')) == 2 and x[1:].split('/')[0] == path[1:]]

    def readlink(self, path):
        return self.data[path]

    def removexattr(self, path, name):
        attrs = self.files[path].get('attrs', {})
        try:
            del attrs[name]
        except KeyError:
            pass        # Should return ENOATTR

    def rename(self, old, new):
        self.files[new] = self.files.pop(old)

    def rmdir(self, path):
        self.files.pop(path)
        self.files['/']['st_nlink'] -= 1

    def setxattr(self, path, name, value, options, position=0):
        # Ignore options
        attrs = self.files[path].setdefault('attrs', {})
        attrs[name] = value

    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    def symlink(self, target, source):
        self.files[target] = dict(st_mode=(S_IFLNK | 0777), st_nlink=1,
            st_size=len(source))
        self.data[target] = source

    def truncate(self, path, length, fh=None):
        self.data[path] = self.data[path][:length]
        self.files[path]['st_size'] = length

    def unlink(self, path):
        old_in_file = self.files[path]['in_file']
        self.c.files.delete(old_in_file.id)
        self.files.pop(path)

    def utimens(self, path, times=None):
        now = time()
        atime, mtime = times if times else (now, now)
        self.files[path]['st_atime'] = atime
        self.files[path]['st_mtime'] = mtime

    def write(self, path, data, offset, fh):
        self.data[path] = self.data[path][:offset] + data
        self.files[path]['st_size'] = len(self.data[path])

        old_in_file = self.files[path]['in_file']
        in_dr = self.files[path].get('in_dr')

        if '/' not in path[1:]:
            filename = path[1:]
        else:
            filename = path[1:].split('/')[1]

        in_file = self.c.files.create(filename=filename)
        in_file.data = self.data[path]
        in_file.save()

        self.files[path]['in_file'] = in_file

        if in_dr:
            in_dr.detach(old_in_file)
            in_dr.attach(in_file)
            in_dr.save()

            self.files[path]['in_dr'] = in_dr

        # after we've update the draft we can delete the file
        self.c.files.delete(old_in_file.id)
        return len(data)


if __name__ == "__main__":
    if len(argv) != 2:
        print 'usage: %s <mountpoint>' % argv[0]
        exit(1)
    fuse = FUSE(Memory(), argv[1], foreground=True)

