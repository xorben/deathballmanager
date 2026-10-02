import engine.duel as duel
from domain.player import Player
import config.rules as rules
from engine.duel_result import DuelResult
from domain.team import Team
def process_duel(attacker: Player, defender: Player) -> DuelResult:
    winner_gained_xp = 0
    ko = False
    winner, loser, damage = duel.duel(attacker, defender)
    loser_lost_hp = min(damage, loser.hp)
    loser.hp = max(loser.hp - damage, 0)

    winner_gained_xp += rules.xp["duel_win"]
    if loser.hp == 0:
        ko = True
        winner_gained_xp += rules.xp["ko"]
    winner.xp += winner_gained_xp
    dresult = DuelResult(
        winner,
        loser,
        damage,
        winner_gained_xp,
        loser_lost_hp,
        ko
    )
    return dresult


def decide_active_player(team: Team) -> list[Player]:
    active_players = [p for p in team.players if p.hp > 0]
    return active_players