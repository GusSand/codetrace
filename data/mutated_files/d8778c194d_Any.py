from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""定义mprpc客户端中的通用组件.

+ File: utils.py
+ Version: 0.5
+ Author: hsz
+ Email: hsz1273327@gmail.com
+ Copyright: 2018-02-08 hsz
+ License: MIT
+ History

    + 2018-01-23 created by hsz
    + 2018-01-23 version-0.5 by hsz
"""
from typing import (
    Callable,
    Any
)
from pymprpc.errors import (
    UnsupportSysMethodError
)


class Method:
    """将指定的函数名,任务ID通过指定的发送方法,在执行`__call__`后发送给远端服务器.

    特别的是如果name后面有`.xxx`那么最终实际是执行的`name.xxx`
    """
    # some magic to bind an XML-RPC method to an RPC server.
    # supports "nested" methods (e.g. examples.getStateName)

    def __tmp0(__tmp2, __tmp1, __tmp3, ID):
        """初始化对象的私有属性.

        Parameters:
            send (Callable): - 可执行的发送函数,要求参数要有ID和methodname
            name (str): - 要远端执行的函数名
            ID (str):- 要远端执行的任务ID

        """
        # private
        __tmp2.__send = __tmp1
        __tmp2.__name = __tmp3
        __tmp2.__ID = ID

    def __getattr__(__tmp2, __tmp3):
        return Method(
            __tmp1=__tmp2.__send,
            __tmp3="%s.%s" % (__tmp2.__name, __tmp3),
            ID=__tmp2.__ID)

    def __call__(__tmp2, *args, **kwargs: <FILL>):
        """执行发送任务.

        Parameters:
            args (Any): - 远端名字是<name>的函数的位置参数
            kwargs (Any): - 远端名字是<name>的函数的关键字参数

        Return:
            (Any): - 发送函数send的返回值

        """
        sys_method = ("listMethods", "methodSignature",
                      'methodHelp', 'lenConnections',
                      'lenUndoneTasks', 'getresult')
        if __tmp2.__name.startswith("system."):
            if __tmp2.__name.split(".")[-1] not in sys_method:
                raise UnsupportSysMethodError(
                    "UnsupportSysMethod:{}".format(__tmp2.__name), __tmp2.__ID
                )
        return __tmp2.__send(
            __tmp2.__ID,
            __tmp2.__name,
            *args, **kwargs)
