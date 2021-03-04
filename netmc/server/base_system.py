# coding=utf-8
from mod.server.system.serverSystem import ServerSystem


class ServerSystemBase(ServerSystem):
    event_list = {}

    def __init__(self, namespace, system_name):
        super(ServerSystemBase, self).__init__(namespace, system_name)
        self.__register_events()

    def __register_events(self):
        for event_data in self.event_list.values():
            event_data['instance'] = self
            self.ListenForEvent(**event_data)

    def destroy(self):
        pass

    def Destroy(self):
        self.destroy()

    def __del__(self):
        self.UnListenAllEvents()
