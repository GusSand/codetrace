from typing import TypeAlias
__typ0 : TypeAlias = "ConfigStorage"
from typing import List
from PyQt5 import QtWidgets
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QListWidgetItem, QVBoxLayout
from analyze.matched_event import MatchedEvent
from gui.main_page_widget import MainPageWidget
from gui.ui.main import Ui_Main
from config import ConfigStorage
from runner import Runner

WidgetItems = List[QListWidgetItem]


class MainWindow(QtWidgets.QMainWindow):
    ui: Ui_Main
    last_matched_events: List[MatchedEvent]

    def __init__(__tmp0,
                 config_storage: __typ0,
                 stats_runner: <FILL>
                 ) :
        super().__init__()
        __tmp0.stats_runner = stats_runner
        __tmp0.config = config_storage.load()
        __tmp0.config_storage = config_storage
        __tmp0.ui = Ui_Main()
        __tmp0.ui.setupUi(__tmp0)

        __tmp0.last_matched_events = []

        __tmp0._setup_main_widget()

    def closeEvent(__tmp0, event) :
        event.ignore()
        __tmp0.hide()

    def _setup_main_widget(__tmp0) :
        __tmp0.main_page_widget = MainPageWidget(
            __tmp0.config_storage,
            __tmp0.stats_runner.reload
        )
        layout: QVBoxLayout = __tmp0.ui.tabChart.layout()
        layout.addWidget(__tmp0.main_page_widget)
