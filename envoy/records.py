"""
Records provide immutable access to data returned by the Envoy server.
"""

import json

from collections.abc import Mapping, Sequence


class Record(Mapping):
    """
    A record provides access to data returned from the Envoy server along with helper
    methods for inspecting nested data and resources.
    """

    def __init__(self, data=None, /, parent=None, **kwargs):
        self.data = {}
        self.parent = parent

        if data is not None:
            self.data.update(data)
        if kwargs:
            self.data.update(kwargs)

    def fields(self):
        return tuple(self)

    def cast(self, key, item):
        """
        Converts an item into a nested record or record list as required. Subclasses
        may override this method to return different or particular types based on key.
        """
        if isinstance(item, dict):
            return Record(item, parent=self)

        if isinstance(item, list):
            if any([isinstance(sub, dict) for sub in item]):
                return RecordList(item, parent=self)

        return item

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        if key in self.data:
            return self.cast(key, self.data[key])
        raise KeyError(key)

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return repr(self.data)

    def __or__(self, other):
        if isinstance(other, Record):
            return self.__class__(self.data | other.data)
        if isinstance(other, dict):
            return self.__class__(self.data | other)
        return NotImplemented

    def __ror__(self, other):
        if isinstance(other, Record):
            return self.__class__(other.data | self.data)
        if isinstance(other, dict):
            return self.__class__(other | self.data)
        return NotImplemented

    def __ior__(self, other):
        if isinstance(other, Record):
            self.data |= other.data
        else:
            self.data |= other
        return self

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["data"] = self.__dict__["data"].copy()
        return inst

    def copy(self):
        if self.__class__ is Record:
            return Record(self.data.copy())
        import copy

        data = self.data
        try:
            self.data = {}
            c = copy.copy(self)
        finally:
            self.data = data
        c.update(self)
        return c

    def items(self):
        for key in self:
            yield key, self[key]

    def asdict(self):
        return self.data.copy()

    def pprint(self):
        print(json.dumps(self.data, indent=2))


class RecordList(Sequence):
    """
    A record list provides access to a sequence of data returned from an Envoy API
    request along with helper methods for inspecting subrecords.
    """

    def __init__(self, initlist=None, parent=None):
        self.data = []
        self.parent = parent

        if initlist is not None:
            if isinstance(initlist, type(self.data)):
                self.data[:] = initlist[:]
            elif isinstance(initlist, RecordList):
                self.data[:] = initlist.data[:]
            else:
                self.data = list(initlist)

    def cast(self, item):
        """
        Converts an item into a nested record or record list as required. Subclasses
        may override this method to return different or particular types.
        """
        if isinstance(item, dict):
            return Record(item, parent=self)

        if isinstance(item, list):
            if any([isinstance(sub, dict) for sub in item]):
                return RecordList(item, parent=self)

        return item

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self.data[i])
        else:
            return self.cast(self.data[i])

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["data"] = self.__dict__["data"][:]
        return inst

    def copy(self):
        return self.__class__(self)

    def pprint(self):
        print(json.dumps(self.data, indent=2))


class PaginatedRecords(RecordList):

    CollectionKey = None
    PageKey = "page"

    def __init__(self, data, parent=None):
        if self.CollectionKey is None:
            # expecting only a "page" field and the collections field, e.g. "accounts"
            collection_key = self._collection_key(data)
        else:
            collection_key = self.CollectionKey

        collection = data.pop(collection_key, None)
        super(PaginatedRecords, self).__init__(collection, parent=parent)

        self.page = data.pop(self.PageKey, {})
        for key, val in data.items():
            setattr(self, key, val)

    def _collection_key(self, data):
        for key in data.keys():
            if key == self.PageKey:
                continue

            if isinstance(data[key], list):
                return key

        return "collection"
