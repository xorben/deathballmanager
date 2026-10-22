from domain.player import Player
from domain.team import Team
from engine.match_engine import is_team_eliminated

def test_team_is_eliminated():
    team = Team(
        "Test Team",
        [
            Player(0, 0, "Player 1", 3),
            Player(0, 0, "Player 2", 4)
        ]
    )

    result = is_team_eliminated(team)

    assert result is True


"""
#Grundaufbau
def test_irgendwas():
    # Arrange
    # Testdaten aufbauen

    # Act
    result = funktion(...)

    # Assert
    assert result == erwartetes_ergebnis
"""