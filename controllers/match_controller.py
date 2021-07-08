from controllers.player_controller import create_player_from_json
from models.match_model import Match


def create_match_from_json(json_match):
    player1 = create_player_from_json(json_match["player1"])
    player2 = create_player_from_json(json_match["player2"])
    result1 = json_match["result1"]
    result2 = json_match["result2"]
    return Match(player1, player2, result1, result2)
