# coding=utf-8
class Mod(object):
    @staticmethod
    def system(cls):
        cls_attrs = cls.__dict__.copy()
        cls.event_list = {}
        for name, method in cls_attrs.iteritems():
            if hasattr(method, 'event_conf'):
                cls.event_list[name] = method.event_conf
        return cls
