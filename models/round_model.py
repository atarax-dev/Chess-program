from datetime import datetime


class Round:
    def __init__(self, match_list, name, begin_date, end_date=None):
        self.end_date = end_date
        self.begin_date = begin_date
        self.name = name
        self.match_list = match_list

    def get_json(self):
        json_match_list = []
        for match in self.match_list:
            json_match = match.get_json()
            json_match_list.append(json_match)
        end_date = datetime.strftime(self.end_date, "%Y-%m-%d %H:%M") if self.end_date is not None else None
        return {
            "match_list": json_match_list,
            "name": self.name,
            "begin_date": datetime.strftime(self.begin_date, "%Y-%m-%d %H:%M"),
            "end_date": end_date
        }
