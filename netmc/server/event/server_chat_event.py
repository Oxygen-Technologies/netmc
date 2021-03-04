# coding=utf-8
from ...event import BaseEvent, Event
from ..player import Player


@Event.config('ServerChatEvent')
class ServerChatEvent(BaseEvent):
    def __init__(self, playerId, username, message, cancel, bChatById, toPlayerIds, players, messageValid):
        self.__player = Player(playerId)
        self.__username = username
        self.__message = message
        self.__player_list = toPlayerIds
        self.chat_by_player = bChatById
        self.cancel = cancel

    @property
    def player(self):
        # type: () -> Player
        return self.__player

    @property
    def username(self):
        return self.__username

    @property
    def message(self):
        return self.__message

    @property
    def player_list(self):
        return self.__player_list

    @player_list.setter
    def player_list(self, value):
        self.__player_list = [player.name for player in value]
