from domain.zones import Zone
from domain.career_stats import CareerStats

class Player:
    def __init__(self,
                 hp: int,
                 xp: int,
                 name: str,
                 strength: int,
                 player_id: int,
                 max_hp: int,
                 level:int,
                 position: Zone,
                 age: int,
                 implants: list,
                 career_stats: CareerStats

    ):
        self.player_id = player_id
        self.hp = hp
        self.xp = xp
        self.name = name
        self.strength = strength
        self.max_hp = max_hp
        self.level = level
        self.position = position
        self.age = age
        self.implants = implants
        self.career_stats = career_stats


    @property
    def market_value(self) -> None:
        mv =    self.xp * 10 \
                + self.strength * 30 \
                + self.max_hp * 20 \
                - self.age * 10
        return mv


    def __str__(self):
        return self.name


    def __repr__(self):
        return self.name