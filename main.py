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



mf_result = match_engine.process_midfield(team_a, team_b)
print(mf_result.ball_carrier, "fights against", mf_result.defeated_player)
sleep(1)
attacking_team = mf_result.winning_team
if attacking_team == team_a:
    defending_team = team_b
else:
    defending_team = team_a
attacker = mf_result.ball_carrier
player_action = match_engine.player_decide_action(attacker)
if player_action == PlayerAction.PASS:
    passed_to_player = match_engine.select_random_player_in_zone(attacking_team, Zone.ATTACK)
    if passed_to_player is not None:
        print(attacker.name, "passed ball to", passed_to_player.name)
        attacker = passed_to_player
    else:
        print(attacker.name, "charges to attack zone!")
        player_action = PlayerAction.CHARGE
a_result = match_engine.process_attack(attacker, defending_team, attacking_team)
print(a_result.stopped)


exit()