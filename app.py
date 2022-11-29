import secrets
from utils import connect
from utils.hash import hash
from utils.roles import Player
from utils.roles.tables import Guild, Quest, Item, Character
from enum import Enum

def randombase64(length):
    return secrets.token_urlsafe(length * 3 // 4)

class Register(str, Enum):
    REGISTER = "R"
    LOGIN = "L"

class InGameOptions(str, Enum):
    SHOW_PLAYER_DATA = "1"
    REQUEST_QUEST = "2"
    COMPLETE_QUEST = "3"
    BUY_ITEM = "4"
    BUY_CHARACTER = "5"
    CHANGE_USERNAME = "6"
    CHANGE_PASSWORD = "7"
    EXIT_GAME = "X"

class App:
    def __init__(self, db: str):
        self._conn = connect(db)
    
    def _create_user(self, username: str, password: str):
        password_hash = hash(password)
        player_id = randombase64(50)
        player = Player(player_id, username, password_hash, 0, 0, 0)

        # Execute the player
        player._sql(self._conn, True)
        self._player = player
        return player

    def _login(self, username: str, password: str):
        password_hash = hash(password)
        sql = f"""
            SELECT * FROM player WHERE player.username = \"{username}\" AND player.passwordHash = \"{password_hash}\"
        """
        player_tup = self._conn.cursor().execute(sql).fetchone()
        if player_tup is None:
            raise ValueError('Username or Password Incorrect')
        player = Player(*player_tup)
        self._player = player
        return player
    
    def _get_all_quests(self):
        sql = f"""
            SELECT * FROM quest
        """
        quest_tup = self._conn.cursor().execute(sql).fetchall()
        return [Quest(*q) for q in quest_tup]
    
    def _get_all_items(self):
        sql = f"""
            SELECT * FROM item
        """
        item_tup = self._conn.cursor().execute(sql).fetchall()
        return [Item(*i) for i in item_tup]
    
    def _get_all_characters(self):
        sql = f"""
            SELECT * FROM character
        """
        chracter_tup = self._conn.cursor().execute(sql).fetchall()
        return [Character(*c) for c in chracter_tup]

class Interface(App):
    in_game_options = {
        InGameOptions.SHOW_PLAYER_DATA: "Show player data",
        InGameOptions.REQUEST_QUEST: "Request a quest",
        InGameOptions.COMPLETE_QUEST: "Complete a quest",
        InGameOptions.BUY_ITEM: "Buy an item",
        InGameOptions.BUY_CHARACTER: "Buy a character",
        InGameOptions.CHANGE_USERNAME: "Change Username",
        InGameOptions.CHANGE_PASSWORD: "Change Password",
        InGameOptions.EXIT_GAME: "Exit the game"
    }

    def __init__(self, db: str, game_title: str):
        super().__init__(db)
        self._game_title = game_title
        self._running = True
    
    @staticmethod
    def _print_line():
        print("-" * 20)
    
    def _print_title(self):
        print(f"Welcome to {self._game_title}!")
    
    def _register_login_input(self):
        available_options = [Register.REGISTER, Register.LOGIN]
        while True:
            option = input(f"Register ({Register.REGISTER}) or Login ({Register.LOGIN}):")
            if option not in available_options:
                print("Invalid input!")
            else:
                return option
    
    def _input_username_password(self):
        username = input("Username:")
        password = input("Password:")
        return username, password

    def _show_login_prompt(self):
        self._print_line()
        self._print_title()
        self._print_line()
        register_login = self._register_login_input()
        if register_login == Register.REGISTER:
            username, password = self._input_username_password()
            self._create_user(username, password)
        if register_login == Register.LOGIN:
            while True:
                password_correct = True
                try:
                    username, password = self._input_username_password()
                    self._login(username, password)
                except ValueError:
                    print("Username or password incorrect!")
                    password_correct = False
                if password_correct:
                    break
        
        return self._player

    def _print_game_prompt(self):
        print("What would you like to do today?")
        self._print_line()
        for option_input, option in self.in_game_options.items():
            print(f"{option_input}: {option}")
        self._print_line()
    
    def _get_in_game_option(self):
        self._print_game_prompt()
        selected_option = input()
        while selected_option not in self.in_game_options.keys():
            print("Invalid Option! Please try again")
            selected_option = input()
        
        return selected_option
    
    @staticmethod
    def _print_inventory(inventory: list):
        for item, count in inventory:
            itemname = item.itemName
            print(f"{itemname}: {count}")
        
    @staticmethod
    def _print_character(characters: list):
        for char, charxp in characters:
            charname = char.charName
            print(f"{charname}: {charxp} EXP")
    
    @staticmethod
    def _print_quests(quests: list):
        for quest, completed in quests:
            questname = quest.questName
            status = "Completed" if completed else "Not Completed"
            print(f"{questname}: {status}")
    
    @staticmethod
    def _print_stats(player: Player, level: int, guild: Guild):
        print("Username:", player.username)
        print("EXP:", player.exp, "| Level:", level)
        if guild != "":
            print("Guild:", guild.guildName)
    
    @staticmethod
    def _show_all_quests(quests: list[Quest]):
        print("Quests")
        for i, quest in enumerate(quests):
            print(f"{i + 1}: {quest.questName}")
    
    @staticmethod
    def _show_items(items: list[Item]):
        print("Items")
        for i, item in enumerate(items):
            print(f"{i + 1}: {item.itemName} | price: {item.price}")
    
    @staticmethod
    def _show_characters(characters: list[Character]):
        print("Characters")
        for i, character in enumerate(characters):
            print(f"{i + 1}: {character.charName} | price: {character.price}")
    
    def _show_item_detail(self, item: Item):
        print(f"Item Name: {item.itemName}")
        print(f"Item Description: {item.itemDescription}")
        itemclass = item.item_class(self._conn)
        itemtype = item.item_type(self._conn)
        print(f"{itemtype.itemTypeName}: {itemtype.itemTypeDesc}")
        print(f"{itemclass.itemClassName}: {itemclass.itemClassDesc}")
        print(f"Price: {item.price}")
    
    def _show_character_detail(self, character: Character):
        print(f"Character Name: {character.charName}")
        print(f"Character Description: {character.charDescription}")
        charclass = character.char_class(self._conn)
        print(f"{charclass.charClassName}: {charclass.charClassDesc}")
        print(f"HP: {character.charHP} | ATK: {character.charATK} | DEF: {character.charDEF}")
        print(f"Price: {character.price}")

    def _show_quest_detail(self, quest: Quest):
        print("Quest Name:", quest.questName)
        print("Description:", quest.questDescription)
        print("EXP Prerequisites:", quest.prereqsEXP)
        print("EXP Reward:", quest.expReward)
        print("Money Reward:", quest.moneyReward)
        self._print_line()
        print("Item(s) Required to receive a Quest")
        print()
        for item in quest.prereqs_item(self._conn):
            print("-", item.itemName)
        print()
        self._print_line()
        print("Quest(s) Required to receive a Quest")
        print()
        for q in quest.prereqs_quest(self._conn):
            print("-", q.questName)
        print()
        self._print_line()

    def _exit(self):
        self._running = False

    def _show_player_data(self):
        player_inventory = self._player.inventory(self._conn)
        player_characters = self._player.character(self._conn)
        player_level = self._player.level(self._conn)
        player_guild = self._player.guild(self._conn)
        player_quests = self._player.quest(self._conn)
        self._print_line()
        self._print_stats(self._player, player_level, player_guild)
        self._print_line()
        print("Inventory")
        self._print_inventory(player_inventory)
        self._print_line()
        print("Quests")
        self._print_quests(player_quests)
        self._print_line()
        print("Characters")
        self._print_character(player_characters)
        self._print_line()

    def _request_quest(self):
        all_quests = self._get_all_quests()
        self._print_line()
        self._show_all_quests(all_quests)
        while True:
            valid_quest = True
            request_quest = input("Please Request the Quest:")
            try:
                quest_requested = all_quests[int(request_quest) - 1]
            except Exception:
                valid_quest = False
                print("Invalid Input! Try again")
            if valid_quest:
                break
        
        self._show_quest_detail(quest_requested)
        confirm = input("Are you sure to request this quest? (Y/N):")
        if confirm == "Y":
            try:
                self._player.receieve_quest(quest_requested.questID, self._conn)
            except ValueError:
                print("You are still not eligible to take the quest")
            print("You have requested the quest:", quest_requested.questName)

    def _complete_quest(self):
        pending_quest = self._player.pending_quest(self._conn)
        self._print_line()
        self._show_all_quests(pending_quest)
        while True:
            valid_quest = True
            submit_quest = input("Select the Quest to submit:")
            try:
                quest_submitted = pending_quest[int(submit_quest) - 1]
            except Exception as e:
                valid_quest = False
                print("Invalid Input! Try again")
            if valid_quest:
                break
        
        confirm = input("Are you sure to submit this quest? (Y/N):")
        if confirm == "Y":
            self._player.complete_quest(quest_submitted.questID, self._conn)
            print("Submitted the Quest:", quest_submitted.questName)
    
    def _buy_item(self):
        items = self._get_all_items()
        self._print_line()
        self._show_items(items)
        print("Your current balance is:", self._player.money)
        while True:
            valid_item = True
            item_buy = input("Select the Item to buy:")
            try:
                item = items[int(item_buy) - 1]
            except Exception:
                valid_item = False
                print("Invalid Input! Try again")
            if valid_item:
                break
        
        self._show_item_detail(item)
        confirm = input("Are you sure to buy this item? (Y/N):")
        if confirm == "Y":
            try:
                self._player.buy_item(item.itemID, self._conn)
                print("Bought an item:", item.itemName)
                print("Your current balance is:", self._player.money)
            except ValueError:
                print("You don't have enough money to buy an item")

    
    def _buy_character(self):
        characters = self._get_all_characters()
        self._print_line()
        self._show_characters(characters)
        print("Your current balance is:", self._player.money)
        while True:
            valid_character = True
            character_buy = input("Select the Character to buy:")
            try:
                character = characters[int(character_buy) - 1]
            except Exception:
                valid_character = False
                print("Invalid Input! Try again")
            if valid_character:
                break
        
        self._show_character_detail(character)
        confirm = input("Are you sure to buy this character? (Y/N):")
        if confirm == "Y":
            try:
                self._player.buy_character(character.charID, self._conn)
                print("Bought a character:", character.charName)
                print("Your current balance is:", self._player.money)
            except ValueError:
                print("You don't have enough money to buy a character")
    
    def _change_username(self):
        new_username = input("New Username:")
        password = input("Enter Password for Confirmation:")

        self._player.change_username(password, new_username, self._conn)
    
    def _change_password(self):
        old_password = input("Old password:")
        new_password = input("New password:")

        self._player.change_password(old_password, new_password, self._conn)
    
    def _process_options(self):
        in_game_process = {
            InGameOptions.SHOW_PLAYER_DATA: self._show_player_data,
            InGameOptions.REQUEST_QUEST: self._request_quest,
            InGameOptions.COMPLETE_QUEST: self._complete_quest,
            InGameOptions.BUY_ITEM: self._buy_item,
            InGameOptions.BUY_CHARACTER: self._buy_character,
            InGameOptions.CHANGE_USERNAME: self._change_username,
            InGameOptions.CHANGE_PASSWORD: self._change_password,
            InGameOptions.EXIT_GAME: self._exit
        }
        return in_game_process

    def _game(self):
        process_options = self._process_options()
        while self._running:
            selected_option = self._get_in_game_option()
            process = process_options[selected_option]
            process()
        print("See you next time!")

    def run(self):
        self._show_login_prompt()
        self._game()
