from typing import TypeAlias
__typ3 : TypeAlias = "Rule"
__typ2 : TypeAlias = "QVBoxLayout"
__typ0 : TypeAlias = "RuleWidget"
from typing import Callable, List

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from config import Project, Rule
from gui.rule_widget import RuleWidget
from .ui.project import Ui_ProjectFrame


class __typ1(QtWidgets.QFrame):
    def __init__(
            __tmp0,
            project: <FILL>,
            on_remove_rule: Callable[['ProjectWidget'], None],
            on_edit_project_name,
    ) -> None:
        super().__init__()
        __tmp0.ui = Ui_ProjectFrame()
        __tmp0.ui.setupUi(__tmp0)
        __tmp0.ui.nameEdit.setText(project.name)
        __tmp0._setup_rules(project)

        __tmp0.ui.removeButton.clicked.connect(
            lambda: on_remove_rule(__tmp0)
        )
        __tmp0.ui.nameEdit.textChanged.connect(on_edit_project_name)

    def _setup_rules(__tmp0, project) :
        layout: __typ2 = __tmp0.ui.rulesBox.layout()
        for rule in project.rules:
            rule_widget = __tmp0._create_rule_widget(layout, rule)
            layout.addWidget(rule_widget)

    def _create_rule_widget(__tmp0,
                            layout,
                            rule
                            ) :
        rule_widget = __typ0(rule)
        rule_widget.register_callbacks(
            lambda: layout.insertWidget(
                layout.indexOf(rule_widget),
                __tmp0._create_rule_widget(layout, __typ3({"type": "app"}))
            ),
            lambda: rule_widget.remove_from(layout)
        )

        return rule_widget

    def remove_from(__tmp0, layout) -> None:
        __tmp0.hide()
        layout.removeWidget(__tmp0)
        __tmp0.deleteLater()

    @property
    def project(__tmp0) :
        name = __tmp0.ui.nameEdit.text()
        layout: __typ2 = __tmp0.ui.rulesBox.layout()
        rule_widgets: List[__typ0] = []
        for i in range(0, layout.count()):
            widget = layout.itemAt(i).widget()
            assert isinstance(widget, __typ0)
            rule_widgets.append(widget)
        return Project(name, [rule_widget.rule
                              for rule_widget
                              in rule_widgets])
