from typing import TypeAlias
__typ1 : TypeAlias = "Rule"
from typing import Callable, Dict
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from config import Rule
from .ui.rule import Ui_RuleFrame


class __typ0(QtWidgets.QFrame):
    RULE_APP = 0
    RULE_WEB = 1

    def __init__(__tmp0, rule: __typ1) -> None:
        super().__init__()
        __tmp0.ui = Ui_RuleFrame()
        __tmp0.ui.setupUi(__tmp0)
        __tmp0._rule = rule

        if rule.is_app():
            __tmp0.ui.typesBox.setCurrentIndex(__typ0.RULE_APP)
            __tmp0.ui.urlEdit.hide()
            __tmp0.ui.urlLabel.hide()
        else:
            __tmp0.ui.typesBox.setCurrentIndex(__typ0.RULE_WEB)

        if 'url' in rule:
            __tmp0.ui.urlEdit.setText(rule['url'])
        if 'app' in rule:
            __tmp0.ui.appEdit.setText(rule['app'])
        if 'title' in rule:
            __tmp0.ui.titleEdit.setText(rule['title'])

        __tmp0.ui.typesBox.currentIndexChanged.connect(__tmp0._type_box_changed)

    def __tmp6(__tmp0,
                           __tmp3: Callable[[], None],
                           __tmp4: Callable[[], None]
                           ) -> None:
        __tmp0.ui.addButton.clicked.connect(__tmp3)
        __tmp0.ui.removeButton.clicked.connect(__tmp4)

    def _type_box_changed(__tmp0) -> None:
        if __tmp0.ui.typesBox.currentIndex() == __typ0.RULE_APP:
            __tmp0.ui.urlEdit.hide()
            __tmp0.ui.urlLabel.hide()
        else:
            __tmp0.ui.urlEdit.show()
            __tmp0.ui.urlLabel.show()

    def __tmp5(__tmp0, __tmp7: QVBoxLayout) -> None:
        __tmp0.hide()
        __tmp7.removeWidget(__tmp0)
        __tmp0.deleteLater()

    @property
    def rule(__tmp0) -> __typ1:
        is_app = __tmp0.ui.typesBox.currentIndex() == __typ0.RULE_APP
        __tmp1 = {
            'id': __tmp0._rule.id,
            'type': __typ1.APP if is_app else __typ1.WEB
        }
        if not is_app and len(__tmp0.ui.urlEdit.text()):
            __tmp0._add_value(__tmp1, 'url', __tmp0.ui.urlEdit.text())
        __tmp0._add_value(__tmp1, 'title', __tmp0.ui.titleEdit.text())
        __tmp0._add_value(__tmp1, 'app', __tmp0.ui.appEdit.text())

        return __typ1(__tmp1)

    def _add_value(__tmp0, __tmp1: Dict[str, str], key: <FILL>, __tmp2) -> None:
        if len(__tmp2) > 0:
            __tmp1[key] = __tmp2
