from domain.zones import Zone
from domain.player import Player
class Team:
    def __init__(self, name: str, score: int = 0) -> None:
        self.name = name
        self.players = []
        self.score = score
        self.formation = {
            Zone.DEFENSE: [],
            Zone.MIDFIELD: [],
            Zone.ATTACK: []
        }


    def get_player_stats(self, match_players: bool = False) -> str:
        """Returns all player stats as dict"""
        if match_players:
            p_list = self.match_players
        else:
            p_list = self.players
        stats_str_list = []
        stats_head = f"{'Player':<20} {'STR':<5} {'HP':<5} {'XP':<5}"
        stats_str_list.append(stats_head)
        stats_line = "-" * 38
        stats_str_list.append(stats_line)
        for idx, player in enumerate(p_list):
            p_stats = f"{idx+1:>3}. {player.name:<20} {player.strength:<5} {player.hp:<5} {player.xp:<5}"
            stats_str_list.append(p_stats)
        return "\n".join(stats_str_list)


    def add_player_to_team(self, player: Player) -> None:
        if player not in self.players:
            self.players.append(player)


    def remove_player_from_team(self, player: Player) -> None:
        if player in self.players and player not in self.match_players:
            self.players.remove(player)


    @property
    def match_players(self) -> list:
        match_player_list = []
        for zone, player_list in self.formation.items():
            for player in player_list:
                match_player_list.append(player)
        return match_player_list


    def add_player_to_match_team(self, player: Player) -> None:
        if (
            len(self.match_players) <5
            and player in self.players
            and player not in self.match_players
        ):
            self.formation[player.position].append(player)


    def remove_player_from_match_team(self, player: Player) -> None:
        if player in self.match_players:
            self.formation[player.position].remove(player)
