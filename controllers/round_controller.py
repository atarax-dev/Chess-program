from datetime import datetime


def enter_scores(tournament):
    i = tournament.current_round - 1
    for versus in tournament.rounds_list[i].match_list:
        result = input(f"Veuillez entrez le résultat du match {versus} (1/2/N) ")
        if result == "1":
            versus.player1.score += 1
            versus.result1 = 1
            versus.result2 = 0
        elif result == "2":
            versus.player2.score += 1
            versus.result1 = 0
            versus.result2 = 1
        elif result == "N":
            versus.player1.score += 0.5
            versus.result1 = 0.5
            versus.player2.score += 0.5
            versus.result2 = 0.5
    tournament.rounds_list[i].end_date = datetime.now()
    tournament.current_round += 1
