from domain.player import Player
import engine.duel as duel

attacker = Player(100, 0, "Crusher", 5)
defender = Player(100, 0, "Smasher", 4)

winner, loser, damage = duel.duel(attacker, defender)
print(attacker.name, "attacks", defender.name)
print("Winner", winner.name)
print("Loser", loser.name)
print("Damage", damage)