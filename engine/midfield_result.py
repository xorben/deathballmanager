from domain.team import Team
from domain.player import Player
from engine.duel_result import DuelResult
class MidfieldResult:
    def __init__(
        self,
        winning_team: Team | None,
        ball_carrier: Player | None,
        duel_result: DuelResult | None
    ):
        self.winning_team = winning_team
        self.ball_carrier = ball_carrier
        self.duel_result = duel_result