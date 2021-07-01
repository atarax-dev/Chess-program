from datetime import datetime

from controllers.match_controller import create_swiss_pairs, remove_already_paired
from controllers.tournament_controller import sort_players_rank, sort_players_score
from models.match_model import Match
from models.round_model import Round


def enter_scores(round_instance):
    match_results = []
    result1 = 0
    result2 = 0
    for versus in round_instance.match_list:
        result = input(f"Veuillez entrez le résultat du match {versus} (1/2/N) ")
        if result == "1":
            versus.player1.score += 1
            result1 = 1
            result2 = 0
        elif result == "2":
            versus.player2.score += 1
            result1 = 0
            result2 = 1
        elif result == "N":
            versus.player1.score += 0.5
            result1 = 0.5
            versus.player2.score += 0.5
            result2 = 0.5
        match_result = Match(versus.player1, versus.player2, result1, result2)
        match_results.append(match_result)
    round_instance.results = match_results
    round_instance.end_date = datetime.now()


def gen_pairs(tournament, round_number):
    if round_number == 1:
        players_list = sort_players_rank(tournament)
        sup_list = players_list[0:4]
        inf_list = players_list[4:8]
        first_pair = Match(sup_list[0], inf_list[0])
        second_pair = Match(sup_list[1], inf_list[1])
        third_pair = Match(sup_list[2], inf_list[2])
        fourth_pair = Match(sup_list[3], inf_list[3])
        match_list = [first_pair, second_pair, third_pair, fourth_pair]
        current_round = Round(match_list, name=f"Round{round_number}")
        tournament.rounds_list.append(current_round)
        return current_round

    else:
        tmp_list = sort_players_score(tournament)
        first_pair = create_swiss_pairs(tmp_list)
        remove_already_paired(tmp_list, first_pair)
        second_pair = create_swiss_pairs(tmp_list)
        remove_already_paired(tmp_list, second_pair)
        third_pair = create_swiss_pairs(tmp_list)
        remove_already_paired(tmp_list, third_pair)
        fourth_pair = create_swiss_pairs(tmp_list)
        match_list = [first_pair, second_pair, third_pair, fourth_pair]
        current_round = Round(match_list, name=f"Round{round_number}")
        tournament.rounds_list.append(current_round)
        return current_round
