"""Consolidated Death Ball Manager V0.1 / V0.2 regression tests.

Run with: pytest test/test_all.py -v
Do not leave the original test_*.py files alongside this file if you want one
execution of each test (pytest will collect both otherwise).
"""

import itertools
import pytest

import engine.duel as duel_engine
import engine.match_engine as match_engine
import engine.match_processor as match_processor
from config import rules, implants
from domain.career_stats import CareerStats
from domain.match import Match
from domain.player import Player as RealPlayer
from domain.player_action import PlayerAction
from domain.team import Team
from domain.zones import Zone
from engine.duel import duel
from engine.duel_result import DuelResult
from engine.match_engine import (
    process_duel, process_midfield, goal_attempt,
    get_all_active_player, is_team_eliminated,
    select_random_player_in_zone, select_midfield_player,
)
from engine.midfield_result import MidfieldResult
from i18n.message_key import MessageKey

# Central test constructor: keeps the original V0.1 test arguments readable
# while always constructing the V0.2 production Player with all required fields.
_id_sequence = itertools.count(1)


def Player(hp, xp, name, basic_strength, player_id=None,
           basic_max_hp=None, level=1, position=Zone.MIDFIELD,
           age=20, career_stats=None):
    return RealPlayer(
        hp=hp,
        xp=xp,
        name=name,
        basic_strength=basic_strength,
        player_id=next(_id_sequence) if player_id is None else player_id,
        basic_max_hp=max(50, hp) if basic_max_hp is None else basic_max_hp,
        level=level,
        position=position,
        age=age,
        career_stats=CareerStats() if career_stats is None else career_stats,
    )


@pytest.fixture
def player():
    return Player(
        hp=100,
        xp=0,
        name="Crusher",
        basic_strength=5,
        player_id=1001,
        basic_max_hp=100,
        level=1,
        position=Zone.DEFENSE,
        age=20,
        career_stats=CareerStats()
    )



# ============================================================================
# PLAYER TESTS
# ============================================================================

def test_player_initialization(player):
    assert player.player_id == 1001
    assert player.name == "Crusher"
    assert player.hp == 100
    assert player.xp == 0
    assert player.level == 1
    assert player.position == Zone.DEFENSE
    assert player.age == 20

    assert player.basic_strength == 5
    assert player.basic_max_hp == 100

    assert player.strength == 5
    assert player.max_hp == 100
    assert player.implants == ()


def test_player_string_representation(player):
    assert str(player) == "Crusher"
    assert repr(player) == "Crusher"


def test_player_career_stats(player):
    assert isinstance(player.career_stats, CareerStats)
    assert player.career_stats.match_wins == 0
    assert player.career_stats.duels_won == 0


# --------------------------------------------------
# Implantate: Strength
# --------------------------------------------------


def test_install_strength_implant(player):
    player.install_implant(implants.POWER_ARM_1)

    assert player.strength == 6
    assert player.basic_strength == 5


def test_install_multiple_strength_implants(player):
    player.install_implant(implants.POWER_ARM_1)
    player.install_implant(implants.POWER_ARM_2)

    assert player.strength == 8


def test_remove_strength_implant(player):
    player.install_implant(implants.POWER_ARM_1)

    assert player.strength == 6

    player.remove_implant(implants.POWER_ARM_1)

    assert player.strength == 5


def test_prevent_duplicate_implants(player):
    player.install_implant(implants.POWER_ARM_1)
    player.install_implant(implants.POWER_ARM_1)

    assert len(player.implants) == 1
    assert player.strength == 6


# --------------------------------------------------
# Implantate: HP
# --------------------------------------------------


def test_install_hp_implant(player):
    player.install_implant(implants.HELMET_1)

    assert player.max_hp == 105
    assert player.basic_max_hp == 100
    assert player.hp == 100


def test_install_multiple_hp_implants(player):
    player.install_implant(implants.HELMET_1)
    player.install_implant(implants.TORSO_AMPLIFIER)

    assert player.max_hp == 115


def test_remove_hp_implant(player):
    player.install_implant(implants.HELMET_1)

    assert player.max_hp == 105

    player.remove_implant(implants.HELMET_1)

    assert player.max_hp == 100


def test_hp_limit_after_implant_removal(player):
    player.install_implant(implants.HELMET_2)

    player.hp = 108

    assert player.max_hp == 110

    player.remove_implant(implants.HELMET_2)

    assert player.max_hp == 100
    assert player.hp == 100


def test_hp_remains_unchanged_if_below_limit(player):
    player.install_implant(implants.HELMET_2)

    player.hp = 80

    player.remove_implant(implants.HELMET_2)

    assert player.hp == 80


def test_reinstall_does_not_restore_hp(player):
    player.install_implant(implants.HELMET_2)
    player.hp = 108

    player.remove_implant(implants.HELMET_2)

    assert player.hp == 100

    player.install_implant(implants.HELMET_2)

    assert player.max_hp == 110
    assert player.hp == 100


# --------------------------------------------------
# Implantatverwaltung
# --------------------------------------------------


def test_implants_property_is_read_only(player):
    player.install_implant(implants.POWER_ARM_1)

    assert isinstance(player.implants, tuple)

    with pytest.raises(AttributeError):
        player.implants.append(implants.POWER_ARM_2)


def test_remove_nonexistent_implant(player):
    with pytest.raises(ValueError):
        player.remove_implant(implants.POWER_ARM_1)


def test_implant_does_not_modify_unrelated_attribute(player):
    player.install_implant(implants.HELMET_1)

    assert player.strength == 5

    player.install_implant(implants.POWER_ARM_1)

    assert player.max_hp == 105


def test_implants_are_independent_between_players(player):
    other_player = Player(
        hp=100,
        xp=0,
        name="Slasher",
        basic_strength=4,
        player_id=1002,
        basic_max_hp=100,
        level=1,
        position=Zone.DEFENSE,
        age=21,
        career_stats=CareerStats()
    )

    player.install_implant(implants.POWER_ARM_1)

    assert len(player.implants) == 1
    assert len(other_player.implants) == 0

    assert player.strength == 6
    assert other_player.strength == 4


# --------------------------------------------------
# Marktwert
# --------------------------------------------------


def test_market_value_without_implants(player):
    expected = (
        player.xp * 10
        + player.strength * 30
        + player.max_hp * 20
        - player.age * 10
    )

    assert player.market_value == expected


def test_market_value_increases_with_implant(player):
    value_before = player.market_value

    player.install_implant(implants.POWER_ARM_1)

    assert player.market_value > value_before


def test_market_value_decreases_after_removal(player):
    value_before = player.market_value

    player.install_implant(implants.POWER_ARM_1)

    player.remove_implant(implants.POWER_ARM_1)

    assert player.market_value == value_before


def test_market_value_changes_with_xp(player):
    value_before = player.market_value

    player.xp += 10

    assert player.market_value > value_before


# --------------------------------------------------
# Kompatibilität zur Match Engine
# --------------------------------------------------


def test_hp_can_be_reduced(player):
    player.hp -= 20

    assert player.hp == 80


def test_strength_is_read_only(player):
    with pytest.raises(AttributeError):
        player.strength = 10


def test_max_hp_is_read_only(player):
    with pytest.raises(AttributeError):
        player.max_hp = 150


# --------------------------------------------------
# Karriere
# --------------------------------------------------


def test_career_stats_can_be_updated(player):
    player.career_stats.match_wins += 1
    player.career_stats.duels_won += 3
    player.career_stats.ko_inflicted += 1

    assert player.career_stats.match_wins == 1
    assert player.career_stats.duels_won == 3
    assert player.career_stats.ko_inflicted == 1



# ============================================================================
# TEAM TESTS
# ============================================================================

def test_get_all_active_player_all_alive():
    player_1 = Player(10, 0, "Player 1", 3)
    player_2 = Player(20, 0, "Player 2", 4)
    team = Team("Test Team", [player_1, player_2])
    result = get_all_active_player(team)
    assert result == [player_1, player_2]


def test_get_all_active_player_all_ko():
    player_1 = Player(0, 0, "Player 1", 3)
    player_2 = Player(0, 0 ,"Player 2", 4)
    team = Team("Test Team", [player_1, player_2])
    result = get_all_active_player(team)
    assert result == []


def test_get_all_active_player_partly_ko():
    player_1 = Player(3, 0, "Player 1", 3)
    player_2 = Player(0, 0 ,"Player 2", 4)
    team = Team("Test Team", [player_1, player_2])
    result = get_all_active_player(team)
    assert result == [player_1]


def test_is_team_eliminated_all_ko():
    player_1 = Player(0, 0, "Player 1", 3)
    player_2 = Player(0, 0 ,"Player 2", 4)
    team = Team("Test Team", [player_1, player_2])
    result = is_team_eliminated(team)
    assert result == True


def test_is_team_eliminated_all_alive():
    player_1 = Player(11, 0, "Player 1", 3)
    player_2 = Player(3, 0 ,"Player 2", 4)
    team = Team("Test Team", [player_1, player_2])
    result = is_team_eliminated(team)
    assert result == False


def test_is_team_eliminated_mixed():
    player_1 = Player(11, 0, "Player 1", 3)
    player_2 = Player(0, 0, "Player 2", 4)
    team = Team("Test Team", [player_1, player_2])
    result = is_team_eliminated(team)
    assert result == False


def test_select_random_player_in_zone_only_active():
    player_1 = Player(0, 0, "Test Player 1", 2)
    player_2 = Player(50, 0, "Test Player 2", 4)
    player_3 = Player(50, 0, "Test Player 3", 4)
    player_4 = Player(50, 0, "Test Player 4", 3)
    player_5 = Player(50, 0, "Test Player 5", 5)
    team = Team("Test Team",[player_1, player_2, player_3, player_4, player_5])
    team.formation[Zone.DEFENSE].append(player_1)
    team.formation[Zone.DEFENSE].append(player_2)
    team.formation[Zone.DEFENSE].append(player_3)
    result = select_random_player_in_zone(team, Zone.DEFENSE)
    assert result in [team.match_players[1], team.match_players[2]]
    assert result.hp > 0


def test_select_random_player_in_zone_empty():
    team = Team(
        "Test Team",
        [
            Player(0, 0, "Test Player 1", 2),
            Player(0, 0, "Test Player 2", 4),
            Player(0, 0, "Test Player 3", 4),
        ]
    )
    team.formation[Zone.ATTACK].append(team.match_players[1])
    team.formation[Zone.ATTACK].append(team.match_players[2])
    team.formation[Zone.MIDFIELD].append(team.match_players[0])
    result = select_random_player_in_zone(team, Zone.DEFENSE)
    assert result is None


def test_select_midfield_player_from_midfield():
    player_1 = Player(1, 0, "Test Player 1", 2)
    player_2 = Player(3, 0, "Test Player 2", 4)
    player_3 = Player(22, 0, "Test Player 3", 4)
    player_4 = Player(3, 0, "Test Player 4", 4)
    player_5 = Player(2, 0, "Test Player 5", 4)
    team = Team("Test Team", [player_1, player_2, player_3, player_4, player_5])
    team.formation[Zone.DEFENSE].append(player_1)
    team.formation[Zone.MIDFIELD].append(player_2)
    team.formation[Zone.ATTACK].append(player_3)
    team.formation[Zone.MIDFIELD].append(player_4)
    team.formation[Zone.ATTACK].append(player_5)
    result = select_midfield_player(team)
    assert result in (player_2, player_4)


def test_select_midfield_player_fallback_defense():
    """Checks that a DEFENSE player was chosen"""
    player_1 = Player(1, 0, "Test Player 1", 2)
    player_2 = Player(0, 0, "Test Player 2", 4)
    player_3 = Player(22, 0, "Test Player 3", 4)
    player_4 = Player(0, 0, "Test Player 4", 4)
    player_5 = Player(2, 0, "Test Player 5", 4)
    team = Team("Test Team", [player_1, player_2, player_3, player_4, player_5])
    team.formation[Zone.DEFENSE].append(player_1)
    team.formation[Zone.MIDFIELD].append(player_2)
    team.formation[Zone.ATTACK].append(player_3)
    team.formation[Zone.MIDFIELD].append(player_4)
    team.formation[Zone.DEFENSE].append(player_5)
    result = select_midfield_player(team)
    assert result in (player_1, player_5)


def test_select_midfield_player_fallback_attack():
    player_1 = Player(0, 0, "Test Player 1", 2)
    player_2 = Player(0, 0, "Test Player 2", 4)
    player_3 = Player(22, 0, "Test Player 3", 4)
    player_4 = Player(0, 0, "Test Player 4", 4)
    player_5 = Player(0, 0, "Test Player 5", 4)
    team = Team("Test Team", [player_1, player_2, player_3, player_4, player_5])
    team.formation[Zone.DEFENSE].append(player_1)
    team.formation[Zone.MIDFIELD].append(player_2)
    team.formation[Zone.ATTACK].append(player_3)
    team.formation[Zone.MIDFIELD].append(player_4)
    team.formation[Zone.DEFENSE].append(player_5)
    result = select_midfield_player(team)
    assert result is player_3



# ============================================================================
# DUEL TESTS
# ============================================================================

def test_attacker_wins_duel(monkeypatch):
    """Checks that the attacker wins with the higher total value."""
    attacker = Player(50, 0, "Attacker", 4)
    defender = Player(50, 0, "Defender", 2)

    rolls = iter([8, 2])
    monkeypatch.setattr(duel_engine.dice, "roll_1d10", lambda: next(rolls))

    winner, loser, damage = duel(attacker, defender)

    assert winner is attacker
    assert loser is defender


def test_defender_wins_duel(monkeypatch):
    """Checks that the defender wins with the higher total value."""
    attacker = Player(50, 0, "Attacker", 2)
    defender = Player(50, 0, "Defender", 4)

    rolls = iter([2, 8])
    monkeypatch.setattr(duel_engine.dice, "roll_1d10", lambda: next(rolls))

    winner, loser, damage = duel(attacker, defender)

    assert winner is defender
    assert loser is attacker


def test_defender_wins_on_draw(monkeypatch):
    """Checks that the defender wins when both total values are equal."""
    attacker = Player(50, 0, "Attacker", 4)
    defender = Player(50, 0, "Defender", 4)

    rolls = iter([5, 5])
    monkeypatch.setattr(duel_engine.dice, "roll_1d10", lambda: next(rolls))

    winner, loser, damage = duel(attacker, defender)

    assert winner is defender
    assert loser is attacker


def test_duel_damage_is_difference(monkeypatch):
    """Checks that damage equals the difference between both total values."""
    attacker = Player(50, 0, "Attacker", 4)
    defender = Player(50, 0, "Defender", 2)

    rolls = iter([8, 3])
    monkeypatch.setattr(duel_engine.dice, "roll_1d10", lambda: next(rolls))

    winner, loser, damage = duel(attacker, defender)

    assert damage == 7


def test_process_duel_hp_not_below_zero(monkeypatch):
    """Checks that player HP never drops below zero."""
    attacker = Player(50, 0, "Attacker", 5)
    defender = Player(3, 0, "Defender", 1)

    rolls = iter([10, 1])
    monkeypatch.setattr(duel_engine.dice, "roll_1d10", lambda: next(rolls))

    result = process_duel(attacker, defender)

    assert defender.hp == 0
    assert result.lost_hp == 3


def test_process_duel_awards_duel_win_xp(monkeypatch):
    """Checks that the duel winner receives DUEL_WIN XP."""
    attacker = Player(50, 0, "Attacker", 5)
    defender = Player(50, 0, "Defender", 1)

    rolls = iter([8, 2])
    monkeypatch.setattr(duel_engine.dice, "roll_1d10", lambda: next(rolls))

    process_duel(attacker, defender)

    assert attacker.xp == rules.Xp.DUEL_WIN


def test_process_duel_awards_ko_xp(monkeypatch):
    """Checks that the winner receives additional KO XP."""
    attacker = Player(50, 0, "Attacker", 5)
    defender = Player(3, 0, "Defender", 1)

    rolls = iter([10, 1])
    monkeypatch.setattr(duel_engine.dice, "roll_1d10", lambda: next(rolls))

    process_duel(attacker, defender)

    expected_xp = rules.Xp.DUEL_WIN + rules.Xp.KO

    assert attacker.xp == expected_xp


def test_duel_result_values(monkeypatch):
    """Checks that DuelResult contains the correct duel values."""
    attacker = Player(50, 0, "Attacker", 5)
    defender = Player(10, 0, "Defender", 1)

    rolls = iter([8, 2])
    monkeypatch.setattr(duel_engine.dice, "roll_1d10", lambda: next(rolls))

    result = process_duel(attacker, defender)
    print(result)
    assert result.attacker is attacker
    assert result.defender is defender
    assert result.winner is attacker
    assert result.loser is defender
    assert result.damage == 10
    assert result.lost_hp == 10
    assert result.ko is True



# ============================================================================
# MIDFIELD TESTS
# ============================================================================

def test_midfield_team_a_wins(monkeypatch):
    """Checks that Team A becomes the winning team when its player wins."""
    player_a = Player(50, 0, "Player A", 4)
    player_b = Player(50, 0, "Player B", 2)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    team_a.formation[Zone.MIDFIELD].append(player_a)
    team_b.formation[Zone.MIDFIELD].append(player_b)

    rolls = iter([8, 2])
    monkeypatch.setattr(
        duel_engine.dice,
        "roll_1d10",
        lambda: next(rolls)
    )

    result = process_midfield(team_a, team_b)

    assert result.winning_team is team_a


def test_midfield_team_b_wins(monkeypatch):
    """Checks that Team B becomes the winning team when its player wins."""
    player_a = Player(50, 0, "Player A", 2)
    player_b = Player(50, 0, "Player B", 4)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    team_a.formation[Zone.MIDFIELD].append(player_a)
    team_b.formation[Zone.MIDFIELD].append(player_b)

    rolls = iter([2, 8])
    monkeypatch.setattr(
        duel_engine.dice,
        "roll_1d10",
        lambda: next(rolls)
    )

    result = process_midfield(team_a, team_b)

    assert result.winning_team is team_b


def test_midfield_winner_becomes_ball_carrier(monkeypatch):
    """Checks that the midfield duel winner becomes the ball carrier."""
    player_a = Player(50, 0, "Player A", 4)
    player_b = Player(50, 0, "Player B", 2)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    team_a.formation[Zone.MIDFIELD].append(player_a)
    team_b.formation[Zone.MIDFIELD].append(player_b)

    rolls = iter([8, 2])
    monkeypatch.setattr(
        duel_engine.dice,
        "roll_1d10",
        lambda: next(rolls)
    )

    result = process_midfield(team_a, team_b)

    assert result.ball_carrier is player_a


def test_midfield_loser_becomes_defeated_player(monkeypatch):
    """Checks that the midfield duel loser becomes the defeated player."""
    player_a = Player(50, 0, "Player A", 4)
    player_b = Player(50, 0, "Player B", 2)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    team_a.formation[Zone.MIDFIELD].append(player_a)
    team_b.formation[Zone.MIDFIELD].append(player_b)

    rolls = iter([8, 2])
    monkeypatch.setattr(
        duel_engine.dice,
        "roll_1d10",
        lambda: next(rolls)
    )

    result = process_midfield(team_a, team_b)

    assert result.defeated_player is player_b


def test_midfield_only_team_a_has_player():
    """Checks that Team A gains possession when only Team A has an active player."""
    player_a = Player(50, 0, "Player A", 4)
    player_b = Player(0, 0, "Player B", 4)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    team_a.formation[Zone.MIDFIELD].append(player_a)
    team_b.formation[Zone.MIDFIELD].append(player_b)

    result = process_midfield(team_a, team_b)

    assert result.winning_team is team_a
    assert result.ball_carrier is player_a
    assert result.defeated_player is None
    assert result.duel_result is None


def test_midfield_only_team_b_has_player():
    """Checks that Team B gains possession when only Team B has an active player."""
    player_a = Player(0, 0, "Player A", 4)
    player_b = Player(50, 0, "Player B", 4)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    team_a.formation[Zone.MIDFIELD].append(player_a)
    team_b.formation[Zone.MIDFIELD].append(player_b)

    result = process_midfield(team_a, team_b)

    assert result.winning_team is team_b
    assert result.ball_carrier is player_b
    assert result.defeated_player is None
    assert result.duel_result is None


def test_midfield_no_active_players():
    """Checks that no team gains possession when no active player is available."""
    player_a = Player(0, 0, "Player A", 4)
    player_b = Player(0, 0, "Player B", 4)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    team_a.formation[Zone.MIDFIELD].append(player_a)
    team_b.formation[Zone.MIDFIELD].append(player_b)

    result = process_midfield(team_a, team_b)

    assert result.winning_team is None
    assert result.ball_carrier is None
    assert result.defeated_player is None
    assert result.duel_result is None



# ============================================================================
# PLAYER ACTION TESTS
# ============================================================================

def test_player_decides_pass(monkeypatch):
    """Checks that the player decides to pass with a low enough result."""
    player = Player(20, 0, "Player", 2)

    monkeypatch.setattr(
        match_engine.dice,
        "roll_1d10",
        lambda: 3
    )

    result = match_engine.player_decide_action(player)

    assert result is PlayerAction.PASS


def test_player_decides_charge(monkeypatch):
    """Checks that the player decides to charge with a high enough result."""
    player = Player(20, 0, "Player", 5)

    monkeypatch.setattr(
        match_engine.dice,
        "roll_1d10",
        lambda: 5
    )

    result = match_engine.player_decide_action(player)

    assert result is PlayerAction.CHARGE


def test_pass_selects_attack_player(monkeypatch):
    """Checks that a pass selects an active player from the attack zone."""
    ball_carrier = Player(50, 0, "Ball Carrier", 3)
    attack_player = Player(50, 0, "Attack Player", 4)
    defeated_player = Player(50, 0, "Defeated Player", 3)

    team_a = Team("Team A", [ball_carrier, attack_player])
    team_b = Team("Team B", [defeated_player])

    team_a.formation[Zone.MIDFIELD].append(ball_carrier)
    team_a.formation[Zone.ATTACK].append(attack_player)
    team_b.formation[Zone.MIDFIELD].append(defeated_player)

    match = Match(team_a, team_b)

    midfield_result = MidfieldResult(
        team_a,
        ball_carrier,
        None,
        defeated_player
    )

    monkeypatch.setattr(
        match_engine,
        "process_midfield",
        lambda team_a, team_b: midfield_result
    )

    monkeypatch.setattr(
        match_engine,
        "player_decide_action",
        lambda player: PlayerAction.PASS
    )

    monkeypatch.setattr(
        match_engine,
        "process_attack",
        lambda attacker, defending_team, attacking_team, match: None
    )

    result = match_engine.process_play(match)

    assert result[1] is PlayerAction.PASS


def test_pass_falls_back_to_charge(monkeypatch):
    """Checks that pass falls back to charge when no attack player is available."""
    ball_carrier = Player(50, 0, "Ball Carrier", 3)
    defeated_player = Player(50, 0, "Defeated Player", 3)

    team_a = Team("Team A", [ball_carrier])
    team_b = Team("Team B", [defeated_player])

    team_a.formation[Zone.MIDFIELD].append(ball_carrier)
    team_b.formation[Zone.MIDFIELD].append(defeated_player)

    match = Match(team_a, team_b)

    midfield_result = MidfieldResult(
        team_a,
        ball_carrier,
        None,
        defeated_player
    )

    monkeypatch.setattr(
        match_engine,
        "process_midfield",
        lambda team_a, team_b: midfield_result
    )

    monkeypatch.setattr(
        match_engine,
        "player_decide_action",
        lambda player: PlayerAction.PASS
    )

    monkeypatch.setattr(
        match_engine,
        "process_attack",
        lambda attacker, defending_team, attacking_team, match: None
    )

    result = match_engine.process_play(match)

    assert result[1] is PlayerAction.CHARGE



# ============================================================================
# ATTACK TESTS
# ============================================================================

def test_empty_defense_reaches_goal_attempt(monkeypatch):
    """Checks that an empty defense allows the attacker to reach the goal attempt."""
    attacker = Player(50, 0, "Attacker", 4)

    attacking_team = Team("Attacking Team", [attacker])
    defending_team = Team("Defending Team", [])
    match = Match(attacking_team, defending_team)

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: None
    )

    monkeypatch.setattr(
        match_engine,
        "goal_attempt",
        lambda attacker: False
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    result = match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert result.last_field is Zone.GOAL


def test_defender_win_stops_attack(monkeypatch):
    """Checks that the attack stops when the defender wins the duel."""
    attacker = Player(50, 0, "Attacker", 3)
    defender = Player(50, 0, "Defender", 4)

    attacking_team = Team("Attacking Team", [attacker])
    defending_team = Team("Defending Team", [defender])
    match = Match(attacking_team, defending_team)

    duel_result = DuelResult(
        defender,
        attacker,
        5,
        rules.Xp.DUEL_WIN,
        5,
        False,
        defender,
        attacker
    )

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: duel_result
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    result = match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert result.stopped is True


def test_attacker_win_reaches_goal_attempt(monkeypatch):
    """Checks that the attacker reaches the goal attempt after winning the duel."""
    attacker = Player(50, 0, "Attacker", 4)
    defender = Player(50, 0, "Defender", 3)

    attacking_team = Team("Attacking Team", [attacker])
    defending_team = Team("Defending Team", [defender])
    match = Match(attacking_team, defending_team)

    duel_result = DuelResult(
        attacker,
        defender,
        5,
        rules.Xp.DUEL_WIN,
        5,
        False,
        defender,
        attacker
    )

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: duel_result
    )

    monkeypatch.setattr(
        match_engine,
        "goal_attempt",
        lambda attacker: False
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    result = match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert result.last_field is Zone.GOAL


def test_attack_result_stopped(monkeypatch):
    """Checks that AttackResult stores the stopped state correctly."""
    attacker = Player(50, 0, "Attacker", 3)
    defender = Player(50, 0, "Defender", 4)

    attacking_team = Team("Attacking Team", [attacker])
    defending_team = Team("Defending Team", [defender])
    match = Match(attacking_team, defending_team)

    duel_result = DuelResult(
        defender,
        attacker,
        5,
        rules.Xp.DUEL_WIN,
        5,
        False,
        defender,
        attacker
    )

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: duel_result
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    result = match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert result.stopped is True


def test_attack_result_defender(monkeypatch):
    """Checks that AttackResult stores the correct defender."""
    attacker = Player(50, 0, "Attacker", 3)
    defender = Player(50, 0, "Defender", 4)

    attacking_team = Team("Attacking Team", [attacker])
    defending_team = Team("Defending Team", [defender])
    match = Match(attacking_team, defending_team)

    duel_result = DuelResult(
        defender,
        attacker,
        5,
        rules.Xp.DUEL_WIN,
        5,
        False,
        defender,
        attacker
    )

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: duel_result
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    result = match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert result.defender is defender


def test_attack_last_field_attack_when_stopped(monkeypatch):
    """Checks that the last field remains ATTACK when the attack is stopped."""
    attacker = Player(50, 0, "Attacker", 3)
    defender = Player(50, 0, "Defender", 4)

    attacking_team = Team("Attacking Team", [attacker])
    defending_team = Team("Defending Team", [defender])
    match = Match(attacking_team, defending_team)

    duel_result = DuelResult(
        defender,
        attacker,
        5,
        rules.Xp.DUEL_WIN,
        5,
        False,
        defender,
        attacker
    )

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: duel_result
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    result = match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert result.last_field is Zone.ATTACK


def test_attack_last_field_goal_on_attempt(monkeypatch):
    """Checks that the last field becomes GOAL when a goal attempt is reached."""
    attacker = Player(50, 0, "Attacker", 4)

    attacking_team = Team("Attacking Team", [attacker])
    defending_team = Team("Defending Team", [])
    match = Match(attacking_team, defending_team)

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: None
    )

    monkeypatch.setattr(
        match_engine,
        "goal_attempt",
        lambda attacker: False
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    result = match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert result.last_field is Zone.GOAL


def test_goal_increases_score(monkeypatch):
    """Checks that a successful goal increases the team score by one."""
    attacker = Player(50, 0, "Attacker", 4)

    attacking_team = Team("Attacking Team", [attacker])
    defending_team = Team("Defending Team", [])
    match = Match(attacking_team, defending_team)

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: None
    )

    monkeypatch.setattr(
        match_engine,
        "goal_attempt",
        lambda attacker: True
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert attacking_team.score == 1


def test_goal_awards_xp(monkeypatch):
    """Checks that the scoring player receives GOAL XP."""
    attacker = Player(50, 0, "Attacker", 4)

    attacking_team = Team("Attacking Team", [attacker])
    defending_team = Team("Defending Team", [])
    match = Match(attacking_team, defending_team)

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: None
    )

    monkeypatch.setattr(
        match_engine,
        "goal_attempt",
        lambda attacker: True
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert attacker.xp == rules.Xp.GOAL


def test_missed_goal_does_not_change_score(monkeypatch):
    """Checks that a missed goal does not change the team score."""
    attacker = Player(50, 0, "Attacker", 4)

    attacking_team = Team("Attacking Team", [attacker])
    defending_team = Team("Defending Team", [])
    match = Match(attacking_team, defending_team)

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: None
    )

    monkeypatch.setattr(
        match_engine,
        "goal_attempt",
        lambda attacker: False
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert attacking_team.score == 0


def test_attack_result_points_scored(monkeypatch):
    """Checks that AttackResult stores one point after a successful goal."""
    attacker = Player(50, 0, "Attacker", 4)

    attacking_team = Team("Attacking Team", [attacker])
    defending_team = Team("Defending Team", [])
    match = Match(attacking_team, defending_team)

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: None
    )

    monkeypatch.setattr(
        match_engine,
        "goal_attempt",
        lambda attacker: True
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    result = match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert result.points_scored == 1


def test_attack_stopped_event(monkeypatch):
    """Checks that a stopped attack creates an ATTACK_STOPPED event."""
    attacker = Player(50, 0, "Attacker", 3)
    defender = Player(50, 0, "Defender", 4)

    attacking_team = Team("Team A", [attacker])
    defending_team = Team("Team B", [defender])
    match = Match(attacking_team, defending_team)

    duel_result = DuelResult(
        defender,
        attacker,
        5,
        rules.Xp.DUEL_WIN,
        5,
        False,
        defender,
        attacker
    )

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: duel_result
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert any(
        event["key"] is MessageKey.ATTACK_STOPPED
        for event in match.events
    )



# ============================================================================
# GOAL TESTS
# ============================================================================

def test_goal_attempt_below_threshold(monkeypatch):
    """Checks that a total value below 10 results in a missed goal."""
    player = Player(50, 0, "Player", 4)

    monkeypatch.setattr(
        match_engine.dice,
        "roll_1d10",
        lambda: 5
    )

    result = goal_attempt(player)

    assert result is False


def test_goal_attempt_exact_threshold(monkeypatch):
    """Checks that a total value of exactly 10 results in a goal."""
    player = Player(50, 0, "Player", 4)

    monkeypatch.setattr(
        match_engine.dice,
        "roll_1d10",
        lambda: 6
    )

    result = goal_attempt(player)

    assert result is True


def test_goal_attempt_above_threshold(monkeypatch):
    """Checks that a total value above 10 results in a goal."""
    player = Player(50, 0, "Player", 4)

    monkeypatch.setattr(
        match_engine.dice,
        "roll_1d10",
        lambda: 8
    )

    result = goal_attempt(player)

    assert result is True



# ============================================================================
# EVENT TESTS
# ============================================================================

def test_add_event_adds_event():
    """Checks that add_event adds an event to the match."""
    team_a = Team("Team A", [])
    team_b = Team("Team B", [])
    match = Match(team_a, team_b)

    match.add_event(
        MessageKey.GOAL,
        team="Team A"
    )

    assert len(match.events) == 1


def test_add_event_stores_correct_key():
    """Checks that add_event stores the correct event key."""
    team_a = Team("Team A", [])
    team_b = Team("Team B", [])
    match = Match(team_a, team_b)

    match.add_event(
        MessageKey.GOAL,
        team="Team A"
    )

    assert match.events[0]["key"] is MessageKey.GOAL


def test_add_event_stores_correct_data():
    """Checks that add_event stores the supplied event data."""
    team_a = Team("Team A", [])
    team_b = Team("Team B", [])
    match = Match(team_a, team_b)

    match.add_event(
        MessageKey.PASS,
        player="Player A",
        receiver="Player B"
    )

    assert match.events[0]["data"]["player"] == "Player A"
    assert match.events[0]["data"]["receiver"] == "Player B"


def test_pass_event(monkeypatch):
    """Checks that a successful pass creates a PASS event."""
    ball_carrier = Player(50, 0, "Ball Carrier", 3)
    receiver = Player(50, 0, "Receiver", 4)
    defeated_player = Player(50, 0, "Defeated Player", 3)

    team_a = Team("Team A", [ball_carrier, receiver])
    team_b = Team("Team B", [defeated_player])

    team_a.formation[Zone.MIDFIELD].append(ball_carrier)
    team_a.formation[Zone.ATTACK].append(receiver)
    team_b.formation[Zone.MIDFIELD].append(defeated_player)

    match = Match(team_a, team_b)

    midfield_result = MidfieldResult(
        team_a,
        ball_carrier,
        None,
        defeated_player
    )

    monkeypatch.setattr(
        match_engine,
        "process_midfield",
        lambda team_a, team_b: midfield_result
    )

    monkeypatch.setattr(
        match_engine,
        "player_decide_action",
        lambda player: PlayerAction.PASS
    )

    monkeypatch.setattr(
        match_engine,
        "process_attack",
        lambda attacker, defending_team, attacking_team, match: None
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    match_engine.process_play(match)

    pass_events = [
        event for event in match.events
        if event["key"] is MessageKey.PASS
    ]

    assert len(pass_events) == 1
    assert pass_events[0]["data"]["player"] == ball_carrier.name
    assert pass_events[0]["data"]["receiver"] == receiver.name


def test_goal_event(monkeypatch):
    """Checks that a successful goal creates a GOAL event."""
    attacker = Player(50, 0, "Attacker", 4)

    attacking_team = Team("Team A", [attacker])
    defending_team = Team("Team B", [])
    match = Match(attacking_team, defending_team)

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: None
    )

    monkeypatch.setattr(
        match_engine,
        "goal_attempt",
        lambda attacker: True
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert any(
        event["key"] is MessageKey.GOAL
        for event in match.events
    )


def test_goal_missed_event(monkeypatch):
    """Checks that a missed goal creates a GOAL_MISSED event."""
    attacker = Player(50, 0, "Attacker", 4)

    attacking_team = Team("Team A", [attacker])
    defending_team = Team("Team B", [])
    match = Match(attacking_team, defending_team)

    monkeypatch.setattr(
        match_engine,
        "process_zone_attack",
        lambda attacker, defending_team, zone: None
    )

    monkeypatch.setattr(
        match_engine,
        "goal_attempt",
        lambda attacker: False
    )

    monkeypatch.setattr(
        match_engine,
        "sleep",
        lambda seconds: None
    )

    match_engine.process_attack(
        attacker,
        defending_team,
        attacking_team,
        match
    )

    assert any(
        event["key"] is MessageKey.GOAL_MISSED
        for event in match.events
    )


def test_event_order_is_preserved():
    """Checks that events remain stored in the order they were added."""
    team_a = Team("Team A", [])
    team_b = Team("Team B", [])
    match = Match(team_a, team_b)

    match.add_event(
        MessageKey.ATTACK_ZONE,
        attacker="Player"
    )

    match.add_event(
        MessageKey.GOAL_ATTEMPT
    )

    match.add_event(
        MessageKey.GOAL,
        team="Team A"
    )

    assert match.events[0]["key"] is MessageKey.ATTACK_ZONE
    assert match.events[1]["key"] is MessageKey.GOAL_ATTEMPT
    assert match.events[2]["key"] is MessageKey.GOAL



# ============================================================================
# MATCH TESTS
# ============================================================================

def test_match_ends_normally(monkeypatch):
    """Checks that a normal match reaches fulltime."""
    player_a = Player(50, 0, "Player A", 3)
    player_b = Player(50, 0, "Player B", 3)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    match = Match(team_a, team_b)

    monkeypatch.setattr(
        match_processor.dice,
        "roll_1d10",
        lambda: 0
    )

    monkeypatch.setattr(
        match_processor,
        "sleep",
        lambda seconds: None
    )

    match_processor.process_match(match)

    assert any(
        event["key"] is MessageKey.FULLTIME
        for event in match.events
    )


def test_match_draw(monkeypatch):
    """Checks that equal scores result in a draw."""
    player_a = Player(50, 0, "Player A", 3)
    player_b = Player(50, 0, "Player B", 3)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    match = Match(team_a, team_b)

    monkeypatch.setattr(
        match_processor.dice,
        "roll_1d10",
        lambda: 0
    )

    monkeypatch.setattr(
        match_processor,
        "sleep",
        lambda seconds: None
    )

    match_processor.process_match(match)

    assert any(
        event["key"] is MessageKey.DRAW
        for event in match.events
    )

    assert player_a.xp == 0
    assert player_b.xp == 0


def test_match_team_a_wins_by_score(monkeypatch):
    """Checks that Team A wins when Team A has the higher score."""
    player_a = Player(50, 0, "Player A", 3)
    player_b = Player(50, 0, "Player B", 3)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    team_a.score = 2
    team_b.score = 1

    match = Match(team_a, team_b)

    monkeypatch.setattr(
        match_processor.dice,
        "roll_1d10",
        lambda: 0
    )

    monkeypatch.setattr(
        match_processor,
        "sleep",
        lambda seconds: None
    )

    match_processor.process_match(match)

    assert player_a.xp == rules.Xp.MATCH_WIN
    assert player_b.xp == 0


def test_match_team_b_wins_by_score(monkeypatch):
    """Checks that Team B wins when Team B has the higher score."""
    player_a = Player(50, 0, "Player A", 3)
    player_b = Player(50, 0, "Player B", 3)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    team_a.score = 1
    team_b.score = 2

    match = Match(team_a, team_b)

    monkeypatch.setattr(
        match_processor.dice,
        "roll_1d10",
        lambda: 0
    )

    monkeypatch.setattr(
        match_processor,
        "sleep",
        lambda seconds: None
    )

    match_processor.process_match(match)

    assert player_b.xp == rules.Xp.MATCH_WIN
    assert player_a.xp == 0


def test_match_ends_on_elimination(monkeypatch):
    """Checks that the match ends when one team is already eliminated."""
    player_a = Player(50, 0, "Player A", 3)
    player_b = Player(0, 0, "Player B", 3)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    match = Match(team_a, team_b)

    process_play_calls = 0

    def test_process_play(match):
        nonlocal process_play_calls
        process_play_calls += 1

    monkeypatch.setattr(
        match_processor,
        "process_play",
        test_process_play
    )

    monkeypatch.setattr(
        match_processor,
        "sleep",
        lambda seconds: None
    )

    match_processor.process_match(match)

    assert process_play_calls == 0

    assert any(
        event["key"] is MessageKey.TEAM_ELIMINATED
        for event in match.events
    )


def test_elimination_in_minute_60(monkeypatch):
    """Checks that elimination is detected correctly in minute 60."""
    player_a = Player(50, 0, "Player A", 3)
    player_b = Player(50, 0, "Player B", 3)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    match = Match(team_a, team_b)

    rolls = iter([0] * 59 + [10])

    monkeypatch.setattr(
        match_processor.dice,
        "roll_1d10",
        lambda: next(rolls)
    )

    def test_process_play(match):
        player_b.hp = 0

    monkeypatch.setattr(
        match_processor,
        "process_play",
        test_process_play
    )

    monkeypatch.setattr(
        match_processor,
        "sleep",
        lambda seconds: None
    )

    match_processor.process_match(match)

    assert player_b.hp == 0

    assert any(
        event["key"] is MessageKey.TEAM_ELIMINATED
        for event in match.events
    )


def test_elimination_score_is_adjusted(monkeypatch):
    """Checks that elimination creates at least a three point lead."""
    player_a = Player(50, 0, "Player A", 3)
    player_b = Player(0, 0, "Player B", 3)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    team_a.score = 1
    team_b.score = 2

    match = Match(team_a, team_b)

    monkeypatch.setattr(
        match_processor,
        "sleep",
        lambda seconds: None
    )

    match_processor.process_match(match)

    assert team_a.score == 3
    assert team_b.score == 0


def test_existing_larger_lead_is_preserved(monkeypatch):
    """Checks that an existing larger lead is preserved after elimination."""
    player_a = Player(50, 0, "Player A", 3)
    player_b = Player(0, 0, "Player B", 3)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    team_a.score = 6
    team_b.score = 1

    match = Match(team_a, team_b)

    monkeypatch.setattr(
        match_processor,
        "sleep",
        lambda seconds: None
    )

    match_processor.process_match(match)

    assert team_a.score == 6
    assert team_b.score == 1


def test_match_winner_gets_match_win_xp(monkeypatch):
    """Checks that all winning team players receive MATCH_WIN XP."""
    player_a_1 = Player(50, 0, "Player A1", 3)
    player_a_2 = Player(0, 0, "Player A2", 3)
    player_b = Player(50, 0, "Player B", 3)

    team_a = Team("Team A", [player_a_1, player_a_2])
    team_b = Team("Team B", [player_b])

    team_a.score = 1
    team_b.score = 0

    match = Match(team_a, team_b)

    monkeypatch.setattr(
        match_processor.dice,
        "roll_1d10",
        lambda: 0
    )

    monkeypatch.setattr(
        match_processor,
        "sleep",
        lambda seconds: None
    )

    match_processor.process_match(match)

    assert player_a_1.xp == rules.Xp.MATCH_WIN
    assert player_a_2.xp == rules.Xp.MATCH_WIN


def test_loser_gets_no_match_win_xp(monkeypatch):
    """Checks that losing team players receive no MATCH_WIN XP."""
    player_a = Player(50, 0, "Player A", 3)
    player_b = Player(50, 0, "Player B", 3)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    team_a.score = 1
    team_b.score = 0

    match = Match(team_a, team_b)

    monkeypatch.setattr(
        match_processor.dice,
        "roll_1d10",
        lambda: 0
    )

    monkeypatch.setattr(
        match_processor,
        "sleep",
        lambda seconds: None
    )

    match_processor.process_match(match)

    assert player_b.xp == 0


def test_team_eliminated_event(monkeypatch):
    """Checks that elimination creates a TEAM_ELIMINATED event."""
    player_a = Player(50, 0, "Player A", 3)
    player_b = Player(0, 0, "Player B", 3)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    match = Match(team_a, team_b)

    monkeypatch.setattr(
        match_processor,
        "sleep",
        lambda seconds: None
    )

    match_processor.process_match(match)

    assert any(
        event["key"] is MessageKey.TEAM_ELIMINATED
        for event in match.events
    )


def test_halftime_event(monkeypatch):
    """Checks that halftime creates a HALFTIME event."""
    player_a = Player(50, 0, "Player A", 3)
    player_b = Player(50, 0, "Player B", 3)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    match = Match(team_a, team_b)

    monkeypatch.setattr(
        match_processor.dice,
        "roll_1d10",
        lambda: 0
    )

    monkeypatch.setattr(
        match_processor,
        "sleep",
        lambda seconds: None
    )

    match_processor.process_match(match)

    assert any(
        event["key"] is MessageKey.HALFTIME
        for event in match.events
    )


def test_fulltime_event(monkeypatch):
    """Checks that match end creates a FULLTIME event."""
    player_a = Player(50, 0, "Player A", 3)
    player_b = Player(50, 0, "Player B", 3)

    team_a = Team("Team A", [player_a])
    team_b = Team("Team B", [player_b])

    match = Match(team_a, team_b)

    monkeypatch.setattr(
        match_processor.dice,
        "roll_1d10",
        lambda: 0
    )

    monkeypatch.setattr(
        match_processor,
        "sleep",
        lambda seconds: None
    )

    match_processor.process_match(match)

    assert any(
        event["key"] is MessageKey.FULLTIME
        for event in match.events
    )


