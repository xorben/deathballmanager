import engine.match_engine as match_engine

from domain.player import Player
from engine.match_engine import goal_attempt


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