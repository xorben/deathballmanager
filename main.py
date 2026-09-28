from domain.player import Player
import engine.duel as duel

player_a = Player(100, 0, "Crusher", 5)
player_b = Player(100, 0, "Smasher", 4)

winner = duel.duel(player_a, player_b)
print(winner.name)