from random import choice

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


def get_all_active_player(team: Team) -> list[Player]:
    active_players = [p for p in team.players if p.hp > 0]
    return active_players


def get_active_player_in_zone(team: Team, zone: str) -> list[Player]:
    active_players = [p for p in team.formation[zone] if p.hp > 0]
    return active_players


def select_random_player_in_zone(team: Team, zone: str) -> Player|None:
    players_in_zone = get_active_player_in_zone(team, zone)
    selected_player = None
    if len(players_in_zone) > 0:
        selected_player = choice(players_in_zone)
    return selected_player