class Match:
    def __init__(self, player1, player2, result1=0, result2=0):
        self.player1 = player1
        self.player2 = player2
        self.result1 = result1
        self.result2 = result2

    def add_match_to_tournament(self, tournament):
        tournament.matchs_registry.append(self)

    def versus(self):
        return self.player1, self.player2

    def __repr__(self):
        if self.result1 == 0 and self.result2 == 0:
            return f"{self.player1} vs. {self.player2}"
        else:
            return f"{self.player1} {self.result1} vs. {self.player2} {self.result2} "
