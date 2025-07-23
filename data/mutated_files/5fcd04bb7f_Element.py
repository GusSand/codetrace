from typing import TypeAlias
__typ3 : TypeAlias = "Any"
__typ1 : TypeAlias = "str"
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from typing import Any, Dict, Optional, List, Tuple
import markdown
from xml.etree.cElementTree import Element

from zerver.lib.bugdown import walk_tree_with_family, ResultWithFamily

class __typ2(Extension):
    def __tmp4(__tmp1, __tmp7, __tmp2: Dict[__typ1, __typ3]) :
        __tmp7.treeprocessors.add(
            'nested_code_blocks',
            __typ0(__tmp7, __tmp1.getConfigs()),
            '_end'
        )

class __typ0(markdown.treeprocessors.Treeprocessor):
    def __init__(__tmp1, __tmp7: markdown.Markdown, __tmp10: Dict[__typ1, __typ3]) :
        super(__typ0, __tmp1).__init__(__tmp7)

    def __tmp9(__tmp1, __tmp5) :
        __tmp8 = walk_tree_with_family(__tmp5, __tmp1.get_code_tags)
        nested_code_blocks = __tmp1.get_nested_code_blocks(__tmp8)
        for block in nested_code_blocks:
            tag, text = block.result
            codehilite_block = __tmp1.get_codehilite_block(text)
            __tmp1.replace_element(block.family.grandparent,
                                 codehilite_block,
                                 block.family.parent)

    def get_code_tags(__tmp1, e: <FILL>) -> Optional[Tuple[__typ1, Optional[__typ1]]]:
        if e.tag == "code":
            return (e.tag, e.text)
        return None

    def get_nested_code_blocks(
            __tmp1, __tmp8: List[ResultWithFamily]
    ) :
        nested_code_blocks = []
        for code_tag in __tmp8:
            parent = code_tag.family.parent  # type: Any
            grandparent = code_tag.family.grandparent  # type: Any
            if parent.tag == "p" and grandparent.tag == "li":
                # if the parent (<p>) has no text, and no children,
                # that means that the <code> element inside is its
                # only thing inside the bullet, we can confidently say
                # that this is a nested code block
                if parent.text is None and len(list(parent)) == 1 and len(list(parent.itertext())) == 1:
                    nested_code_blocks.append(code_tag)

        return nested_code_blocks

    def get_codehilite_block(__tmp1, __tmp11: __typ1) -> Element:
        div = markdown.util.etree.Element("div")
        div.set("class", "codehilite")
        pre = markdown.util.etree.SubElement(div, "pre")
        pre.text = __tmp11
        return div

    def replace_element(
            __tmp1, parent: Optional[Element],
            __tmp3,
            __tmp6
    ) -> None:
        if parent is None:
            return

        children = parent.getchildren()
        for index, child in enumerate(children):
            if child is __tmp6:
                parent.insert(index, __tmp3)
                parent.remove(__tmp6)

def __tmp0(*args: __typ3, **kwargs: __typ1) -> __typ2:
    return __typ2(kwargs)
