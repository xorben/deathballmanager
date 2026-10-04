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