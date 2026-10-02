from domain.player import Player
class DuelResult:
    def __init__(self, winner: Player,
                 loser: Player,
                 damage: int,
                 gained_xp: int,
                 lost_hp: int,
                 ko: bool):
        self.winner = winner
        self.loser = loser
        self.damage = damage
        self.gained_xp = gained_xp
        self.lost_hp = lost_hp
        self.ko = ko

