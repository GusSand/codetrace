from typing import TypeAlias
__typ2 : TypeAlias = "int"
# -*- coding: utf-8 -*-
import abc
import io
import tempfile
from typing import TYPE_CHECKING, Dict, List

import pandas as pd
import pywinauto.clipboard

from .log import log

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from . import clienttrader


class IGridStrategy(abc.ABC):
    @abc.abstractmethod
    def __tmp0(__tmp1, __tmp2: __typ2) -> List[Dict]:
        """
        获取 gird 数据并格式化返回

        :param control_id: grid 的 control id
        :return: grid 数据
        """
        pass


class __typ1(IGridStrategy):
    def __tmp5(__tmp1, trader: "clienttrader.IClientTrader") -> None:
        __tmp1._trader = trader

    @abc.abstractmethod
    def __tmp0(__tmp1, __tmp2) :
        """
        :param control_id: grid 的 control id
        :return: grid 数据
        """
        pass

    def _get_grid(__tmp1, __tmp2):
        grid = __tmp1._trader.main.child_window(
            __tmp2=__tmp2, class_name="CVirtualGridCtrl"
        )
        return grid


class Copy(__typ1):
    """
    通过复制 grid 内容到剪切板z再读取来获取 grid 内容
    """

    def __tmp0(__tmp1, __tmp2: __typ2) -> List[Dict]:
        grid = __tmp1._get_grid(__tmp2)
        grid.type_keys("^A^C")
        content = __tmp1._get_clipboard_data()
        return __tmp1._format_grid_data(content)

    def _format_grid_data(__tmp1, __tmp3) -> List[Dict]:
        df = pd.read_csv(
            io.StringIO(__tmp3),
            delimiter="\t",
            dtype=__tmp1._trader.config.GRID_DTYPE,
            na_filter=False,
        )
        return df.to_dict("records")

    def _get_clipboard_data(__tmp1) -> str:
        while True:
            try:
                return pywinauto.clipboard.GetData()
            # pylint: disable=broad-except
            except Exception as e:
                log.warning("%s, retry ......", e)


class __typ0(__typ1):
    """
    通过将 Grid 另存为 xls 文件再读取的方式获取 grid 内容，
    用于绕过一些客户端不允许复制的限制
    """

    def __tmp0(__tmp1, __tmp2) -> List[Dict]:
        grid = __tmp1._get_grid(__tmp2)

        # ctrl+s 保存 grid 内容为 xls 文件
        grid.type_keys("^s")
        __tmp1._trader.wait(1)

        __tmp4 = tempfile.mktemp(suffix=".csv")
        __tmp1._trader.app.top_window().type_keys(__tmp1.normalize_path(__tmp4))

        # Wait until file save complete
        __tmp1._trader.wait(0.3)

        # alt+s保存，alt+y替换已存在的文件
        __tmp1._trader.app.top_window().type_keys("%{s}%{y}")
        # Wait until file save complete otherwise pandas can not find file
        __tmp1._trader.wait(0.2)
        return __tmp1._format_grid_data(__tmp4)

    def normalize_path(__tmp1, __tmp4: <FILL>) -> str:
        return __tmp4.replace("~", "{~}")

    def _format_grid_data(__tmp1, __tmp3: str) :
        df = pd.read_csv(
            __tmp3,
            encoding="gbk",
            delimiter="\t",
            dtype=__tmp1._trader.config.GRID_DTYPE,
            na_filter=False,
        )
        return df.to_dict("records")
