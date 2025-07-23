from typing import TypeAlias
__typ1 : TypeAlias = "Any"
__typ0 : TypeAlias = "int"
from zulip_bots.test_lib import BotTestCase, DefaultTests
from zulip_bots.game_handler import GameInstance

from typing import List, Tuple, Any


class TestTicTacToeBot(BotTestCase, DefaultTests):
    bot_name = 'tictactoe'

    # FIXME: Add tests for computer moves
    # FIXME: Add test lib for game_handler

    # Tests for TicTacToeModel functions
    # Things that might need to be checked: how model is being used in these functions,
    # When running the tests, many of the failures involved current_board. This
    # may need to be initialized prior to the constructor initialization in order to
    # avoid these errors.

    def __tmp2(__tmp1) -> None:
        board = [[0, 1, 0],
                 [0, 0, 0],
                 [0, 0, 2]]
        position = (0, 1)
        response = 1
        __tmp1._test_get_value(board, position, response)

    def _test_get_value(__tmp1, board: List[List[__typ0]], position: Tuple[__typ0, __typ0], expected_response: __typ0) -> None:
        model, message_handler = __tmp1._get_game_handlers()
        tictactoeboard = model(board)
        response = tictactoeboard.get_value(board, position)
        __tmp1.assertEqual(response, expected_response)

    def test_determine_game_over_with_win(__tmp1) :
        board = [[1, 1, 1],
                 [0, 2, 0],
                 [2, 0, 2]]
        players = ['Human', 'Computer']
        response = 'current turn'
        __tmp1._test_determine_game_over_with_win(board, players, response)

    def _test_determine_game_over_with_win(__tmp1, board: List[List[__typ0]], players, expected_response: str) -> None:
        model, message_handler = __tmp1._get_game_handlers()
        tictactoegame = model(board)
        response = tictactoegame.determine_game_over(players)
        __tmp1.assertEqual(response, expected_response)

    def test_determine_game_over_with_draw(__tmp1) :
        board = [[1, 2, 1],
                 [1, 2, 1],
                 [2, 1, 2]]
        players = ['Human', 'Computer']
        response = 'draw'
        __tmp1._test_determine_game_over_with_draw(board, players, response)

    def _test_determine_game_over_with_draw(__tmp1, board, players: List[str], expected_response: str) -> None:
        model, message_handler = __tmp1._get_game_handlers()
        tictactoeboard = model(board)
        response = tictactoeboard.determine_game_over(players)
        __tmp1.assertEqual(response, expected_response)

    def __tmp0(__tmp1) :
        board = [[1, 0, 1],
                 [1, 2, 1],
                 [2, 1, 2]]
        response = False
        __tmp1._test_board_is_full(board, response)

    def _test_board_is_full(__tmp1, board: List[List[__typ0]], expected_response: bool) -> None:
        model, message_handler = __tmp1._get_game_handlers()
        tictactoeboard = model(board)
        response = tictactoeboard.board_is_full(board)
        __tmp1.assertEqual(response, expected_response)

    def test_contains_winning_move(__tmp1) -> None:
        board = [[1, 1, 1],
                 [0, 2, 0],
                 [2, 0, 2]]
        response = True
        __tmp1._test_contains_winning_move(board, response)

    def _test_contains_winning_move(__tmp1, board, expected_response: bool) :
        model, message_handler = __tmp1._get_game_handlers()
        tictactoeboard = model(board)
        response = tictactoeboard.contains_winning_move(board)
        __tmp1.assertEqual(response, expected_response)

    def test_player_color(__tmp1) -> None:
        turn = 0
        response = ':cross_mark_button:'
        __tmp1._test_player_color(turn, response)

    def _test_player_color(__tmp1, turn: __typ0, expected_response: str) -> None:
        model, message_handler = __tmp1._get_game_handlers()
        response = message_handler.get_player_color(0)

        __tmp1.assertEqual(response, expected_response)

    def test_static_responses(__tmp1) -> None:
        model, message_handler = __tmp1._get_game_handlers()
        __tmp1.assertNotEqual(message_handler.get_player_color(0), None)
        __tmp1.assertNotEqual(message_handler.game_start_message(), None)
        __tmp1.assertEqual(message_handler.alert_move_message(
            'foo', 'move 3'), 'foo put a token at 3')

    def test_has_attributes(__tmp1) -> None:
        model, message_handler = __tmp1._get_game_handlers()
        __tmp1.assertTrue(hasattr(message_handler, 'parse_board') is not None)
        __tmp1.assertTrue(
            hasattr(message_handler, 'alert_move_message') is not None)
        __tmp1.assertTrue(hasattr(model, 'current_board') is not None)
        __tmp1.assertTrue(hasattr(model, 'determine_game_over') is not None)

    def test_parse_board(__tmp1) -> None:
        board = [[0, 1, 0],
                 [0, 0, 0],
                 [0, 0, 2]]
        response = ':one: :cross_mark_button: :three:\n\n' +\
            ':four: :five: :six:\n\n' +\
            ':seven: :eight: :o_button:\n\n'
        __tmp1._test_parse_board(board, response)

    def _test_parse_board(__tmp1, board: List[List[__typ0]], expected_response: <FILL>) -> None:
        model, message_handler = __tmp1._get_game_handlers()
        response = message_handler.parse_board(board)
        __tmp1.assertEqual(response, expected_response)

    def add_user_to_cache(__tmp1, name, bot: __typ1=None) -> __typ1:
        if bot is None:
            bot, bot_handler = __tmp1._get_handlers()
        message = {
            'sender_email': '{}@example.com'.format(name),
            'sender_full_name': '{}'.format(name)
        }
        bot.add_user_to_cache(message)
        return bot

    def setup_game(__tmp1) -> None:
        bot = __tmp1.add_user_to_cache('foo')
        __tmp1.add_user_to_cache('baz', bot)
        instance = GameInstance(bot, False, 'test game', 'abc123', [
                                'foo@example.com', 'baz@example.com'], 'test')
        bot.instances.update({'abc123': instance})
        instance.start()
        return bot

    def _get_game_handlers(__tmp1) -> Tuple[__typ1, __typ1]:
        bot, bot_handler = __tmp1._get_handlers()
        return bot.model, bot.gameMessageHandler
