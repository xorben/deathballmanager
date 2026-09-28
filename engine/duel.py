import engine.dice as dice
from domain.player import Player
def duel(attacker: Player, defender: Player) -> tuple[Player, Player, int]:
    attacker_value = dice.roll_1d10() + attacker.strength
    defender_value = dice.roll_1d10() + defender.strength
    if attacker_value > defender_value:
        winner = attacker
        loser = defender
    else:
        winner = defender
        loser = attacker
    damage = abs(attacker_value-defender_value)
    return winner, loser, damage
