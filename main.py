import sqlite3
from app import Interface
from utils.roles.admins import bfs
from utils.roles.tables import Quest

# conn = sqlite3.connect('last_fantasy_xd_2.db')

# first_quest = conn.cursor().execute('select * from quest where prereqsEXP = 0').fetchone()

# first_quest = Quest(*first_quest)

# print(bfs(first_quest, conn))

app = Interface('last_fantasy_xd_2.db', 'Last Fantasy XD 2')
app.run()
