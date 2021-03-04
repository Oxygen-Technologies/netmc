# coding=utf-8
from .utils import CompFactory, Enum
from .base_behavior import BaseBehavior


class Attr(BaseBehavior):
    def __init__(self, uid):
        super(Attr, self).__init__(uid)

    @property
    def health(self):
        return CompFactory.CreateAttr(self._uid).GetAttrValue(Enum.AttrType.HEALTH)

    @health.setter
    def health(self, value):
        CompFactory.CreateAttr(self._uid).SetAttrValue(Enum.AttrType.HEALTH, value)
