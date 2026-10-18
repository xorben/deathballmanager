from domain.team import Team
from config import settings
from engine.match_engine import is_team_eliminated, process_play
from engine import dice
from i18n.message_key import MessageKey
from i18n.messages_en import messages
from time import sleep
from config import rules

def process_match(team_a: Team, team_b: Team) -> None:
    """Processes whole match."""
    winner_team = None
    loser_team = None
    c = 0
    attack_possibility = settings.ATTACK_POSIBILITY
    for minute in range(1, 61):
        is_team_a_eliminated = is_team_eliminated(team_a)
        is_team_b_eliminated = is_team_eliminated(team_b)
        if not is_team_a_eliminated and not is_team_b_eliminated:
            # Both teams are alive
            d_result = dice.roll_1d10()
            if d_result >= attack_possibility:
                c += 1
                print(messages[MessageKey.MINUTE_ACTION].format(minute=minute,action_number=c))
                process_play(team_a, team_b)
                # process_play may have eliminated a team
                is_team_a_eliminated = is_team_eliminated(team_a)
                is_team_b_eliminated = is_team_eliminated(team_b)
                if is_team_a_eliminated != is_team_b_eliminated:
                    if is_team_a_eliminated:
                        winner_team = team_b
                        loser_team = team_a
                    else:
                        winner_team = team_a
                        loser_team = team_b
                    break

                    print(
                        messages[MessageKey.TEAM_ELIMINATED].format(
                            team=loser_team.name
                        )
                    )
            if minute == 30:
                print(messages[MessageKey.HALFTIME])
                sleep(2)
        elif is_team_a_eliminated != is_team_b_eliminated:
            c += 1
            print(messages[MessageKey.MINUTE_ACTION].format(minute=minute, action_number=c))
            # One team is eliminated
            if is_team_a_eliminated:
                winner_team = team_b
                loser_team = team_a
            elif is_team_b_eliminated:
                winner_team = team_a
                loser_team = team_b
            print(messages[MessageKey.TEAM_ELIMINATED].format(team=loser_team.name))
            if winner_team.score <= loser_team.score:
                winner_team.score = 3
                loser_team.score = 0
            elif winner_team.score - loser_team.score < 3:
                winner_team.score = loser_team.score + 3
            break
        elif is_team_a_eliminated and is_team_b_eliminated:
            # Booth teams are eliminated
            c += 1
            print(messages[MessageKey.MINUTE_ACTION].format(minute=minute, action_number=c))
            print(messages[MessageKey.BOTH_TEAMS_ELIMINATED])
            break
        elif is_team_a_eliminated and is_team_b_eliminated:
            print(messages[MessageKey.BOTH_TEAMS_ELIMINATED])
            break



    print(messages[MessageKey.FULLTIME])
    print(messages[MessageKey.SCORE].format(team=team_a.name, score=team_a.score))
    print(messages[MessageKey.SCORE].format(team=team_b.name, score=team_b.score))


    if team_a.score > team_b.score:
        winner_team = team_a
        loser_team = team_b
    elif team_b.score > team_a.score:
        winner_team = team_b
        loser_team = team_a
    elif team_a.score == team_b.score:
        winner_team = None
        loser_team = None

    if winner_team:
        for player in winner_team.players:
            player.xp += rules.Xp.MATCH_WIN
        print(messages[MessageKey.WINNER].format(team=winner_team.name))
        print(winner_team.get_player_stats())
        print(loser_team.get_player_stats())
    else:
        print(messages[MessageKey.DRAW])