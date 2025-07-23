from typing import TypeAlias
__typ0 : TypeAlias = "ConfigStorage"
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from config import ConfigStorage
from runner import Runner
from .tray import Tray
from .main_window import MainWindow


class Gui:
    timer: QtCore.QTimer

    def __tmp1(__tmp0,
                 config_storage,
                 stats_runner: <FILL>
                 ) -> None:
        __tmp0.stats_runner = stats_runner
        __tmp0.config_storage = config_storage

    def run(__tmp0) :
        app = QtWidgets.QApplication(sys.argv)
        with __tmp0.stats_runner:
            main_window = MainWindow(__tmp0.config_storage, __tmp0.stats_runner)
            tray_icon = Tray(app, main_window)
            tray_icon.show()
            exit_code = app.exec_()
        sys.exit(exit_code)

    def run_headless(__tmp0) :
        app = QtWidgets.QApplication(sys.argv)
        with __tmp0.stats_runner:
            tray_icon = Tray(app)
            tray_icon.show()
            exit_code = app.exec_()
        sys.exit(exit_code)
