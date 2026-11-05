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
                 market_value: int,
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
        self.market_value = market_value
        self.implants = implants
        self.career_stats = career_stats

    def __str__(self):
        return self.name


    def __repr__(self):
        return self.name