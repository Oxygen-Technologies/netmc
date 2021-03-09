# coding=utf-8
import mod.client.extraClientApi as clientApi
from mod.client.system.clientSystem import ClientSystem
from mod.client.clientEvent import ClientEvent


class ClientSystemBase(ClientSystem):
    """
    此类作为Mod客户端系统的基类，旨在优化开发接口，降低开发的复杂度。主要从包含以下几个方面：

    1. 引擎事件监听机制
    2. UI集成机制
    3. 方块事件监听注册机制
    4. 自定义事件注册机制
    5. 服务端数据获取机制

    ## 引擎事件监听机制

    原本监听自定义事件的方法
    ```
    self.ListenForEvent(MOD_NAME, SERVER_SYSTEM_NAME, ON_RETURN_PLAYER_CAMERAS, self, self.callback_function)
    ```
    优化后的方法
    ```
    @event()    # MOD_NAME, SERVER_SYSTEM_NAME 可作为参数传入event()
    def on_return_player_cameras(data):
        pass
    ```
    """

    def __init__(self, namespace, system_name):
        super(ClientSystemBase, self).__init__(namespace, system_name)

        self.__server_data = {}
        self._mod_name = None
        self._server_system_name = None

        self.__init_by_config()

        self.player_id = clientApi.GetLocalPlayerId()

        # 监听从服务端返回数据的Notify
        self.ListenForEvent(self.mod_name, self.server_system_name, 'data_from_server', self, self._on_server_data_got)

        self.game_comp = clientApi.GetEngineCompFactory().CreateGame(self.player_id)

    def __init_by_config(self):
        """
        通过配置初始化
        Returns:

        """
        from ... import config
        self._mod_name = config.MOD_NAME
        self._server_system_name = config.SERVER_SYSTEM_NAME

    @property
    def mod_name(self):
        if isinstance(self._mod_name, basestring):
            return self._mod_name
        raise ValueError(u'没有获取到mod_name的值, 请检查配置, 不存在或不是字符串...')

    @property
    def server_system_name(self):
        if isinstance(self._server_system_name, basestring):
            return self._server_system_name
        raise ValueError(u'没有获取到client_system_name的值, 请检查配置, 不存在或不是字符串...')

    def exec_delay(self, delay, func, args):
        self.game_comp.AddTimer(delay, func, args)

    def popup_notice(self, msg, subtitle='', color=''):
        """
        代替原生的game_comp.SetPopupNotice方法
        Args:
            msg: 信息
            subtitle: 子标题
            color: 必须是RED ... 中的一个

        Returns:

        """
        self.game_comp.SetPopupNotice(color + msg, subtitle)

    def from_server(self, signore, data=None, delay=0.1):
        """
        此函数用于与从服务端获取数据，你需要在客户端实现一个名称与signore参数相同的函数，并用 @to_client() 装饰器装饰，
        或是在装饰器参数中指明signore名称，如 @to_client('foo')
        Args:
            signore: string 信号名称，可以简单理解为对应服务端目标函数的名称
            data: dict 需要传入服务端函数的数据
            delay: float 延迟获取结果的时间，用于解决服务端延迟较大的问题，默认为0.1秒。现在还不起作用

        Returns:

        """
        # 通过NotifyToServer向服务端发起请求
        self.NotifyToServer('get_data_from_server', {'player_id': self.player_id, 'signore': signore, 'data': data})
        # 从结果中获取信息
        return self.__get_server_data(signore, delay)

    def __get_server_data(self, signore, delay):
        # TODO 将实现替换成延迟获取结果
        retry_times = 10
        while retry_times > 0:
            res = self.__server_data.get(signore)
            if res is not None:
                return res
            retry_times -= 1

    def _on_server_data_got(self, data):
        """
        从服务端获取到数据的回调
        Args:
            data:

        Returns:

        """
        self.__server_data.update(data)
