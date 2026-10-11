from domain.player import Player
import engine.match_engine as match_engine
from domain.team import Team
from domain.zones import Zone
from domain.player_action import PlayerAction
from time import sleep

team_a = Team(
    "Solar Smashers",
    [
        Player(0, 0, "Dominator", 2),
        Player(100, 0, "Slasher", 4),
        Player(100, 0, "Beastmaster", 4),
        Player(100, 0, "Godslayer", 3),
        Player(100, 0, "Tearmaker", 5)
    ]
)
team_a.formation[Zone.DEFENSE].append(team_a.players[1])
team_a.formation[Zone.DEFENSE].append(team_a.players[2])
team_a.formation[Zone.MIDFIELD].append(team_a.players[0])
team_a.formation[Zone.ATTACK].append(team_a.players[3])
team_a.formation[Zone.ATTACK].append(team_a.players[4])


team_b = Team(
    "Lunar Ionstorm",
    [
        Player(100, 0, "Fistor", 3),
        Player(100, 0, "Hammerslammer", 5),
        Player(100, 0, "Masterblaster", 4),
        Player(100, 0, "Angelraper", 4),
        Player(100, 0, "Ironsight", 2)
    ]
)
team_b.formation[Zone.DEFENSE].append(team_b.players[1])
team_b.formation[Zone.DEFENSE].append(team_b.players[2])
team_b.formation[Zone.MIDFIELD].append(team_b.players[0])
team_b.formation[Zone.ATTACK].append(team_b.players[3])
team_b.formation[Zone.ATTACK].append(team_b.players[4])


mf_result, player_action, a_result = match_engine.process_play(
    team_a,
    team_b
)

""" Bausteine
"""
exit()