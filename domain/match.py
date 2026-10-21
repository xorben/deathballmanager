from i18n.message_key import MessageKey
from domain.team import Team


class Match:
    def __init__(self, team_a: Team, team_b: Team) -> None:
        self.team_a = team_a
        self.team_b = team_b
        self.events = []

    def add_event(self, key: MessageKey, **data) -> None:
        self.events.append({
            "key": key,
            "data": data
        })