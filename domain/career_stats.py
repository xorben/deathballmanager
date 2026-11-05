from dataclasses import dataclass

@dataclass
class CareerStats:
    match_wins: int = 0
    match_losses: int = 0
    match_draws: int = 0
    goal_hits: int = 0
    goal_misses: int = 0
    duels_won: int = 0
    duels_lost: int = 0
    ko_inflicted: int = 0
    ko_received: int = 0

