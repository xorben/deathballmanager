from random import choice
import engine.dice as dice
import engine.duel as duel
from domain.player import Player
import config.rules as rules
from engine.duel_result import DuelResult
from domain.team import Team
from engine.attack_result import AttackResult
from engine.midfield_result import MidfieldResult

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
        ko
    )
    return d_result


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


def process_zone_attack(attacker: Player, defending_team:Team, zone:str) -> DuelResult | None:
    defender = select_random_player_in_zone(defending_team, zone)
    if defender is not None:
        return process_duel(attacker, defender)
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
    stopped = False
    points_scored = 0
    gained_xp = 0
    last_field = ""
    goal = False

    if not stopped:
        # Attacker is in midfield and fights against midfield
        print("Attacking Midfield")
        d_result = process_zone_attack(attacker, defending_team, "midfield")
        last_field = "midfield"
        if d_result is not None and d_result.winner == attacker:
            gained_xp += d_result.gained_xp
        if d_result is not None and d_result.winner != attacker:
            print("Attack stopped in Midfield")
            stopped = True

    if not stopped:
        # Attacker is in attack zone and fights against enemy defense
        print("Attacking Attack")
        d_result = process_zone_attack(attacker, defending_team, "defense")
        last_field = "attack"
        if d_result is not None and d_result.winner == attacker:
            gained_xp += d_result.gained_xp
        if d_result is not None and d_result.winner != attacker:
            print("Attack stopped in Attack")
            stopped = True

    if not stopped:
        print("Goal attempt")
        last_field = "goal"
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
        last_field
    )
    return a_result


def select_midfield_player(team: Team) -> Player|None:
    player = select_random_player_in_zone(team, "midfield")
    if player is None:
        player = select_random_player_in_zone(team, "defense")
    if player is None:
        player = select_random_player_in_zone(team, "attack")
    return player


def process_midfield(team_a: Team, team_b: Team) -> MidfieldResult:
    active_player_a = select_midfield_player(team_a)
    active_player_b = select_midfield_player(team_b)
    d_result = None
    ball_carrier = None
    winning_team = None
    if active_player_a is not None and active_player_b is not None:
        d_result = process_duel(active_player_a, active_player_b)
        if d_result.winner == active_player_a:
            winning_team = team_a
            ball_carrier = active_player_a
        else:
            winning_team = team_b
            ball_carrier = active_player_b
    elif active_player_a is not None and active_player_b is None:
        winning_team = team_a
        ball_carrier = active_player_a
    elif active_player_b is not None and active_player_a is None:
        winning_team = team_b
        ball_carrier = active_player_b
    mf_result = MidfieldResult(winning_team, ball_carrier, d_result)
    return mf_result