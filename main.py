import config.rules
import engine
from domain.player import Player
import engine.match_engine as match_engine
from domain.team import Team
from domain.zones import Zone
from domain.player_action import PlayerAction
from time import sleep
from engine.dice import roll_1d10


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


c = 0
attack_possibility = 8
for minute in range(1, 61):
    d_result = roll_1d10()
    if d_result >= attack_possibility:
        c += 1
        print("Minute", minute, f"(Action #{c})")
        match_engine.process_play(team_a,team_b)
    if minute == 30:
        print("HALFTIME!")
        sleep(2)
print("FULLTIME")
print("Score:", team_a.name, team_a.score)
print("Score:", team_b.name, team_b.score)
winner_team = None
loser_team = None
if team_a.score > team_b.score:
    winner_team = team_a
    loser_team = team_b
elif team_b.score > team_a.score:
    winner_team = team_b
    loser_team = team_a
elif team_a.score == team_b.score:
    winner_team = None
    loser_team = None

if winner_team:
    print("Winner is", winner_team.name)
    for player in winner_team.players:
        player.xp += config.rules.Xp.MATCH_WIN
        print(player.name, player.xp, player.hp)
else:
    print("Draw Game!")
exit()