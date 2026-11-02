import engine.match_engine as match_engine

from domain.match import Match
from domain.player import Player
from domain.player_action import PlayerAction
from domain.team import Team
from domain.zones import Zone
from engine.midfield_result import MidfieldResult


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