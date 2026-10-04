from domain.player import Player
from domain.zones import Zone
class AttackResult:
    def __init__(self,
                 attacker: Player,
                 stopped: bool,
                 goal:bool,
                 points_scored: int,
                 gained_xp: int,
                 last_field: Zone
                 ) -> None:
        self.attacker = attacker
        self.stopped = stopped
        self.goal = goal
        self.points_scored = points_scored
        self.gained_xp = gained_xp
        self.last_field = last_field