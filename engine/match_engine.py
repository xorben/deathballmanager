import engine.duel as duel
from domain.player import Player
import config.rules as rules
def process_duel(attacker: Player, defender: Player) -> tuple[Player, Player, int, int]:
    winner_gained_xp = 0
    winner, loser, damage = duel.duel(attacker, defender)
    loser.hp = max(loser.hp - damage, 0)
    winner_gained_xp += rules.xp["duel_win"]
    if loser.hp == 0:
        winner_gained_xp += rules.xp["ko"]
    winner.xp += winner_gained_xp
    return winner, loser, damage, winner_gained_xp