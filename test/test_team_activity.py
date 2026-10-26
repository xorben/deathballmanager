"""
get_all_active_player() liefert nur Spieler mit hp > 0
is_team_eliminated() → True, wenn alle HP 0 sind
is_team_eliminated() → False, wenn mindestens ein Spieler aktiv ist
select_random_player_in_zone() → None, wenn Zone leer ist
select_random_player_in_zone() → liefert nur aktive Spieler
select_midfield_player() → nimmt MIDFIELD-Spieler
select_midfield_player() → fällt bei leerem Midfield auf DEFENSE zurück
select_midfield_player() → fällt danach auf ATTACK zurück
"""

from domain.player import Player
from domain.team import Team
from engine.match_engine import (get_all_active_player,
                                 is_team_eliminated,
                                 select_random_player_in_zone,
                                 select_midfield_player
                                 )
from domain.zones import Zone

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
    assert result in [team.players[1], team.players[2]]
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
    team.formation[Zone.DEFENSE].append(team.players[1])
    team.formation[Zone.DEFENSE].append(team.players[2])
    team.formation[Zone.DEFENSE].append(team.players[0])
    result = select_random_player_in_zone(team, Zone.DEFENSE)
    assert result is None


def test_select_midfield_player_from_midfield():
    """Checks that an active player from MIDFIELD is selected first.."""
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
    """Checks that a DEFENSE player was """"— Prüft, dass bei leerem/inaktivem Midfield auf DEFENSE ausgewichen wird.
#test_select_midfield_player_fallback_attack — Prüft, dass erst dann auf ATTACK ausgewichen wird, wenn auch Defense nichts liefert.