import engine.duel as duel_engine

from config import rules
from domain.player import Player
from engine.duel import duel
from engine.match_engine import process_duel


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

    assert result.attacker is attacker
    assert result.defender is defender
    assert result.winner is attacker
    assert result.loser is defender
    assert result.damage == 10
    assert result.lost_hp == 10
    assert result.ko is True