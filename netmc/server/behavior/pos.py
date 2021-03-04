# coding=utf-8
from .utils import CompFactory
from .base_behavior import BaseBehavior


class Pos(BaseBehavior):
    def __init__(self, uid):
        super(Pos, self).__init__(uid)

    @property
    def pos(self):
        return CompFactory.CreatePos(self._uid).GetPos()

    @pos.setter
    def pos(self, value):
        CompFactory.CreatePos(self._uid).SetPos(value)
