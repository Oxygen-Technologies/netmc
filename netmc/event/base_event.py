# coding=utf-8

class BaseEvent(object):
    _EVENT_CONFIG = {}

    @classmethod
    def _serialize(cls, data):
        return cls(**data)

    @classmethod
    def _deserialize(cls, *args, **kwargs):
        return

    @classmethod
    def callback(cls, method):
        def inner(instance, data):
            method(instance, cls._serialize(data))

        cls._EVENT_CONFIG['func'] = method
        inner.event_conf = cls._EVENT_CONFIG

        return inner

    @classmethod
    def __notify(cls, method, target=None, *args, **kwargs):
        deserialize_data = cls._deserialize(*args, **kwargs)
        _args = (cls._EVENT_CONFIG['eventName'], deserialize_data) if target else (
            cls._EVENT_CONFIG['eventName'], target, deserialize_data)
        getattr(cls._EVENT_CONFIG['instance'], method)(*_args)

    @classmethod
    def notify_to_server(cls, *args, **kwargs):
        cls.__notify('NotifyToServer', *args, **kwargs)

    @classmethod
    def notify_to_client(cls, player, *args, **kwargs):
        cls.__notify('NotifyToClient', player, *args, **kwargs)

    @classmethod
    def broadcast_event(cls, *args, **kwargs):
        cls.__notify('BroadcastEvent', *args, **kwargs)

    @classmethod
    def broadcast_to_all_client(cls, *args, **kwargs):
        cls.__notify('BroadcastToAllClient', *args, **kwargs)
