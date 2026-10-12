from enum import Enum, auto


class MessageKey(Enum):
    """
    i18n solution
    """
    MATCH_START = auto()
    MINUTE_ACTION = auto()
    HALFTIME = auto()
    FULLTIME = auto()
    SCORE = auto()
    WINNER = auto()
    DRAW = auto()

    MIDFIELD_DUEL = auto()
    MIDFIELD_NO_OPPONENT = auto()

    PASS = auto()
    CHARGE = auto()

    ATTACK_ZONE = auto()
    DEFENSE_DUEL = auto()
    DEFENSE_EMPTY = auto()
    ATTACK_STOPPED = auto()

    GOAL_ATTEMPT = auto()
    GOAL = auto()
    GOAL_MISSED = auto()

    HP_LOST = auto()
    XP_GAINED = auto()
    PLAYER_KO = auto()

    TEAM_ELIMINATED = auto()
    BOTH_TEAMS_ELIMINATED = auto()