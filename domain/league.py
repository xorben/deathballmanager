from domain.season import Season
from domain.team import Team
class League:
    def __init__(self):
        self.season_year = 2149
        self.season_dict = {}
        self.team_list = []


    def add_new_season(self, season: Season) -> None:
        self.season_year += 1
        self.season_dict[self.season_year] = season


    def add_new_team(self, team: Team) -> None:
        if team not in self.team_list:
            self.team_list.append(team)