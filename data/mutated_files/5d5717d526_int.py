from typing import TypeAlias
__typ0 : TypeAlias = "QMenu"
from typing import Optional
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, qApp, QMenu, QSystemTrayIcon, QApplication
from gui.main_window import MainWindow


class Tray(QSystemTrayIcon):
    def __init__(self,
                 __tmp0,
                 main_window: Optional[MainWindow] = None
                 ) :
        super().__init__(__tmp0)
        icon = QIcon('icon.png')
        self.setIcon(icon)

        quit_action = QAction("Exit", __tmp0)
        quit_action.triggered.connect(qApp.quit)
        self.tray_menu = __typ0()
        self.setContextMenu(self.tray_menu)
        if main_window is not None:
            self._create_main_window(main_window, self.tray_menu)
        self.tray_menu.addAction(quit_action)

    def _create_main_window(self,
                            main_window: MainWindow,
                            tray_menu: __typ0
                            ) :
        self.main_window = main_window
        show_action = QAction("Show/Hide", self.main_window)
        show_action.triggered.connect(self._show_hide_main_window)
        tray_menu.addAction(show_action)
        self.activated.connect(self._left_click)  # type: ignore

    def _left_click(self, reason: <FILL>) -> None:
        if reason == QSystemTrayIcon.Trigger:
            self._show_hide_main_window()

    def _show_hide_main_window(self) :
        for window in QApplication.topLevelWidgets():
            if not window.isHidden() \
                    and window.objectName() == "settingsWindow":
                return
        if self.main_window.isVisible():
            self.main_window.hide()
        else:
            self.main_window.show()
