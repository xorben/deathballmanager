from domain.matchday import MatchDay

class Season:
    def __init__(self):
        self.match_day_list = []


    def add_new_match_day(self, match_day: MatchDay) -> None:
        if match_day not in self.match_day_list:
            self.match_day_list.append(match_day)