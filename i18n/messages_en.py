from i18n.message_key import MessageKey


messages = {
    MessageKey.MATCH_START: "{team_a} vs {team_b}",
    MessageKey.MINUTE_ACTION: "### Minute {minute} (Action #{action_number})",
    MessageKey.HALFTIME: "#### HALFTIME!",
    MessageKey.FULLTIME: "##### FULLTIME",
    MessageKey.SCORE: "Score: {team} {score}",
    MessageKey.WINNER: "Winner is {team}",
    MessageKey.DRAW: "Draw Game!",

    MessageKey.MIDFIELD_DUEL: "{player_a} fights against {player_b}",
    MessageKey.MIDFIELD_NO_OPPONENT: "{player} takes possession without opposition.",

    MessageKey.PASS: "{player} passed ball to {receiver}",
    MessageKey.CHARGE: "{player} charges to attack zone!",

    MessageKey.ATTACK_ZONE: "{attacker} attacking attack zone!",
    MessageKey.DEFENSE_DUEL: "{attacker} fights against {defender}",
    MessageKey.DEFENSE_EMPTY: "Enemy defense is empty. {attacker} is running towards the goal!",
    MessageKey.ATTACK_STOPPED: "{attacker} got stopped by {defender}",

    MessageKey.GOAL_ATTEMPT: "Goal attempt",
    MessageKey.GOAL: "GOAL!!!\nPoint for {team}",
    MessageKey.GOAL_MISSED: "Missed goal...",

    MessageKey.HP_LOST: "{player} lost HP: {lost_hp} -> Now has {hp}",
    MessageKey.XP_GAINED: "{player} gains XP: {gained_xp} -> Now has {xp}",
    MessageKey.PLAYER_KO: "{player} is KO!",

    MessageKey.TEAM_ELIMINATED: "{team} is eliminated!",
    MessageKey.BOTH_TEAMS_ELIMINATED: "Both teams eliminated!"
}
