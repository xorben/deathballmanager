import engine.match_engine as match_engine

from config import rules
from domain.match import Match
from domain.player import Player
from domain.team import Team
from domain.zones import Zone
from engine.duel_result import DuelResult


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