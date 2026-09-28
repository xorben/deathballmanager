from domain.player import Player
import engine.match_engine as match_engine

attacker = Player(100, 0, "Crusher", 5)
defender = Player(100, 0, "Smasher", 4)

winner, loser, damage, winner_gained_xp = match_engine.process_duel(attacker, defender)
print(attacker.name, "attacks", defender.name)
print("Winner", winner.name)
print("Loser", loser.name)
print(loser.name, "lost HP:", damage, "-> Now has", loser.hp)
print(winner.name, "gains XP:", winner_gained_xp, "-> Now has", winner.xp)
if loser.hp == 0:
    print(loser.name, "is KO!")
