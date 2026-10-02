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
team_a.formation["defense"].append(team_a.players[1])
team_a.formation["defense"].append(team_a.players[2])
team_a.formation["midfield"].append(team_a.players[0])
team_a.formation["attack"].append(team_a.players[3])
team_a.formation["attack"].append(team_a.players[4])


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
team_b.formation["defense"].append(team_b.players[1])
team_b.formation["defense"].append(team_b.players[2])
team_b.formation["midfield"].append(team_b.players[0])
team_b.formation["attack"].append(team_b.players[3])
team_b.formation["attack"].append(team_b.players[4])





attacker = team_a.players[1]
defender = match_engine.select_random_player_in_zone(team_b, "defense")

dresult = match_engine.process_duel(attacker, defender)
print(attacker.name, "attacks", defender.name)
print("Winner", dresult.winner.name)
print("Loser", dresult.loser.name)
print(dresult.loser.name, "lost HP:", dresult.lost_hp, "-> Now has", dresult.loser.hp)
print(dresult.winner.name, "gains XP:", dresult.gained_xp, "-> Now has", dresult.winner.xp)
if dresult.ko == True:
    print(dresult.loser.name, "is KO!")
