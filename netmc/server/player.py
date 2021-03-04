# coding=utf-8
from .entity import Entity


class Player(Entity):
    def __init__(self, uid):
        super(Player, self).__init__(uid)
