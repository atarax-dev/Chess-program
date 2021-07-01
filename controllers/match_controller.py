from models.match_model import Match


def check_matches(player1, player2):
    for match in Match.registry:
        if match.versus() == (player1, player2) or match.versus() == (player2, player1):
            return True
    return False


def create_swiss_pairs(players_list):
    i = 0
    x = 1
    if not check_matches(players_list[i], players_list[x]):
        pair = Match(players_list[i], players_list[x])
        return pair
    else:
        try:
            while check_matches(players_list[i], players_list[x]):
                x += 1
        except IndexError:
            x = 1
    pair = Match(players_list[i], players_list[x])
    return pair


def remove_already_paired(players_list, pair):
    players_list.remove(pair.player1)
    players_list.remove(pair.player2)
