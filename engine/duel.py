import engine.dice as dice
from domain.player import Player
def duel(attacker: Player, defender: Player) -> Player:
    attacker_value = dice.roll_1d10() + attacker.strength
    defender_value = dice.roll_1d10() + defender.strength
    if attacker_value > defender_value:
        return attacker
    elif defender_value >= attacker_value:
        return defender
