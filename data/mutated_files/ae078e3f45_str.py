from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from typing import Any, Dict, Optional, List, Tuple
import markdown
from xml.etree.cElementTree import Element

from zerver.lib.bugdown import walk_tree_with_family, ResultWithFamily

class NestedCodeBlocksRenderer(Extension):
    def extendMarkdown(__tmp1, md: markdown.Markdown, md_globals: Dict[str, Any]) -> None:
        md.treeprocessors.add(
            'nested_code_blocks',
            __typ0(md, __tmp1.getConfigs()),
            '_end'
        )

class __typ0(markdown.treeprocessors.Treeprocessor):
    def __init__(__tmp1, md: markdown.Markdown, __tmp2: Dict[str, Any]) -> None:
        super(__typ0, __tmp1).__init__(md)

    def run(__tmp1, __tmp0: Element) -> None:
        code_tags = walk_tree_with_family(__tmp0, __tmp1.get_code_tags)
        nested_code_blocks = __tmp1.get_nested_code_blocks(code_tags)
        for block in nested_code_blocks:
            tag, text = block.result
            codehilite_block = __tmp1.get_codehilite_block(text)
            __tmp1.replace_element(block.family.grandparent,
                                 codehilite_block,
                                 block.family.parent)

    def get_code_tags(__tmp1, e: Element) -> Optional[Tuple[str, Optional[str]]]:
        if e.tag == "code":
            return (e.tag, e.text)
        return None

    def get_nested_code_blocks(
            __tmp1, code_tags: List[ResultWithFamily]
    ) -> List[ResultWithFamily]:
        nested_code_blocks = []
        for code_tag in code_tags:
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

    def get_codehilite_block(__tmp1, code_block_text: <FILL>) :
        div = markdown.util.etree.Element("div")
        div.set("class", "codehilite")
        pre = markdown.util.etree.SubElement(div, "pre")
        pre.text = code_block_text
        return div

    def replace_element(
            __tmp1, parent: Optional[Element],
            replacement: markdown.util.etree.Element,
            element_to_replace: Element
    ) -> None:
        if parent is None:
            return

        children = parent.getchildren()
        for index, child in enumerate(children):
            if child is element_to_replace:
                parent.insert(index, replacement)
                parent.remove(element_to_replace)

def makeExtension(*args: Any, **kwargs: str) -> NestedCodeBlocksRenderer:
    return NestedCodeBlocksRenderer(kwargs)
