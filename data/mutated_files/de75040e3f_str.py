
from typing import cast, Any

import sys
import unittest

try:
    from tools.lib.css_parser import (
        CssParserException,
        CssSection,
        parse,
    )
except ImportError:
    print('ERROR!!! You need to run this via tools/test-tools.')
    sys.exit(1)

class ParserTestHappyPath(unittest.TestCase):
    def __tmp2(__tmp1) -> None:
        my_selector = 'li.foo'
        my_block = '''{
                color: red;
            }'''
        my_css = my_selector + ' ' + my_block
        res = parse(my_css)
        __tmp1.assertEqual(res.text().strip(), 'li.foo {\n    color: red;\n}')
        section = cast(CssSection, res.sections[0])
        block = section.declaration_block
        __tmp1.assertEqual(block.text().strip(), '{\n    color: red;\n}')
        declaration = block.declarations[0]
        __tmp1.assertEqual(declaration.css_property, 'color')
        __tmp1.assertEqual(declaration.css_value.text().strip(), 'red')

    def __tmp3(__tmp1) -> None:
        my_css = '''
            li.hide {
                display: none; /* comment here */
                /* Not to be confused
                   with this comment */
                color: green;
            }'''
        res = parse(my_css)
        section = cast(CssSection, res.sections[0])
        block = section.declaration_block
        declaration = block.declarations[0]
        __tmp1.assertIn('/* comment here */', declaration.text())

    def test_no_semicolon(__tmp1) -> None:
        my_css = '''
            p { color: red }
        '''

        reformatted_css = 'p {\n    color: red;\n}'

        res = parse(my_css)

        __tmp1.assertEqual(res.text().strip(), reformatted_css)

        section = cast(CssSection, res.sections[0])

        __tmp1.assertFalse(section.declaration_block.declarations[0].semicolon)

    def __tmp9(__tmp1) -> None:
        my_css = '''
            div {
            }'''
        __tmp6 = 'Empty declaration'
        with __tmp1.assertRaisesRegex(CssParserException, __tmp6):
            parse(my_css)

    def __tmp5(__tmp1) :
        my_css = '''
            h1,
            h2,
            h3 {
                top: 0
            }'''
        res = parse(my_css)
        section = res.sections[0]
        selectors = section.selector_list.selectors
        __tmp1.assertEqual(len(selectors), 3)

    def __tmp10(__tmp1) -> None:
        my_css = '''
            @media (max-width: 300px) {
                h5 {
                    margin: 0;
                }
            }'''
        res = parse(my_css)
        __tmp1.assertEqual(len(res.sections), 1)
        expected = '@media (max-width: 300px) {\n    h5 {\n        margin: 0;\n    }\n}'
        __tmp1.assertEqual(res.text().strip(), expected)

class ParserTestSadPath(unittest.TestCase):
    '''
    Use this class for tests that verify the parser will
    appropriately choke on malformed CSS.

    We prevent some things that are technically legal
    in CSS, like having comments in the middle of list
    of selectors.  Some of this is just for expediency;
    some of this is to enforce consistent formatting.
    '''
    def _assert_error(__tmp1, my_css: str, __tmp6: <FILL>) :
        with __tmp1.assertRaisesRegex(CssParserException, __tmp6):
            parse(my_css)

    def __tmp4(__tmp1) :
        my_css = '''
            @media (max-width: 975px) {
                body {
                    color: red;
                }
            }} /* whoops */'''
        __tmp6 = 'unexpected }'
        __tmp1._assert_error(my_css, __tmp6)

    def __tmp8(__tmp1) -> None:
        my_css = '''

            /* nothing to see here, move along */
            '''
        __tmp6 = 'unexpected empty section'
        __tmp1._assert_error(my_css, __tmp6)

    def test_missing_colon(__tmp1) -> None:
        my_css = '''
            .hide
            {
                display none /* no colon here */
            }'''
        __tmp6 = 'We expect a colon here'
        __tmp1._assert_error(my_css, __tmp6)

    def __tmp0(__tmp1) :
        my_css = ''' /* comment with no end'''
        __tmp6 = 'unclosed comment'
        __tmp1._assert_error(my_css, __tmp6)

    def __tmp11(__tmp1) -> None:
        my_css = '''
            /* no selectors here */
            {
                bottom: 0
            }'''
        __tmp6 = 'Missing selector'
        __tmp1._assert_error(my_css, __tmp6)

    def __tmp7(__tmp1) -> None:
        my_css = '''
            h1
            {
                bottom:
            }'''
        __tmp6 = 'Missing value'
        __tmp1._assert_error(my_css, __tmp6)

    def test_disallow_comments_in_selectors(__tmp1) -> None:
        my_css = '''
            h1,
            h2, /* comment here not allowed by Zulip */
            h3 {
                top: 0
            }'''
        __tmp6 = 'Comments in selector section are not allowed'
        __tmp1._assert_error(my_css, __tmp6)
