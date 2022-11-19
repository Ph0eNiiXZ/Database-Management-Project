from sqlite3 import Connection
from .tables import Quest

def bfs(quest: Quest, conn: Connection):
    """
    Case Scenario 5: A player / An analyst wants to see the pathway for the quests

    The Bredth's First Search algorithm applied for the recommendation of quest progression. 
    A player will start with the initial quest given at the beginning of the game, the proceed further through various quests
    starting from clearing the first quest, then the quest which are the successors of the first quest, and so on.
    """
    visits_id = []
    visits_quests = [quest]
    successors = quest.quest_successor(conn)
    next_visits = successors.copy()
    while len(next_visits) > 0:
        next_visit = next_visits[0]
        next_visits = next_visits[1:]
        if next_visit.questID in visits_id:
            continue
        next_visits.extend(next_visit.quest_successor(conn))
        visits_id.append(next_visit.questID)
        visits_quests.append(next_visit)
    return visits_quests
