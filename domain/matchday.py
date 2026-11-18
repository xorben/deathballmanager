from domain.fixture import Fixture
class MatchDay:
    def __init__(self, match_day_date: str) -> None:
        self.fixture_list: list[Fixture] = []
        self.match_day_date = match_day_date
        self.match_day_number = int


    def add_new_fixture(self, fixture: Fixture) -> None:
        if fixture not in self.fixture_list:
            self.fixture_list.append(fixture)