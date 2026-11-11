from domain.player import Player
from domain.team import Team
from domain.zones import Zone
from engine import match_processor
from domain.match import Match
from domain.career_stats import CareerStats
import config.implants as implants

team_a = Team(
    "Solar Smashers",
)

player_dominator = Player(50, 0, "Dominator", 2,
       1001, 30, 0, Zone.MIDFIELD,
       20, CareerStats())
player_slasher = Player(50, 0, "Slasher", 4,
       1002, 30, 0, Zone.DEFENSE,
       19, CareerStats())
player_beastmaster = Player(50, 0, "Beastmaster", 4,
       1003, 30, 0, Zone.DEFENSE,
       21, CareerStats())
player_godslayer = Player(50, 0, "Godslayer", 3,
       1004, 30, 0, Zone.ATTACK,
       20, CareerStats())
player_tearmaker = Player(50, 0, "Tearmaker", 5,
       1005, 30, 0, Zone.ATTACK,
       20, CareerStats())
player_seth = Player(50, 0, "Seth", 1,
       1006, 30, 0, Zone.MIDFIELD,
       18, CareerStats())

# all to team
team_a.add_player_to_team(player_dominator)
team_a.add_player_to_team(player_slasher)
team_a.add_player_to_team(player_beastmaster)
team_a.add_player_to_team(player_godslayer)
team_a.add_player_to_team(player_tearmaker)
team_a.add_player_to_team(player_seth)

team_a.add_player_to_match_team(player_dominator)
team_a.add_player_to_match_team(player_slasher)
team_a.add_player_to_match_team(player_beastmaster)
team_a.add_player_to_match_team(player_godslayer)
team_a.add_player_to_match_team(player_tearmaker)
team_a.add_player_to_match_team(player_seth)
print(team_a.get_player_stats(match_players=True))

exit()

team_a.match_players[0].install_implant(implants.HELMET_1)
print(team_a.match_players[0].implants)
team_a.match_players[0].remove_implant(implants.HELMET_1)
print(team_a.match_players[0].implants)
exit()


match = Match(team_a, team_b)
match_processor.process_match(match)
for event in match.events:
    print(event)
exit()