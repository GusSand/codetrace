#!/usr/bin/env python3
import os
import sys
import zulip_bots.run
from zulip_bots.lib import extract_query_without_mention
import unittest
from typing import Optional
from unittest import TestCase

from unittest import mock
from unittest.mock import patch


class __typ0(TestCase):

    our_dir = os.path.dirname(__file__)
    path_to_bot = os.path.abspath(os.path.join(our_dir, '../bots/giphy/giphy.py'))

    @patch('sys.argv', ['zulip-run-bot', 'giphy', '--config-file', '/foo/bar/baz.conf'])
    @patch('zulip_bots.run.run_message_handler_for_bot')
    def test_argument_parsing_with_bot_name(__tmp1, __tmp5) -> None:
        with patch('zulip_bots.run.exit_gracefully_if_zulip_config_is_missing'):
            zulip_bots.run.main()

        __tmp5.assert_called_with(bot_name='giphy',
                                                            config_file='/foo/bar/baz.conf',
                                                            bot_config_file=None,
                                                            lib_module=mock.ANY,
                                                            quiet=False)

    @patch('sys.argv', ['zulip-run-bot', path_to_bot, '--config-file', '/foo/bar/baz.conf'])
    @patch('zulip_bots.run.run_message_handler_for_bot')
    def test_argument_parsing_with_bot_path(__tmp1, __tmp5: mock.Mock) -> None:
        with patch('zulip_bots.run.exit_gracefully_if_zulip_config_is_missing'):
            zulip_bots.run.main()

        __tmp5.assert_called_with(
            bot_name='giphy',
            config_file='/foo/bar/baz.conf',
            bot_config_file=None,
            lib_module=mock.ANY,
            quiet=False)

    def test_adding_bot_parent_dir_to_sys_path_when_bot_name_specified(__tmp1) -> None:
        bot_name = 'helloworld'  # existing bot's name
        expected_bot_dir_path = os.path.join(
            os.path.dirname(zulip_bots.run.__file__),
            'bots',
            bot_name
        )
        __tmp1._test_adding_bot_parent_dir_to_sys_path(bot_qualifier=bot_name, __tmp4=expected_bot_dir_path)

    @patch('os.path.isfile', return_value=True)
    def __tmp2(__tmp1, mock_os_path_isfile: mock.Mock) :
        bot_path = '/path/to/bot'
        expected_bot_dir_path = '/path/to'
        __tmp1._test_adding_bot_parent_dir_to_sys_path(bot_qualifier=bot_path, __tmp4=expected_bot_dir_path)

    def _test_adding_bot_parent_dir_to_sys_path(__tmp1, bot_qualifier, __tmp4):
        # type: (str, str) -> None
        with patch('sys.argv', ['zulip-run-bot', bot_qualifier, '--config-file', '/path/to/config']):
            with patch('zulip_bots.finder.import_module_from_source', return_value=mock.Mock()):
                with patch('zulip_bots.run.run_message_handler_for_bot'):
                    with patch('zulip_bots.run.exit_gracefully_if_zulip_config_is_missing'):
                        zulip_bots.run.main()

        __tmp1.assertIn(__tmp4, sys.path)

    @patch('os.path.isfile', return_value=False)
    def test_run_bot_by_module_name(__tmp1, mock_os_path_isfile: mock.Mock) :
        bot_module_name = 'bot.module.name'
        mock_bot_module = mock.Mock()
        mock_bot_module.__name__ = bot_module_name
        with patch('sys.argv', ['zulip-run-bot', 'bot.module.name', '--config-file', '/path/to/config']):
            with patch('importlib.import_module', return_value=mock_bot_module) as mock_import_module:
                with patch('zulip_bots.run.run_message_handler_for_bot'):
                        with patch('zulip_bots.run.exit_gracefully_if_zulip_config_is_missing'):
                            zulip_bots.run.main()
                            mock_import_module.assert_called_once_with(bot_module_name)


class __typ1(TestCase):
    def __tmp3(__tmp1) :

        def test_message(name: str, __tmp0: <FILL>, expected_return) -> None:
            mock_client = mock.MagicMock()
            mock_client.full_name = name
            mock_message = {'content': __tmp0}
            __tmp1.assertEqual(expected_return, extract_query_without_mention(mock_message, mock_client))
        test_message("xkcd", "@**xkcd**foo", "foo")
        test_message("xkcd", "@**xkcd** foo", "foo")
        test_message("xkcd", "@**xkcd** foo bar baz", "foo bar baz")
        test_message("xkcd", "@**xkcd**         foo bar baz", "foo bar baz")
        test_message("xkcd", "@**xkcd** 123_) (/&%) +}}}l", "123_) (/&%) +}}}l")
        test_message("brokenmention", "@**brokenmention* foo", None)
        test_message("nomention", "foo", None)
        test_message("Max Mustermann", "@**Max Mustermann** foo", "foo")
        test_message("Max (Mustermann)#(*$&12]\]", "@**Max (Mustermann)#(*$&12]\]** foo", "foo")

if __name__ == '__main__':
    unittest.main()
