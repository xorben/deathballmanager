import engine.duel as duel_engine

from domain.player import Player
from domain.team import Team
from domain.zones import Zone
from engine.match_engine import process_midfield


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