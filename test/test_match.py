import engine.match_processor as match_processor

from config import rules
from domain.match import Match
from domain.player import Player
from domain.team import Team
from i18n.message_key import MessageKey


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