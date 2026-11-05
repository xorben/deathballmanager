from domain.attributes import Attribute
from domain.zones import Zone
from domain.career_stats import CareerStats

class Player:
    def __init__(self,
                 hp: int,
                 xp: int,
                 name: str,
                 basic_strength: int,
                 player_id: int,
                 basic_max_hp: int,
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
        self.basic_strength = basic_strength
        self.basic_max_hp = basic_max_hp
        self.level = level
        self.position = position
        self.age = age
        self.implants = implants
        self.career_stats = career_stats


    @property
    def strength(self) -> int:
        effective_strength = self.basic_strength
        for implant in self.implants:
            if implant.modifiers.get(Attribute.STRENGTH):
                effective_strength += implant.modifiers.get(Attribute.STRENGTH)
        return effective_strength


    @property
    def max_hp(self) -> int:
        effective_max_hp = self.basic_max_hp
        for implant in self.implants:
            if implant.modifiers.get(Attribute.MAX_HP):
                effective_max_hp += implant.modifiers.get(Attribute.MAX_HP)
        return effective_max_hp



    @property
    def market_value(self) -> int:
        mv =    self.xp * 10 \
                + self.strength * 30 \
                + self.max_hp * 20 \
                - self.age * 10

        for implant in self.implants:
            mv += implant.tier * 20
        return mv


    def __str__(self):
        return self.name


    def __repr__(self):
        return self.name