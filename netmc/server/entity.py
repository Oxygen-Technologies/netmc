# coding=utf-8
from .behavior import Pos, Attr


class Entity(Pos, Attr):
    def __init__(self, uid):
        super(Entity, self).__init__(uid)

    @property
    def id(self):
        return self._uid
