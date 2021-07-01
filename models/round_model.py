from datetime import datetime


class Round:
    def __init__(self, match_list, results=None, name=None, begin_date=datetime.now(), end_date=None):

        self.end_date = end_date
        self.begin_date = begin_date
        self.name = name
        self.match_list = match_list
        self.results = results

    def __repr__(self):
        return f"{self.results}"
