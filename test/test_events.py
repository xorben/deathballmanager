import engine.match_engine as match_engine

from config import rules
from domain.match import Match
from domain.player import Player
from domain.player_action import PlayerAction
from domain.team import Team
from domain.zones import Zone
from engine.duel_result import DuelResult
from engine.midfield_result import MidfieldResult
from i18n.message_key import MessageKey


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