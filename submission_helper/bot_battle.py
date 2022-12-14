import json
from .enums import ChallengeAction, PrimaryAction, CounterAction, RequestedMove
from .state import GameInfo


class BotBattle:
    def __init__(self):
        self.from_engine = open(f'/io/from_engine.pipe', 'r', encoding='utf-8') 
        self.to_engine = open(f'/io/to_engine.pipe', 'w', encoding='utf-8') 

    def get_game_info(self) -> GameInfo:
        dict_game_info = self._read_from_pipe()
        return GameInfo(dict_game_info)

    def play_primary_action(self, primary_action: PrimaryAction, target_player_id: int = None):
        dict_move = {
            'type': RequestedMove.PrimaryAction.name,
            'action': int(primary_action),
            'target': target_player_id
        }
        self._write_to_pipe(dict_move)

    def play_challenge_action(self, challenge_action: ChallengeAction):
        dict_move = {
            'type': RequestedMove.ChallengeAction.name,
            'action': int(challenge_action)
        }
        self._write_to_pipe(dict_move)

    def play_challenge_response(self, card_index: int):
        dict_move = {
            'type': RequestedMove.ChallengeResponse.name,
            'card_index': card_index
        }
        self._write_to_pipe(dict_move)

    def play_counter_action(self, counter_action: CounterAction):
        dict_move = {
            'type': RequestedMove.CounterAction.name,
            'action': int(counter_action)
        }
        self._write_to_pipe(dict_move)

    def play_discard_choice(self, card_index: int):
        dict_move = {
            'type': RequestedMove.DiscardChoice.name,
            'card_index': card_index
        }
        self._write_to_pipe(dict_move)

    def _read_from_pipe(self):
        json_game_info = ''
        while not json_game_info or json_game_info[-1] != ';':
            json_game_info += self.from_engine.read(1)

        deserialized_game_info = json.loads(json_game_info[:-1])
        return deserialized_game_info

    def _write_to_pipe(self, dict_move):
        serialized_move = json.dumps(dict_move)
        serialized_move += ';'
        self.to_engine.write(serialized_move)
        self.to_engine.flush()