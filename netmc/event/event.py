# coding=utf-8
class Event(object):
    @staticmethod
    def config(event_name, namespace='Minecraft', engine='Engine'):
        def inner(cls):
            cls._EVENT_CONFIG = {'namespace': namespace,
                                 'systemName': engine,
                                 'eventName': event_name,
                                 'instance': None,
                                 'func': None
                                 }
            return cls

        return inner
