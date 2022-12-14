from .enums import *
from typing import Dict, List, Optional


class Action:
    def __init__(self, dict):
        # The ActionType of the action.
        self.action_type: ActionType = ActionType(int(dict['action_type']))

        # The Action of the action.
        if self.action_type == ActionType.PrimaryAction:
            self.action = PrimaryAction(int(dict['action']))
        elif self.action_type == ActionType.CounterAction:
            self.action = CounterAction(int(dict['action']))
        else:
            self.action = ChallengeAction(int(dict['action']))

        # The player that made the action.
        self.player: int = int(dict['player'])

        # The targeted player of the action if it exists.
        self.target: Optional[int] = int(dict['target']) if dict['target'] != None else None

        # Says whether the move successfully happened or was challenged and failed.
        self.successful: bool = bool(dict['successful'])


class GameInfo:
    def __init__(self, dict):
        # The move currently requested from you.
        self.requested_move: RequestedMove = RequestedMove(int(dict['requested_move']))

        # Your player id
        self.player_id: int = int(dict['player_id'])

        # A list of integers where the integers refer to the current balance of
        # each player. For example, balance[1] refers to the number of coins that
        # player 1 has currently.
        self.balances: List[int] = [int(x) for x in dict['balances']]

        # A list of Characters representing your current cards. See Character enum for details.
        self.own_cards: List[Character] = [Character(int(x)) for x in dict['own_cards']]

        # A list of integers where the integers refer to the current number of
        # cards each player possesses. For example, other_players_cards_num[2] refers
        # to the number of cards player 2 has currently.
        self.players_cards_num: List[int] = [int(x) for x in dict['players_cards_num']]

        # A dictionary index by Character containing an integer. This integer
        # refers to the number of that Character card that has been revealed
        # thus far. Hint: you can figure out which player revealed each card
        # by parsing the history.
        self.revealed_cards: Dict[Character, int] = {Character(int(character)):int(num) for (character, num) in dict['revealed_cards'].items()}

        # A list of turns. Each turn is a dictionary keyed by the action type in that turn.
        # The value is an Action which contains the move made & all relevant information.
        self.history: List[Dict[ActionType, Action]] = [{ActionType(int(move['action_type'])):Action(move['action']) for move in turn['turn']} for turn in dict['history']]

        # An integer representing the player who played/is playing the current
        # primary action. Note: this can be you. 
        self.current_primary_player: int = int(dict['current_primary_player'])