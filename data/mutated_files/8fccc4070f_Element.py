from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from typing import Any, Dict, Optional, List, Tuple
import markdown
from xml.etree.cElementTree import Element

from zerver.lib.bugdown import walk_tree_with_family, ResultWithFamily

class __typ0(Extension):
    def __tmp2(__tmp0, md: markdown.Markdown, __tmp6: Dict[str, Any]) -> None:
        md.treeprocessors.add(
            'nested_code_blocks',
            NestedCodeBlocksRendererTreeProcessor(md, __tmp0.getConfigs()),
            '_end'
        )

class NestedCodeBlocksRendererTreeProcessor(markdown.treeprocessors.Treeprocessor):
    def __init__(__tmp0, md: markdown.Markdown, __tmp4: Dict[str, Any]) -> None:
        super(NestedCodeBlocksRendererTreeProcessor, __tmp0).__init__(md)

    def run(__tmp0, __tmp3) -> None:
        __tmp5 = walk_tree_with_family(__tmp3, __tmp0.get_code_tags)
        nested_code_blocks = __tmp0.get_nested_code_blocks(__tmp5)
        for block in nested_code_blocks:
            tag, text = block.result
            codehilite_block = __tmp0.get_codehilite_block(text)
            __tmp0.replace_element(block.family.grandparent,
                                 codehilite_block,
                                 block.family.parent)

    def get_code_tags(__tmp0, e) -> Optional[Tuple[str, Optional[str]]]:
        if e.tag == "code":
            return (e.tag, e.text)
        return None

    def get_nested_code_blocks(
            __tmp0, __tmp5: List[ResultWithFamily]
    ) -> List[ResultWithFamily]:
        nested_code_blocks = []
        for code_tag in __tmp5:
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

    def get_codehilite_block(__tmp0, code_block_text: str) :
        div = markdown.util.etree.Element("div")
        div.set("class", "codehilite")
        pre = markdown.util.etree.SubElement(div, "pre")
        pre.text = code_block_text
        return div

    def replace_element(
            __tmp0, parent: Optional[Element],
            __tmp1: markdown.util.etree.Element,
            element_to_replace: <FILL>
    ) -> None:
        if parent is None:
            return

        children = parent.getchildren()
        for index, child in enumerate(children):
            if child is element_to_replace:
                parent.insert(index, __tmp1)
                parent.remove(element_to_replace)

def makeExtension(*args: Any, **kwargs: str) -> __typ0:
    return __typ0(kwargs)
