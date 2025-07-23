from typing import TypeAlias
__typ2 : TypeAlias = "Any"
from zulip_bots.game_handler import GameAdapter, BadMoveException
from typing import List, Any


class __typ0(object):
    tokens = [':blue_circle:', ':red_circle:']

    def parse_board(__tmp1, board: __typ2) -> str:
        return 'foo'

    def __tmp0(__tmp1, turn: int) -> str:
        return __tmp1.tokens[turn]

    def alert_move_message(__tmp1, original_player, move_info: <FILL>) -> str:
        column_number = move_info.replace('move ', '')
        return original_player + ' moved in column ' + column_number

    def game_start_message(__tmp1) -> str:
        return 'Type `move <column>` to place a token.\n \
The first player to get 4 in a row wins!\n \
Good Luck!'


class MockModel(object):
    def __init__(__tmp1) -> None:
        __tmp1.current_board = 'mock board'

    def make_move(
        __tmp1,
        move: str,
        player: int,
        is_computer: bool=False
    ) -> __typ2:
        if not is_computer:
            if int(move.replace('move ', '')) < 9:
                return 'mock board'
            else:
                raise BadMoveException('Invalid Move.')
        return 'mock board'

    def determine_game_over(__tmp1, players: List[str]) -> None:
        return None


class __typ1(GameAdapter):
    '''
    DO NOT USE THIS BOT
    This bot is used to test game_handler.py
    '''

    def __init__(__tmp1) -> None:
        game_name = 'foo test game'
        bot_name = 'game_handler_bot'
        move_help_message = '* To make your move during a game, type\n' \
                            '```move <column-number>```'
        move_regex = 'move (\d)$'
        model = MockModel
        gameMessageHandler = __typ0
        rules = ''

        super(__typ1, __tmp1).__init__(
            game_name,
            bot_name,
            move_help_message,
            move_regex,
            model,
            gameMessageHandler,
            rules,
            max_players=2,
            supports_computer=True
        )


handler_class = __typ1
