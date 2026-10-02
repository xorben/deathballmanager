class Player:
    def __init__(self, hp: int, xp: int, name: str,  strength: int):
        self.hp = hp
        self.xp = xp
        self.name = name
        self.strength = strength


    def __str__(self):
        return self.name


    def __repr__(self):
        return self.name