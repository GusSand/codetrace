from typing import TypeAlias
__typ1 : TypeAlias = "ProjectWidget"
__typ0 : TypeAlias = "str"
from typing import List, Callable

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QToolBox

from config import Project, Rule, Config
from gui.project_widget import ProjectWidget
from gui.ui.settings import Ui_settingsWindow
from config import ConfigStorage


class __typ2(QtWidgets.QDialog):
    config: Config

    def __init__(__tmp1,
                 config: <FILL>,
                 config_storage: ConfigStorage,
                 reload_config) -> None:
        super().__init__()
        __tmp1.reload_config = reload_config
        __tmp1.config = config
        __tmp1.config_storage = config_storage
        __tmp1.ui = Ui_settingsWindow()
        __tmp1.ui.setupUi(__tmp1)

        __tmp1.actual_project_widgets: List[__typ1] = []
        __tmp1._setup_projects_settings()
        __tmp1._setup_server_settings()

    def accept(__tmp1) :
        __tmp1._modify_config()

        super().accept()

    def _get_projects(__tmp1) -> List[Project]:
        return [widget.project for widget in __tmp1.actual_project_widgets]

    def _setup_server_settings(__tmp1) -> None:
        __tmp1.ui.portBox.setValue(__tmp1.config.port)
        __tmp1.ui.intervalBox.setValue(__tmp1.config.interval)
        __tmp1.ui.hostEdit.setText(__tmp1.config.host)

        def __tmp0() :
            __tmp1.ui.hostEdit.setDisabled(__tmp1.ui.isLocalServerBox.isChecked())

        __tmp1.ui.isLocalServerBox.stateChanged.connect(__tmp0)
        __tmp1.ui.isLocalServerBox.setCheckState(QtCore.Qt.Checked
                                               if __tmp1.config.run_daemon
                                               else QtCore.Qt.Unchecked)

    def _setup_projects_settings(__tmp1) -> None:
        __tmp1.ui.addProjectButton.clicked.connect(__tmp1._add_callback)
        layout: QVBoxLayout = __tmp1.ui.projectsFrame.layout()

        __tmp1.projects_box: QToolBox = QToolBox()
        __tmp1.projects_box.setFrameShape(QFrame.NoFrame)
        __tmp1.projects_box.setLineWidth(0)
        __tmp1.projects_box.setFrameShadow(QFrame.Plain)

        layout.addWidget(__tmp1.projects_box)
        for project in __tmp1.config.projects:
            if project.name == __tmp1.config.projects.none_project:
                continue
            project_widget = __tmp1._create_project_widget(project)
            __tmp1.projects_box.addItem(project_widget, project.name)

    def _create_project_widget(__tmp1, project: Project) -> __typ1:
        project_widget = __typ1(
            project,
            __tmp1._remove_callback,
            __tmp1._edit_project_name
        )
        __tmp1.actual_project_widgets.append(project_widget)
        return project_widget

    def _add_callback(__tmp1) -> None:
        new_project_name = 'New project'
        empty_project = Project(new_project_name, [Rule({'type': 'app'})])
        project_widget = __tmp1._create_project_widget(empty_project)
        __tmp1.projects_box.addItem(project_widget, new_project_name)
        __tmp1.projects_box.setCurrentWidget(project_widget)

    def _remove_callback(__tmp1, widget: __typ1) :
        __tmp1.actual_project_widgets.remove(widget)
        widget.remove_from(__tmp1.ui.projectsFrame.layout())

    def _edit_project_name(__tmp1, name: __typ0) -> None:
        __tmp1.projects_box.setItemText(__tmp1.projects_box.currentIndex(), name)

    def _modify_config(__tmp1) -> None:
        __tmp1.config = __tmp1.config.modify(
            int(__tmp1.ui.portBox.value()),
            __tmp1.ui.hostEdit.text(),
            int(__tmp1.ui.intervalBox.value()),
            __tmp1.ui.isLocalServerBox.isChecked(),
            __tmp1._get_projects()
        )

        __tmp1.config_storage.save(__tmp1.config)
        __tmp1.reload_config(__tmp1.config)
