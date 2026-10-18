from domain.zones import Zone
class Team:
    def __init__(self, name: str, players: list, score: int = 0) -> None:
        self.name = name
        self.players = players
        self.score = score
        self.formation = {
            Zone.DEFENSE: [],
            Zone.MIDFIELD: [],
            Zone.ATTACK: []
        }


    def get_player_stats(self) -> str:
        """Returns all player stats as dict"""
        stats_str_list = []
        stats_head = f"{'Player':<20} {'STR':<5} {'HP':<5} {'XP':<5}"
        stats_str_list.append(stats_head)
        stats_line = "-" * 38
        stats_str_list.append(stats_line)
        for player in self.players:
            p_stats = f"{player.name:<20} {player.strength:<5} {player.hp:<5} {player.xp:<5}"
            stats_str_list.append(p_stats)
        return "\n".join(stats_str_list)