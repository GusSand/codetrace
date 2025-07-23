from typing import TypeAlias
__typ0 : TypeAlias = "QVBoxLayout"
from typing import Callable, Dict
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from config import Rule
from .ui.rule import Ui_RuleFrame


class RuleWidget(QtWidgets.QFrame):
    RULE_APP = 0
    RULE_WEB = 1

    def __init__(__tmp0, rule: Rule) -> None:
        super().__init__()
        __tmp0.ui = Ui_RuleFrame()
        __tmp0.ui.setupUi(__tmp0)
        __tmp0._rule = rule

        if rule.is_app():
            __tmp0.ui.typesBox.setCurrentIndex(RuleWidget.RULE_APP)
            __tmp0.ui.urlEdit.hide()
            __tmp0.ui.urlLabel.hide()
        else:
            __tmp0.ui.typesBox.setCurrentIndex(RuleWidget.RULE_WEB)

        if 'url' in rule:
            __tmp0.ui.urlEdit.setText(rule['url'])
        if 'app' in rule:
            __tmp0.ui.appEdit.setText(rule['app'])
        if 'title' in rule:
            __tmp0.ui.titleEdit.setText(rule['title'])

        __tmp0.ui.typesBox.currentIndexChanged.connect(__tmp0._type_box_changed)

    def register_callbacks(__tmp0,
                           __tmp1: Callable[[], None],
                           __tmp3: Callable[[], None]
                           ) :
        __tmp0.ui.addButton.clicked.connect(__tmp1)
        __tmp0.ui.removeButton.clicked.connect(__tmp3)

    def _type_box_changed(__tmp0) -> None:
        if __tmp0.ui.typesBox.currentIndex() == RuleWidget.RULE_APP:
            __tmp0.ui.urlEdit.hide()
            __tmp0.ui.urlLabel.hide()
        else:
            __tmp0.ui.urlEdit.show()
            __tmp0.ui.urlLabel.show()

    def __tmp4(__tmp0, __tmp5: __typ0) :
        __tmp0.hide()
        __tmp5.removeWidget(__tmp0)
        __tmp0.deleteLater()

    @property
    def rule(__tmp0) :
        is_app = __tmp0.ui.typesBox.currentIndex() == RuleWidget.RULE_APP
        data = {
            'id': __tmp0._rule.id,
            'type': Rule.APP if is_app else Rule.WEB
        }
        if not is_app and len(__tmp0.ui.urlEdit.text()):
            __tmp0._add_value(data, 'url', __tmp0.ui.urlEdit.text())
        __tmp0._add_value(data, 'title', __tmp0.ui.titleEdit.text())
        __tmp0._add_value(data, 'app', __tmp0.ui.appEdit.text())

        return Rule(data)

    def _add_value(__tmp0, data: Dict[str, str], __tmp6, __tmp2: <FILL>) -> None:
        if len(__tmp2) > 0:
            data[__tmp6] = __tmp2
