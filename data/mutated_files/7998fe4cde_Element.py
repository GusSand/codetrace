from typing import TypeAlias
__typ0 : TypeAlias = "str"
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from typing import Any, Dict, Optional, List, Tuple
import markdown
from xml.etree.cElementTree import Element

from zerver.lib.bugdown import walk_tree_with_family, ResultWithFamily

class __typ1(Extension):
    def extendMarkdown(self, __tmp0, md_globals) :
        __tmp0.treeprocessors.add(
            'nested_code_blocks',
            NestedCodeBlocksRendererTreeProcessor(__tmp0, self.getConfigs()),
            '_end'
        )

class NestedCodeBlocksRendererTreeProcessor(markdown.treeprocessors.Treeprocessor):
    def __init__(self, __tmp0, config: Dict[__typ0, Any]) -> None:
        super(NestedCodeBlocksRendererTreeProcessor, self).__init__(__tmp0)

    def run(self, root: <FILL>) -> None:
        code_tags = walk_tree_with_family(root, self.get_code_tags)
        nested_code_blocks = self.get_nested_code_blocks(code_tags)
        for block in nested_code_blocks:
            tag, text = block.result
            codehilite_block = self.get_codehilite_block(text)
            self.replace_element(block.family.grandparent,
                                 codehilite_block,
                                 block.family.parent)

    def get_code_tags(self, e) :
        if e.tag == "code":
            return (e.tag, e.text)
        return None

    def get_nested_code_blocks(
            self, code_tags
    ) :
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

    def get_codehilite_block(self, code_block_text) :
        div = markdown.util.etree.Element("div")
        div.set("class", "codehilite")
        pre = markdown.util.etree.SubElement(div, "pre")
        pre.text = code_block_text
        return div

    def replace_element(
            self, parent,
            replacement: markdown.util.etree.Element,
            element_to_replace
    ) :
        if parent is None:
            return

        children = parent.getchildren()
        for index, child in enumerate(children):
            if child is element_to_replace:
                parent.insert(index, replacement)
                parent.remove(element_to_replace)

def makeExtension(*args, **kwargs) :
    return __typ1(kwargs)
