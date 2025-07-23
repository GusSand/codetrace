from typing import TypeAlias
__typ1 : TypeAlias = "Project"
__typ0 : TypeAlias = "ConfigStorage"
from typing import List, Callable

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QToolBox

from config import Project, Rule, Config
from gui.project_widget import ProjectWidget
from gui.ui.settings import Ui_settingsWindow
from config import ConfigStorage


class SettingsWindow(QtWidgets.QDialog):
    config: Config

    def __init__(__tmp0,
                 config,
                 config_storage,
                 reload_config: Callable[[Config], None]) :
        super().__init__()
        __tmp0.reload_config = reload_config
        __tmp0.config = config
        __tmp0.config_storage = config_storage
        __tmp0.ui = Ui_settingsWindow()
        __tmp0.ui.setupUi(__tmp0)

        __tmp0.actual_project_widgets: List[ProjectWidget] = []
        __tmp0._setup_projects_settings()
        __tmp0._setup_server_settings()

    def accept(__tmp0) :
        __tmp0._modify_config()

        super().accept()

    def _get_projects(__tmp0) :
        return [widget.project for widget in __tmp0.actual_project_widgets]

    def _setup_server_settings(__tmp0) :
        __tmp0.ui.portBox.setValue(__tmp0.config.port)
        __tmp0.ui.intervalBox.setValue(__tmp0.config.interval)
        __tmp0.ui.hostEdit.setText(__tmp0.config.host)

        def _state_changed() :
            __tmp0.ui.hostEdit.setDisabled(__tmp0.ui.isLocalServerBox.isChecked())

        __tmp0.ui.isLocalServerBox.stateChanged.connect(_state_changed)
        __tmp0.ui.isLocalServerBox.setCheckState(QtCore.Qt.Checked
                                               if __tmp0.config.run_daemon
                                               else QtCore.Qt.Unchecked)

    def _setup_projects_settings(__tmp0) :
        __tmp0.ui.addProjectButton.clicked.connect(__tmp0._add_callback)
        layout: QVBoxLayout = __tmp0.ui.projectsFrame.layout()

        __tmp0.projects_box: QToolBox = QToolBox()
        __tmp0.projects_box.setFrameShape(QFrame.NoFrame)
        __tmp0.projects_box.setLineWidth(0)
        __tmp0.projects_box.setFrameShadow(QFrame.Plain)

        layout.addWidget(__tmp0.projects_box)
        for project in __tmp0.config.projects:
            if project.name == __tmp0.config.projects.none_project:
                continue
            project_widget = __tmp0._create_project_widget(project)
            __tmp0.projects_box.addItem(project_widget, project.name)

    def _create_project_widget(__tmp0, project) :
        project_widget = ProjectWidget(
            project,
            __tmp0._remove_callback,
            __tmp0._edit_project_name
        )
        __tmp0.actual_project_widgets.append(project_widget)
        return project_widget

    def _add_callback(__tmp0) :
        new_project_name = 'New project'
        empty_project = __typ1(new_project_name, [Rule({'type': 'app'})])
        project_widget = __tmp0._create_project_widget(empty_project)
        __tmp0.projects_box.addItem(project_widget, new_project_name)
        __tmp0.projects_box.setCurrentWidget(project_widget)

    def _remove_callback(__tmp0, widget: ProjectWidget) :
        __tmp0.actual_project_widgets.remove(widget)
        widget.remove_from(__tmp0.ui.projectsFrame.layout())

    def _edit_project_name(__tmp0, name: <FILL>) -> None:
        __tmp0.projects_box.setItemText(__tmp0.projects_box.currentIndex(), name)

    def _modify_config(__tmp0) :
        __tmp0.config = __tmp0.config.modify(
            int(__tmp0.ui.portBox.value()),
            __tmp0.ui.hostEdit.text(),
            int(__tmp0.ui.intervalBox.value()),
            __tmp0.ui.isLocalServerBox.isChecked(),
            __tmp0._get_projects()
        )

        __tmp0.config_storage.save(__tmp0.config)
        __tmp0.reload_config(__tmp0.config)
