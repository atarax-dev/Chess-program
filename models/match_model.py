class Match:
    def __init__(self, player1, player2, result1=0, result2=0):
        self.player1 = player1
        self.player2 = player2
        self.result1 = result1
        self.result2 = result2

    def __str__(self):
        if self.result1 == 0 and self.result2 == 0:
            return f"{self.player1.first_name} {self.player1.last_name} " \
                   f"vs. {self.player2.first_name} {self.player2.last_name}"
        else:
            return f"{self.player1.first_name} {self.player1.last_name}: {self.result1} " \
                   f"vs. {self.player2.first_name} {self.player2.last_name}: {self.result2} "

    def get_json(self):
        """
Permet d'obtenir les informations du match sous forme de dictionnaire
        :return: dict
        """
        return {
            "player1": self.player1.get_json(),
            "player2": self.player2.get_json(),
            "result1": self.result1,
            "result2": self.result2
        }
