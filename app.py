import secrets
from utils import connect
from utils.hash import hash
from utils.roles import Player

def randombase64(length):
    return secrets.token_urlsafe(length * 3 // 4)

class App:
    def __init__(self, db: str):
        self._conn = connect(db)
    
    def _create_user(self, username: str, password: str):
        password_hash = hash(password)
        player_id = randombase64(50)
        player = Player(player_id, username, password_hash, 0, 0, 0, exists_in_system=False)

        # Execute the player
        player._sql(self._conn, True)
        self._player = player
        return player

    def _login(self, username: str, password: str):
        password_hash = hash(password)
        sql = f"""
            SELECT * FROM player WHERE player.username = {username} AND player.passwordHash = {password_hash}
        """
        player_tup = self._conn.cursor().execute(sql).fetchone()
        if player_tup is None:
            raise ValueError('Username or Password Incorrect')
        player = Player(*player_tup)
        self._player = player
        return player
