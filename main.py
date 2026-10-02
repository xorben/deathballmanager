from domain.player import Player
import engine.match_engine as match_engine
from domain.team import Team
from random import choice
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

active_players_a = match_engine.decide_active_player(team_a)
active_players_b = match_engine.decide_active_player(team_b)
for player in active_players_a:
    print("Team A", player.name, player.hp)
for player in active_players_b:
    print("Team B", player.name, player.hp)


attacker = choice(active_players_a)
defender = choice(active_players_b)

dresult = match_engine.process_duel(attacker, defender)
print(attacker.name, "attacks", defender.name)
print("Winner", dresult.winner.name)
print("Loser", dresult.loser.name)
print(dresult.loser.name, "lost HP:", dresult.lost_hp, "-> Now has", dresult.loser.hp)
print(dresult.winner.name, "gains XP:", dresult.gained_xp, "-> Now has", dresult.winner.xp)
if dresult.ko == True:
    print(dresult.loser.name, "is KO!")
