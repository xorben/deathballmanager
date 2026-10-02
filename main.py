from domain.player import Player
import engine.match_engine as match_engine

attacker = Player(100, 0, "Crusher", 5)
defender = Player(100, 0, "Smasher", 4)

dresult = match_engine.process_duel(attacker, defender)
print(attacker.name, "attacks", defender.name)
print("Winner", dresult.winner.name)
print("Loser", dresult.loser.name)
print(dresult.loser.name, "lost HP:", dresult.lost_hp, "-> Now has", dresult.loser.hp)
print(dresult.winner.name, "gains XP:", dresult.gained_xp, "-> Now has", dresult.winner.xp)
if dresult.ko == True:
    print(dresult.loser.name, "is KO!")
