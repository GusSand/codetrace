from typing import TypeAlias
__typ1 : TypeAlias = "int"
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


class __typ0(abc.ABC):
    @abc.abstractmethod
    def get(__tmp0, __tmp1) :
        """
        获取 gird 数据并格式化返回

        :param control_id: grid 的 control id
        :return: grid 数据
        """
        pass


class BaseStrategy(__typ0):
    def __init__(__tmp0, trader) :
        __tmp0._trader = trader

    @abc.abstractmethod
    def get(__tmp0, __tmp1) -> List[Dict]:
        """
        :param control_id: grid 的 control id
        :return: grid 数据
        """
        pass

    def _get_grid(__tmp0, __tmp1: __typ1):
        grid = __tmp0._trader.main.child_window(
            __tmp1=__tmp1, class_name="CVirtualGridCtrl"
        )
        return grid


class Copy(BaseStrategy):
    """
    通过复制 grid 内容到剪切板z再读取来获取 grid 内容
    """

    def get(__tmp0, __tmp1) :
        grid = __tmp0._get_grid(__tmp1)
        grid.type_keys("^A^C")
        content = __tmp0._get_clipboard_data()
        return __tmp0._format_grid_data(content)

    def _format_grid_data(__tmp0, __tmp2) :
        df = pd.read_csv(
            io.StringIO(__tmp2),
            delimiter="\t",
            dtype=__tmp0._trader.config.GRID_DTYPE,
            na_filter=False,
        )
        return df.to_dict("records")

    def _get_clipboard_data(__tmp0) :
        while True:
            try:
                return pywinauto.clipboard.GetData()
            # pylint: disable=broad-except
            except Exception as e:
                log.warning("%s, retry ......", e)


class Xls(BaseStrategy):
    """
    通过将 Grid 另存为 xls 文件再读取的方式获取 grid 内容，
    用于绕过一些客户端不允许复制的限制
    """

    def get(__tmp0, __tmp1: __typ1) :
        grid = __tmp0._get_grid(__tmp1)

        # ctrl+s 保存 grid 内容为 xls 文件
        grid.type_keys("^s")
        __tmp0._trader.wait(1)

        temp_path = tempfile.mktemp(suffix=".csv")
        __tmp0._trader.app.top_window().type_keys(__tmp0.normalize_path(temp_path))

        # Wait until file save complete
        __tmp0._trader.wait(0.3)

        # alt+s保存，alt+y替换已存在的文件
        __tmp0._trader.app.top_window().type_keys("%{s}%{y}")
        # Wait until file save complete otherwise pandas can not find file
        __tmp0._trader.wait(0.2)
        return __tmp0._format_grid_data(temp_path)

    def normalize_path(__tmp0, temp_path) :
        return temp_path.replace("~", "{~}")

    def _format_grid_data(__tmp0, __tmp2: <FILL>) :
        df = pd.read_csv(
            __tmp2,
            encoding="gbk",
            delimiter="\t",
            dtype=__tmp0._trader.config.GRID_DTYPE,
            na_filter=False,
        )
        return df.to_dict("records")
