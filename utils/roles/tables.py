from sqlite3 import Connection
from dataclasses import dataclass
from utils.hash import hash

@dataclass
class Item:
    itemID: str
    itemName: str
    itemTypeID: str
    itemClassID: str
    itemDescription: str
    price: int

@dataclass
class Character:
    charID: str
    charName: str
    charDescription: str
    charClassID: str
    charHP: float
    charATK: float
    charDEF: float
    price: int

@dataclass
class Guild:
    guildID: str
    guildName: str
    guildEXP: float

    # Query

    def players(self, conn: Connection):
        sql = f"""SELECT * FROM player WHERE player.guildID = \"{self.guildID}\""""
        out = conn.cursor().execute(sql).fetchall()
        return [Player(*x) for x in out]
    
    # Mutation

    def exp_increase(self, exp_reward: float, conn: Connection, commit: bool = True):
        update_query = f"""
            UPDATE guild
            SET exp = {self.guildEXP + exp_reward}
            WHERE guildID = "{self.guildID}"
        """
        conn.cursor().execute(update_query)
        if commit:
            conn.commit()
        self.guildEXP += exp_reward

@dataclass
class Quest:
    questID: str
    questName: str
    questDescription: str
    prereqsEXP: float
    expReward: float
    moneyReward: int

    # Query

    def prereqs_quest(self, conn: Connection):
        sql = f"""SELECT quest.* FROM quest_prereqs_quest 
        JOIN quest ON quest_prereqs_quest.questPreReqsID = quest.questID AND quest_prereqs_quest.questID = \"{self.questID}\""""
        out = conn.cursor().execute(sql).fetchall()
        return [Quest(*x) for x in out]
    
    def prereqs_item(self, conn: Connection):
        sql = f"""
            SELECT item.* FROM quest_prereqs_item JOIN item 
            ON quest_prereqs_item.itemID = item.itemID AND quest_prereqs_item.questID = "{self.questID}"
        """
        out = conn.cursor().execute(sql).fetchall()
        return [Item(*x) for x in out]
    
    def quest_successor(self, conn: Connection):
        sql = f"""SELECT quest.* FROM quest_prereqs_quest 
        JOIN quest ON quest_prereqs_quest.questID = quest.questID AND quest_prereqs_quest.questPreReqsID = \"{self.questID}\""""
        out = conn.cursor().execute(sql).fetchall()
        return [Quest(*x) for x in out]

@dataclass
class Player:
    playerID: str
    username: str
    password_hash: str
    exp: float
    money: int
    rank_score: float
    guildID: str = None

    def _sql(self, conn: Connection, commit: bool = False):
        insert_sql = f"""
            INSERT INTO player (playerID, username, passwordHash, exp, money, rank_score, guildID) 
            VALUES {(self.playerID, self.username, self.password_hash, self.exp, self.money, self.rank_score, self.guildID)}
        """
        conn.cursor().execute(insert_sql)
        if commit:
            conn.commit()

    # Query

    def guild(self, conn: Connection):
        if not self.guildID:
            return
        sql = f"SELECT * FROM guild WHERE guildID = \"{self.guildID}\""
        out = conn.cursor().execute(sql).fetchone()
        return Guild(*out[0])

    def inventory(self, conn: Connection):
        sql = f"""
            SELECT item.itemID, item.itemName, item.itemTypeID, item.itemClassID, 
            item.itemDescription, item.price, playerInventory.amount
            FROM playerInventory join player ON playerInventory.playerID = "{self.playerID}" 
            AND playerInventory.playerID = player.playerID
            JOIN item on playerInventory.itemID = item.itemID
        """
        out = conn.cursor().execute(sql).fetchall()
        items_amt = [(Item(*x[:-1]), x[-1]) for x in out]
        return items_amt
    
    def character(self, conn: Connection):
        sql = f"""
            SELECT player_character.charID, character.charName, character.charDescription,
            character.charClassID, character.charHP, character.charATK, character.charDEF, character.price, 
            player_character.charEXP
            FROM player_character JOIN player ON player_character.playerID = player.playerID 
            AND player_character.playerID = "{self.playerID}"
            JOIN character on player_character.charID = character.charID
        """
        out = conn.cursor().execute(sql).fetchall()
        char_exp = [(Character(*x[:-1]), x[-1]) for x in out]
        return char_exp
    
    def quest(self, conn: Connection):
        sql = f"""
            SELECT player_quest.questID, quest.questName, quest.questDescription, quest.prereqsEXP, quest.expReward, quest.moneyReward
            FROM player_quest JOIN player ON player_quest.playerID = player.playerID
            AND player_quest.playerID = "{self.playerID}"
            JOIN quest ON player_quest.questID = quest.questID
        """
        out = conn.cursor().execute(sql).fetchall()
        return [Quest(*x) for x in out]

    def level(self, conn: Connection):
        sql = f"""
            SELECT max(level.level) FROM level WHERE level.exp_requirements <= (
                SELECT player.exp FROM player WHERE player.playerID = "1"
            )
        """
        out = conn.cursor().execute(sql).fetchone()
        return out[0]

    # Mutation

    def change_password(self, old_password: str, new_password: str, conn: Connection, commit: bool = True):
        # check if the password is right
        hash_old_password = hash(old_password)
        assert hash_old_password == self.password_hash
        # change to new password
        new_password_hash = hash(new_password)
        update_query = f"""
            UPDATE player
            SET passwordHash = "{new_password_hash}"
            WHERE playerID = "{self.playerID}"
        """
        conn.cursor().execute(update_query)
        if commit:
            conn.commit()
        self.password_hash = new_password_hash
    
    def change_username(self, password: str, new_username: str, conn: Connection, commit: bool = True):
        # check if the password is right
        hash_password = hash(password)
        assert hash_password == self.password_hash
        update_query = f"""
            UPDATE player
            SET username = "{new_username}"
            WHERE playerID = "{self.playerID}"
        """
        conn.cursor().execute(update_query)
        if commit:
            conn.commit()
        # change username
        self.username = new_username
    
    def change_guild(self, guildID: str, conn: Connection, commit: bool = True):
        update_query = f"""
            UPDATE player
            SET guildID = "{guildID}"
            WHERE playerID = "{self.playerID}"
        """
        conn.cursor().execute(update_query)
        if commit:
            conn.commit()
        self.guildID = guildID
    
    def transact(self, price: int, conn: Connection, commit: bool = True):
        assert self.money >= price
        update_query = f"""
            UPDATE player
            SET money = {self.money - price}
            WHERE playerID = "{self.playerID}"
        """
        conn.cursor().execute(update_query)
        if commit:
            conn.commit()
        self.money -= price
    
    def exp_increase(self, exp_reward: float, conn: Connection, commit: bool = True):
        update_query = f"""
            UPDATE player
            SET exp = {self.exp + exp_reward}
            WHERE player_id = "{self.playerID}"
        """
        conn.cursor().execute(update_query)
        if commit:
            conn.commit()
        self.exp += exp_reward
    
    def receive_item(self, itemID: str, conn: Connection, commit: bool = True):
        # check inventory if item exists
        inventory = self.inventory(conn)
        item_exists = False
        for item, amount in inventory:
            if item.itemID == itemID:
                update_query = f"""
                    UPDATE playerInventory
                    SET amount = {amount + 1}
                    WHERE playerID = "{self.playerID}" AND itemID = "{itemID}"
                """
                conn.cursor().execute(update_query)
                item_exists = True
                break
        
        if not item_exists:
            update_query = f"""
                INSERT INTO playerInventory (playerID, itemID, amount) VALUES ("{self.playerID}", "{itemID}", 1)
            """
            conn.cursor().execute(update_query)
        
        if commit:
            conn.commit()

    
    def receieve_character(self, charID: str, conn: Connection, commit: bool = True):
        update_query = f"""
            INSERT INTO player_character (playerID, charID, charEXP) VALUES ("{self.playerID}", "{charID}", 0)
        """
        conn.cursor().execute(update_query)

        if commit:
            conn.commit()
    
    def buy_item(self, itemID: str, conn: Connection, commit: bool = True):
        price_sql = f"""SELECT price FROM item WHERE itemID = \"{itemID}\""""
        price = conn.cursor().execute(price_sql).fetchone()[0]
        try:
            self.transact(price, conn, False)
        except AssertionError:
            raise ValueError("Transaction Failed! Player Money is not enough to purchase the item.")
        # since this is the last action, we can input the commit parameter here in order to decide whether to commit
        self.receive_item(itemID, conn, commit)
    
    def buy_character(self, charID: str, conn: Connection, commit: bool = True):
        price_sql = f"""SELECT price FROM character WHERE charID = \"{charID}\""""
        price = conn.cursor().execute(price_sql).fetchone()[0]
        try:
            self.transact(price, conn, False)
        except AssertionError:
            raise ValueError("Transaction Failed! Player Money is not enough to purchase the character.")
        # since this is the last action, we can input the commit parameter here in order to decide whether to commit
        self.receieve_character(charID, conn, commit)

    def use_item(self, itemID: str, conn: Connection, commit: bool = True):
        inventory = self.inventory(conn)
        item_exists = False
        for item, amount in inventory:
            if item.itemID == itemID:
                if amount == 1:
                    update_query = f"""
                        DELETE FROM playerInventory
                        WHERE playerID = "{self.playerID}" AND itemID = "{itemID}"
                    """
                else:
                    update_query = f"""
                        UPDATE playerInventory
                        SET amount = {amount - 1}
                        WHERE playerID = "{self.playerID}" AND itemID = "{itemID}"
                    """
                conn.cursor().execute(update_query)
                item_exists = True
                break
        
        if not item_exists:
            raise ValueError("Player doesn't have the specified item")
        
        if commit:
            conn.commit()
