from itertools import count

from domain.player import Player
from domain.zones import Zone
from domain.career_stats import CareerStats


_player_ids = count(1)


def create_player(
    hp: int = 100,
    xp: int = 0,
    name: str = "Testplayer",
    strength: int = 5,
    position: Zone = Zone.MIDFIELD,
) -> Player:
    return Player(
        hp=hp,
        xp=xp,
        name=name,
        basic_strength=strength,
        player_id=next(_player_ids),
        basic_max_hp=max(100, hp),
        level=1,
        position=position,
        age=20,
        career_stats=CareerStats()
    )