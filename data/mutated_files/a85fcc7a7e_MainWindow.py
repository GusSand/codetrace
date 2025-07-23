from typing import TypeAlias
__typ1 : TypeAlias = "Tray"
__typ0 : TypeAlias = "int"
from typing import Optional
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, qApp, QMenu, QSystemTrayIcon, QApplication
from gui.main_window import MainWindow


class __typ1(QSystemTrayIcon):
    def __init__(__tmp0,
                 parent: QtCore.QObject,
                 main_window: Optional[MainWindow] = None
                 ) :
        super().__init__(parent)
        icon = QIcon('icon.png')
        __tmp0.setIcon(icon)

        quit_action = QAction("Exit", parent)
        quit_action.triggered.connect(qApp.quit)
        __tmp0.tray_menu = QMenu()
        __tmp0.setContextMenu(__tmp0.tray_menu)
        if main_window is not None:
            __tmp0._create_main_window(main_window, __tmp0.tray_menu)
        __tmp0.tray_menu.addAction(quit_action)

    def _create_main_window(__tmp0,
                            main_window: <FILL>,
                            tray_menu
                            ) :
        __tmp0.main_window = main_window
        show_action = QAction("Show/Hide", __tmp0.main_window)
        show_action.triggered.connect(__tmp0._show_hide_main_window)
        tray_menu.addAction(show_action)
        __tmp0.activated.connect(__tmp0._left_click)  # type: ignore

    def _left_click(__tmp0, __tmp1: __typ0) :
        if __tmp1 == QSystemTrayIcon.Trigger:
            __tmp0._show_hide_main_window()

    def _show_hide_main_window(__tmp0) :
        for window in QApplication.topLevelWidgets():
            if not window.isHidden() \
                    and window.objectName() == "settingsWindow":
                return
        if __tmp0.main_window.isVisible():
            __tmp0.main_window.hide()
        else:
            __tmp0.main_window.show()
