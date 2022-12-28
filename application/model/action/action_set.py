from collections.abc import Sequence

from application.model.action.action import Action


class ActionSet(Sequence):

    def __init__(self, iterable):
        self.elements = []
        for value in iterable:
            if not isinstance(value, Action):
                raise AttributeError(f"{self.__class__.__name__} can only be a list of Action objects")
            self.elements.append(value)

    def __repr__(self):
        return repr(self.elements)

    def __iter__(self):
        return iter(self.elements)

    def __contains__(self, value):
        return value in self.elements

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self.elements[i])
        else:
            return self.elements[i]

    def __setitem__(self, i, item):
        self.elements[i] = item

    def __delitem__(self, i):
        del self.elements[i]

    def append(self, item):
        self.elements.append(item)

    def insert(self, i, item):
        self.elements.insert(i, item)

    def pop(self, i=-1):
        return self.elements.pop(i)

    def remove(self, item):
        self.elements.remove(item)

    def clear(self):
        self.elements.clear()

    def copy(self):
        return self.__class__(self)

    def count(self, item):
        return self.elements.count(item)

    def index(self, item, *args):
        return self.elements.index(item, *args)

    def reverse(self):
        self.elements.reverse()

    def sort(self, /, *args, **kwds):
        self.elements.sort(*args, **kwds)

    def extend(self, other):
        if isinstance(other, ActionSet):
            self.elements.extend(other.elements)
        else:
            self.elements.extend(other)
