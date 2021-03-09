# coding=utf-8
from mod.server.system.serverSystem import ServerSystem


class ServerSystemBase(ServerSystem):
    """
    此类作为Mod服务端系统的基类，旨在简化开发的复杂度。主要从包含以下几个方面：

    1. 简化事件注册机制
    2. 与客户端无感通信

    ## 与客户端无感通信
    当客户端向服务端发起Notify时，原本的方法是无法通过返回值来得到服务端的结果的。
    改进后，客户端发起的查询类请求，服务端都会通过反向Notify的方式反馈给客户端

    客户端代码
    ```
    def show_cctvs(self):
        cctvs = self.from_server('get_cameras', {'player_id': self.player_id})
        self.popup_notice(u'你拥有的监控探头有 {}'.format(cctvs))
    ```

    服务端代码
    ```
    @to_client()    # 如果客户端from_server函数的signore参数和此函数名不同，通过传入参数到 to_client 来完成匹配
    def get_cctvs(self, data):
        ...
        cctvs = [...]
        return cctvs
    ```
    """
    event_list = {}
    to_client_functions = {}

    def __init__(self, namespace, system_name):
        super(ServerSystemBase, self).__init__(namespace, system_name)

        self._mod_name = None
        self._client_system_name = None

        self.__init_by_config()

        self.__register_events()
        self.__init_to_client_pipeline()

    def __init_by_config(self):
        """
        通过配置初始化
        Returns:

        """
        from ... import config
        self._mod_name = config.MOD_NAME
        self._client_system_name = config.CLIENT_SYSTEM_NAME

    def __init_to_client_pipeline(self):
        self.ListenForEvent(instance=self,
                            namespace=self.mod_name,
                            systemName=self.client_system_name,
                            eventName='get_data_from_server',
                            func=self.data_to_client)

    @property
    def mod_name(self):
        if isinstance(self._mod_name, basestring):
            return self._mod_name
        raise ValueError(u'没有获取到mod_name的值, 请检查配置, 不存在或不是字符串...')

    @property
    def client_system_name(self):
        if isinstance(self._client_system_name, basestring):
            return self._client_system_name
        raise ValueError(u'没有获取到client_system_name的值, 请检查配置, 不存在或不是字符串...')

    def __register_events(self):
        """自动注册时间装饰器装饰过的函数为服务端事件"""
        for event_data in self.event_list.values():
            event_data['instance'] = self
            self.ListenForEvent(**event_data)

    def destroy(self):
        pass

    def Destroy(self):
        self.destroy()

    @classmethod
    def to_client(cls, alias=None):
        """用于将方法转换为向客户端反馈数据的回调函数的装饰器"""

        def inner(func):
            new_name = alias or func.__name__
            cls.to_client_functions[new_name] = func
            return func

        return inner

    def __exec_signore(self, signore, data):
        """
        这个函数用于动态调用子类对象的方法
        这个函数的实现借助了eval的特性，下面这段代码说明了它的可行性
        ```
        class A(object):
            def x(self):
                return eval('foo', globals(), {k: getattr(self, k) for k in dir(self)})

        class B(A):
            def foo(self):
                print('ok')

        b = B()
        b.x()()
        # 结果将成功打印出 ok
        ```
        """
        func = ServerSystemBase.to_client_functions.get(signore)
        return func(self, data)

    def data_to_client(self, signore_data):
        player_id = signore_data.get('player_id')
        signore = signore_data.get('signore')
        data = signore_data.get('data')
        result = self.__exec_signore(signore, data)
        # 返回数据给客户端
        self.NotifyToClient(player_id,
                            '_on_server_data_got',
                            result)

    def __del__(self):
        self.UnListenAllEvents()
