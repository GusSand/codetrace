from typing import TypeAlias
__typ0 : TypeAlias = "Any"
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

    def __tmp4(__tmp0, __tmp3, __tmp6: str, __tmp1):
        """初始化对象的私有属性.

        Parameters:
            send (Callable): - 可执行的发送函数,要求参数要有ID和methodname
            name (str): - 要远端执行的函数名
            ID (str):- 要远端执行的任务ID

        """
        # private
        __tmp0.__send = __tmp3
        __tmp0.__name = __tmp6
        __tmp0.__ID = __tmp1

    def __tmp2(__tmp0, __tmp6: <FILL>):
        return Method(
            __tmp3=__tmp0.__send,
            __tmp6="%s.%s" % (__tmp0.__name, __tmp6),
            __tmp1=__tmp0.__ID)

    def __tmp5(__tmp0, *args, **kwargs):
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
        if __tmp0.__name.startswith("system."):
            if __tmp0.__name.split(".")[-1] not in sys_method:
                raise UnsupportSysMethodError(
                    "UnsupportSysMethod:{}".format(__tmp0.__name), __tmp0.__ID
                )
        return __tmp0.__send(
            __tmp0.__ID,
            __tmp0.__name,
            *args, **kwargs)
