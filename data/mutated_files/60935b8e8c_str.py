from zulip_bots.test_lib import BotTestCase, DefaultTests
from zulip_bots.game_handler import GameInstance
from libraries.constants import EMPTY_BOARD

from typing import List, Tuple, Any

class __typ0(BotTestCase, DefaultTests):
    bot_name = 'merels'

    def test_no_command(__tmp1):
        message = dict(content='magic', type='stream', sender_email="boo@email.com", sender_full_name="boo")
        res = __tmp1.get_response(message)
        __tmp1.assertEqual(res['content'], 'You are not in a game at the moment.'' Type `help` for help.')

    # FIXME: Add tests for computer moves
    # FIXME: Add test lib for game_handler

    # Test for unchanging aspects within the game
    # Player Color, Start Message, Moving Message
    def test_static_responses(__tmp1) -> None:
        model, message_handler = __tmp1._get_game_handlers()
        __tmp1.assertNotEqual(message_handler.get_player_color(0), None)
        __tmp1.assertNotEqual(message_handler.game_start_message(), None)
        __tmp1.assertEqual(message_handler.alert_move_message('foo', 'moved right'), 'foo :moved right')

    # Test to see if the attributes exist
    def __tmp6(__tmp1) :
        model, message_handler = __tmp1._get_game_handlers()
        # Attributes from the Merels Handler
        __tmp1.assertTrue(hasattr(message_handler, 'parse_board') is not None)
        __tmp1.assertTrue(hasattr(message_handler, 'get_player_color') is not None)
        __tmp1.assertTrue(hasattr(message_handler, 'alert_move_message') is not None)
        __tmp1.assertTrue(hasattr(message_handler, 'game_start_message') is not None)
        __tmp1.assertTrue(hasattr(message_handler, 'alert_move_message') is not None)
        # Attributes from the Merels Model
        __tmp1.assertTrue(hasattr(model, 'determine_game_over') is not None)
        __tmp1.assertTrue(hasattr(model, 'contains_winning_move') is not None)
        __tmp1.assertTrue(hasattr(model, 'make_move') is not None)

    def __tmp4(__tmp1) :
        __tmp2 = EMPTY_BOARD
        expectResponse = EMPTY_BOARD
        __tmp1._test_parse_board(__tmp2, expectResponse)

    def test_add_user_to_cache(__tmp1):
        __tmp1.add_user_to_cache("Name")

    def test_setup_game(__tmp1):
        __tmp1.setup_game()

    def add_user_to_cache(__tmp1, __tmp3: str, bot: Any=None) -> Any:
        if bot is None:
            bot, bot_handler = __tmp1._get_handlers()
        message = {
            'sender_email': '{}@example.com'.format(__tmp3),
            'sender_full_name': '{}'.format(__tmp3)}
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

    def _get_game_handlers(__tmp1) -> Tuple[Any, Any]:
        bot, bot_handler = __tmp1._get_handlers()
        return bot.model, bot.gameMessageHandler

    def _test_parse_board(__tmp1, __tmp2, __tmp7) -> None:
        model, message_handler = __tmp1._get_game_handlers()
        response = message_handler.parse_board(__tmp2)
        __tmp1.assertEqual(response, __tmp7)

    def __tmp0(__tmp1, __tmp2, __tmp5, __tmp7: <FILL>) -> None:
        model, message_handler = __tmp1._get_game_handlers()
        response = model.determine_game_over(__tmp5)
        __tmp1.assertEqual(response, __tmp7)
