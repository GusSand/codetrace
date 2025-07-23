from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
from zulip_bots.test_lib import BotTestCase, DefaultTests
from zulip_bots.game_handler import GameInstance

from typing import List, Tuple, Any


class __typ2(BotTestCase, DefaultTests):
    bot_name = 'tictactoe'

    # FIXME: Add tests for computer moves
    # FIXME: Add test lib for game_handler

    # Tests for TicTacToeModel functions
    # Things that might need to be checked: how model is being used in these functions,
    # When running the tests, many of the failures involved current_board. This
    # may need to be initialized prior to the constructor initialization in order to
    # avoid these errors.

    def __tmp11(__tmp0) :
        __tmp1 = [[0, 1, 0],
                 [0, 0, 0],
                 [0, 0, 2]]
        __tmp13 = (0, 1)
        response = 1
        __tmp0._test_get_value(__tmp1, __tmp13, response)

    def _test_get_value(__tmp0, __tmp1, __tmp13, __tmp15) :
        model, message_handler = __tmp0._get_game_handlers()
        tictactoeboard = model(__tmp1)
        response = tictactoeboard.get_value(__tmp1, __tmp13)
        __tmp0.assertEqual(response, __tmp15)

    def __tmp4(__tmp0) -> None:
        __tmp1 = [[1, 1, 1],
                 [0, 2, 0],
                 [2, 0, 2]]
        __tmp9 = ['Human', 'Computer']
        response = 'current turn'
        __tmp0._test_determine_game_over_with_win(__tmp1, __tmp9, response)

    def _test_determine_game_over_with_win(__tmp0, __tmp1, __tmp9: List[__typ0], __tmp15) :
        model, message_handler = __tmp0._get_game_handlers()
        tictactoegame = model(__tmp1)
        response = tictactoegame.determine_game_over(__tmp9)
        __tmp0.assertEqual(response, __tmp15)

    def __tmp6(__tmp0) :
        __tmp1 = [[1, 2, 1],
                 [1, 2, 1],
                 [2, 1, 2]]
        __tmp9 = ['Human', 'Computer']
        response = 'draw'
        __tmp0._test_determine_game_over_with_draw(__tmp1, __tmp9, response)

    def _test_determine_game_over_with_draw(__tmp0, __tmp1, __tmp9, __tmp15) :
        model, message_handler = __tmp0._get_game_handlers()
        tictactoeboard = model(__tmp1)
        response = tictactoeboard.determine_game_over(__tmp9)
        __tmp0.assertEqual(response, __tmp15)

    def __tmp8(__tmp0) :
        __tmp1 = [[1, 0, 1],
                 [1, 2, 1],
                 [2, 1, 2]]
        response = False
        __tmp0._test_board_is_full(__tmp1, response)

    def _test_board_is_full(__tmp0, __tmp1, __tmp15) :
        model, message_handler = __tmp0._get_game_handlers()
        tictactoeboard = model(__tmp1)
        response = tictactoeboard.board_is_full(__tmp1)
        __tmp0.assertEqual(response, __tmp15)

    def test_contains_winning_move(__tmp0) :
        __tmp1 = [[1, 1, 1],
                 [0, 2, 0],
                 [2, 0, 2]]
        response = True
        __tmp0._test_contains_winning_move(__tmp1, response)

    def _test_contains_winning_move(__tmp0, __tmp1: List[List[__typ1]], __tmp15: <FILL>) :
        model, message_handler = __tmp0._get_game_handlers()
        tictactoeboard = model(__tmp1)
        response = tictactoeboard.contains_winning_move(__tmp1)
        __tmp0.assertEqual(response, __tmp15)

    def __tmp10(__tmp0) :
        __tmp3 = 0
        response = ':cross_mark_button:'
        __tmp0._test_player_color(__tmp3, response)

    def _test_player_color(__tmp0, __tmp3, __tmp15) :
        model, message_handler = __tmp0._get_game_handlers()
        response = message_handler.get_player_color(0)

        __tmp0.assertEqual(response, __tmp15)

    def __tmp12(__tmp0) :
        model, message_handler = __tmp0._get_game_handlers()
        __tmp0.assertNotEqual(message_handler.get_player_color(0), None)
        __tmp0.assertNotEqual(message_handler.game_start_message(), None)
        __tmp0.assertEqual(message_handler.alert_move_message(
            'foo', 'move 3'), 'foo put a token at 3')

    def __tmp14(__tmp0) -> None:
        model, message_handler = __tmp0._get_game_handlers()
        __tmp0.assertTrue(hasattr(message_handler, 'parse_board') is not None)
        __tmp0.assertTrue(
            hasattr(message_handler, 'alert_move_message') is not None)
        __tmp0.assertTrue(hasattr(model, 'current_board') is not None)
        __tmp0.assertTrue(hasattr(model, 'determine_game_over') is not None)

    def __tmp5(__tmp0) :
        __tmp1 = [[0, 1, 0],
                 [0, 0, 0],
                 [0, 0, 2]]
        response = ':one: :cross_mark_button: :three:\n\n' +\
            ':four: :five: :six:\n\n' +\
            ':seven: :eight: :o_button:\n\n'
        __tmp0._test_parse_board(__tmp1, response)

    def _test_parse_board(__tmp0, __tmp1, __tmp15: __typ0) :
        model, message_handler = __tmp0._get_game_handlers()
        response = message_handler.parse_board(__tmp1)
        __tmp0.assertEqual(response, __tmp15)

    def add_user_to_cache(__tmp0, __tmp2: __typ0, bot: Any=None) :
        if bot is None:
            bot, bot_handler = __tmp0._get_handlers()
        message = {
            'sender_email': '{}@example.com'.format(__tmp2),
            'sender_full_name': '{}'.format(__tmp2)
        }
        bot.add_user_to_cache(message)
        return bot

    def __tmp7(__tmp0) :
        bot = __tmp0.add_user_to_cache('foo')
        __tmp0.add_user_to_cache('baz', bot)
        instance = GameInstance(bot, False, 'test game', 'abc123', [
                                'foo@example.com', 'baz@example.com'], 'test')
        bot.instances.update({'abc123': instance})
        instance.start()
        return bot

    def _get_game_handlers(__tmp0) :
        bot, bot_handler = __tmp0._get_handlers()
        return bot.model, bot.gameMessageHandler
