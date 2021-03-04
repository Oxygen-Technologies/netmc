# coding=utf-8
from ...event import BaseEvent, Event
from ..player import Player


@Event.config('ServerChatEvent')
class ServerChatEvent(BaseEvent):
    def __init__(self, player):
        self.__player = Player(player)

    @property
    def player(self):
        # type: () -> Player
        return self.__player

    @classmethod
    def _serialize(cls, data):
        return cls(data['playerId'])
