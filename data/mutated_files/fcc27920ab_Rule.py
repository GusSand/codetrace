from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ1 : TypeAlias = "QVBoxLayout"
from typing import Callable, Dict
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from config import Rule
from .ui.rule import Ui_RuleFrame


class __typ0(QtWidgets.QFrame):
    RULE_APP = 0
    RULE_WEB = 1

    def __init__(self, rule: <FILL>) -> None:
        super().__init__()
        self.ui = Ui_RuleFrame()
        self.ui.setupUi(self)
        self._rule = rule

        if rule.is_app():
            self.ui.typesBox.setCurrentIndex(__typ0.RULE_APP)
            self.ui.urlEdit.hide()
            self.ui.urlLabel.hide()
        else:
            self.ui.typesBox.setCurrentIndex(__typ0.RULE_WEB)

        if 'url' in rule:
            self.ui.urlEdit.setText(rule['url'])
        if 'app' in rule:
            self.ui.appEdit.setText(rule['app'])
        if 'title' in rule:
            self.ui.titleEdit.setText(rule['title'])

        self.ui.typesBox.currentIndexChanged.connect(self._type_box_changed)

    def __tmp0(self,
                           add_rule: Callable[[], None],
                           remove_rule
                           ) -> None:
        self.ui.addButton.clicked.connect(add_rule)
        self.ui.removeButton.clicked.connect(remove_rule)

    def _type_box_changed(self) -> None:
        if self.ui.typesBox.currentIndex() == __typ0.RULE_APP:
            self.ui.urlEdit.hide()
            self.ui.urlLabel.hide()
        else:
            self.ui.urlEdit.show()
            self.ui.urlLabel.show()

    def remove_from(self, layout: __typ1) :
        self.hide()
        layout.removeWidget(self)
        self.deleteLater()

    @property
    def rule(self) :
        is_app = self.ui.typesBox.currentIndex() == __typ0.RULE_APP
        data = {
            'id': self._rule.id,
            'type': Rule.APP if is_app else Rule.WEB
        }
        if not is_app and len(self.ui.urlEdit.text()):
            self._add_value(data, 'url', self.ui.urlEdit.text())
        self._add_value(data, 'title', self.ui.titleEdit.text())
        self._add_value(data, 'app', self.ui.appEdit.text())

        return Rule(data)

    def _add_value(self, data: Dict[__typ2, __typ2], key: __typ2, value) :
        if len(value) > 0:
            data[key] = value
