# coding=utf-8
from .entity import Entity
from .behavior import Item


class Player(Entity, Item):
    def __init__(self, uid):
        super(Player, self).__init__(uid)
