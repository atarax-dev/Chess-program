from models.player_model import Player


def create_player():
    last_name = input("Veuillez entrez le nom de famille du joueur ")
    first_name = input("Veuillez entrez le prénom du joueur ")
    birth_date = input("Veuillez entrez la date de naissance du joueur au format jjmmaa ")
    gender = input("Veuillez entrez le genre du joueur M(ale)/F(emale)/O(thers) ")
    rank = input("Veuillez entrez le classement du joueur ")
    return Player(last_name, first_name, birth_date, gender, rank)


def update_rank_manually(player):
    updated_rank = int(input(f"Quel est le nouveau classement du joueur {player}? "))
    player.rank = updated_rank


def get_player_score(player):
    return player.score


def get_player_rank(player):
    return player.rank
