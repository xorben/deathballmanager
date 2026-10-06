from random import choice
from typing import Literal
from time import sleep
import engine.dice as dice
import engine.duel as duel
from domain.player import Player
import config.rules as rules
from engine.duel_result import DuelResult
from domain.team import Team
from engine.attack_result import AttackResult
from engine.midfield_result import MidfieldResult
from domain.zones import Zone
from domain.player_action import PlayerAction

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
    d_result = DuelResult(
        winner,
        loser,
        damage,
        winner_gained_xp,
        loser_lost_hp,
        ko,
        defender
    )
    return d_result


def get_all_active_player(team: Team) -> list[Player]:
    active_players = [p for p in team.players if p.hp > 0]
    return active_players


def get_active_player_in_zone(team: Team, zone: Zone) -> list[Player]:
    active_players = [p for p in team.formation[zone] if p.hp > 0]
    return active_players


def select_random_player_in_zone(team: Team, zone: Zone) -> Player|None:
    players_in_zone = get_active_player_in_zone(team, zone)
    selected_player = None
    if len(players_in_zone) > 0:
        selected_player = choice(players_in_zone)
    return selected_player


def process_zone_attack(attacker: Player, defending_team:Team, zone: Zone) -> DuelResult | None:
    """
    Determines the winner within a zone
    :param attacker:
    :param defending_team:
    :param zone:
    :return:
    """
    defender = select_random_player_in_zone(defending_team, zone)
    if defender is not None:
        d_result = process_duel(attacker, defender)
        return d_result
    else:
        # go to next zone
        return None


def goal_attempt(attacking_player: Player) -> bool:
    """
    Handels the goal attempt
    :param attacking_player:
    :return:
    """
    roll = dice.roll_1d10()
    if roll + attacking_player.strength >= 10:
        return True
    else:
        return False


def process_attack(attacker: Player, defending_team:Team, attacking_team: Team) -> AttackResult:
    """
    Handels the play through the field and switching through the zones.
    :param attacking_team:
    :param attacker:
    :param defending_team:
    :return:
    """
    defender = None
    stopped = False
    points_scored = 0
    gained_xp = 0
    last_field = Zone.ATTACK
    goal = False

    if not stopped:
        # Attacker is in attack zone and fights against enemy defense
        print(attacker.name, "attacking attack zone!")
        sleep(1)
        d_result = process_zone_attack(attacker, defending_team, Zone.DEFENSE)
        if d_result is not None:
            defender = d_result.defender
            print(attacker.name, "fights against", defender.name)
        else:
            print("Enemy defense is empty.", attacker.name, "is running towards the goal!")
        sleep(1)
        last_field = Zone.ATTACK
        if d_result is not None and d_result.winner == attacker:
            gained_xp += d_result.gained_xp
        if d_result is not None and d_result.winner != attacker:
            stopped = True

    if not stopped:
        print("Goal attempt")
        last_field = Zone.GOAL
        goal = goal_attempt(attacker)
        if goal:
            print("GOAL!!!")
            attacker.xp += rules.xp["goal"]
            attacking_team.score += 1
            points_scored = 1
            gained_xp += rules.xp["goal"]
            print("One point for", attacking_team.name)
        else:
            print("Missed goal...")

    a_result = AttackResult(
        attacker,
        stopped,
        goal,
        points_scored,
        gained_xp,
        last_field,
        defender
    )
    return a_result


def select_midfield_player(team: Team) -> Player|None:
    player = select_random_player_in_zone(team, Zone.MIDFIELD)
    if player is None:
        player = select_random_player_in_zone(team, Zone.DEFENSE)
    if player is None:
        player = select_random_player_in_zone(team, Zone.ATTACK)
    return player


def process_midfield(team_a: Team, team_b: Team) -> MidfieldResult:
    active_player_a = select_midfield_player(team_a)
    active_player_b = select_midfield_player(team_b)
    d_result = None
    ball_carrier = None
    winning_team = None
    defeated_player = None
    if active_player_a is not None and active_player_b is not None:
        d_result = process_duel(active_player_a, active_player_b)
        if d_result.winner == active_player_a:
            winning_team = team_a
            ball_carrier = active_player_a
            defeated_player = active_player_b
        else:
            winning_team = team_b
            ball_carrier = active_player_b
            defeated_player = active_player_a
    elif active_player_a is not None and active_player_b is None:
        winning_team = team_a
        ball_carrier = active_player_a
        defeated_player = active_player_b
    elif active_player_b is not None and active_player_a is None:
        winning_team = team_b
        ball_carrier = active_player_b
        defeated_player = active_player_a
    mf_result = MidfieldResult(winning_team, ball_carrier, d_result, defeated_player)
    return mf_result


def player_decide_action(player: Player) -> Literal[PlayerAction.CHARGE, PlayerAction.PASS] | None:
    """
    Decide whether to pass or to charge
    :param player:
    :return:
    """
    roll = dice.roll_1d10()
    print(roll)
    player_action = None
    if 0 < player.hp < 30:
        # Player is to weak. Check if he has enough vitality
        if player.strength + roll >= 10:
            player_action = PlayerAction.CHARGE
        else:
            player_action = PlayerAction.PASS
    elif 30 <= player.hp < 80:
        # Player seems to be ok.
        if player.strength + roll + 2 >= 10:
            player_action = PlayerAction.CHARGE
        else:
            player_action = PlayerAction.PASS
    elif 80 <= player.hp <= 100:
        # Player is fine, should be less cautious
        if player.strength + roll + 4 >= 10:
            player_action = PlayerAction.CHARGE
        else:
            player_action = PlayerAction.PASS
    return player_action