from domain.player import Player
from domain.team import Team
from domain.zones import Zone
from engine import match_processor
from domain.match import Match
from domain.career_stats import CareerStats
import config.implants as implants

team_a = Team(
    "Solar Smashers",
    [
        Player(50, 0, "Dominator", 2,
               1001,30, 0, Zone.MIDFIELD,
               20, CareerStats()),
        Player(50, 0, "Slasher", 4,
               1002,30, 0, Zone.DEFENSE,
               19, CareerStats()),
        Player(50, 0, "Beastmaster", 4,
               1003,30, 0, Zone.DEFENSE,
               21, CareerStats()),
        Player(50, 0, "Godslayer", 3,
               1004,30, 0, Zone.ATTACK,
               20, CareerStats()),
        Player(50, 0, "Tearmaker", 5,
               1005,30, 0, Zone.ATTACK,
               20, CareerStats())
    ]
)
team_a.players[0].install_implant(implants.HELMET_1)
print(team_a.players[0].implants)
team_a.players[0].remove_implant(implants.HELMET_1)
print(team_a.players[0].implants)
exit()

team_a.formation[Zone.DEFENSE].append(team_a.players[1])
team_a.formation[Zone.DEFENSE].append(team_a.players[2])
team_a.formation[Zone.MIDFIELD].append(team_a.players[0])
team_a.formation[Zone.ATTACK].append(team_a.players[3])
team_a.formation[Zone.ATTACK].append(team_a.players[4])

exit()

team_b = Team(
    "Lunar Ionstorm",
    [
        Player(50, 0, "Fistor", 3),
        Player(50, 0, "Hammerslammer", 5),
        Player(50, 0, "Masterblaster", 4),
        Player(50, 0, "Angelraper", 4),
        Player(50, 0, "Ironsight", 2)
    ]
)
team_b.formation[Zone.DEFENSE].append(team_b.players[1])
team_b.formation[Zone.DEFENSE].append(team_b.players[2])
team_b.formation[Zone.MIDFIELD].append(team_b.players[0])
team_b.formation[Zone.ATTACK].append(team_b.players[3])
team_b.formation[Zone.ATTACK].append(team_b.players[4])


match = Match(team_a, team_b)
match_processor.process_match(match)
for event in match.events:
    print(event)
exit()