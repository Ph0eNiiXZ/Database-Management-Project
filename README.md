# Database Management Project: Last Fantasy XD 2

## About this project

A project for SCIM252, Mahidol University, based on the Multiplayer RPG game with Guild System and Quests.

## Code Documentation

### **Utility Classes and Functions**

### tables

There are classes constructed based on `dataclasses` module in **utils.tables**. It is for encapsulating the data obtained from SQL database into digestible and computable classes in python.

**IMPORTANT REMARKS**: All methods classes in this module requires the parameter `conn` which is the connector to a database. 

### Player

This is the main class for handling the **player** data, containing the query for **inventory**, **characters**, **quests** and some mutations like **change_password**, **change_username**, **transactions** and more.

#### Attributes

- **playerID**: The ID of a player, this will be auto-generated using random base64
- **username**: The username of a player
- **password_hash**: The SHA256 hash value of a player's password using salt techniques
- **exp**: Experience Points of a player
- **money**: In game currency of a player
- **rank_score**: The rank score of a player
- **guildID**: The guild ID of a player

#### Query

- `guild()`: Returns a guild data where a player is in
- `inventory()`: Returns an item inventory of a player
- `character()`: Returns characters that a player owns
- `quest()`: Returns quests that a player has completed
- `level()`: Returns the level of a player based on the EXP

#### Mutations

- `change_password(old_password, new_password)`: Changes the password of a player, requires an old password for the identification
- `change_username(password, new_username)`: Changes the username of a player, requires a password for the identification
- `change_guild(guildID)`: Changes the guildID of a player 
- `transact(price)`: Remove the money from a player
    - **remarks**: if a player receives the in-game currency, you can use the negative price because i am lazy to write another one lol
- `exp_increase(exp_reward)`: Increase the EXP of a player
- `receieve_item(itemID)`: A player receives an item.
- `receieve_character(charID)`: A player receives a character
- `buy_item(itemID)`: A player buys an item
- `buy_character(charID)`: A player buys a character
- `use_item(itemID)`: A player uses an item
- `_sql()`: Translate a player data into the SQL string and insert it into a table

### Item

This is the class for handling the **item** data, containing some necessary item data attributes.

#### Attributes

- **itemID**: ID of an item
- **itemName**: Name of an item
- **itemTypeID**: The ID of the Item Type 
- **itemClassID**: The ID of the Item Class
- **itemDescription**: The description of an item
- **price**: The price of an item

#### Query

TBA

### Character

This is the class for handling the in-game character, containing some necessary attributes to collect the character's data

#### Attributes

- **charID**: The ID of a character
- **charName**: The name of a character
- **charDescription**: The description of a character
- **charClassID**: The ID of a character class
- **charHP**: The Health Point of a character
- **charATK**: The Attack Damage of a character
- **charDEF**: The Defense Power of a character
- **price**: The price of a character

#### Query

TBA

### Guild

This is the class for handling the guild data, containing some necessary guild data attributes ex. **guildName**, **guildEXP** and some necessary query and mutation functions.

#### Attributes

- **guildID**: The ID of the guild
- **guildName**: The Name of the guild
- **guildEXP**: The Experience Points of the guild

#### Query

- `players()`: List all players who are in the guild

#### Mutations

- `exp_increase(exp_reward)`: Rewarding the EXP for the guild

### Quest

This is the class for handling the quests, containing some necessary quest data attributes and query.

#### Attributes

- **questID**: The ID of the quest
- **questName**: The Name of the quest
- **questDescription**: The Description of the quest
- **prereqsEXP**: The experience points required to unlock the quest
- **expReward**: The experience point reward obtained after completing the quest
- **moneyReward**: The in-game currency reward obtained after completing the quest

#### Query

- `prereqs_quest()`: The quests required to unlock the quest
- `prereqs_item()`: The items required to unlick the quest
- `quest_successor()`: The quests unlocked after completing the quest

### app

### App

This is the class for constructing an app to simulate the case scenarios, contains some methods for players, ex. **register** and **login**

#### Registration

After a player enters their necessary data for registration, the data will be processed using `_create_user(username, password)` method, which will insert the player into a database and return a `Player` class.

#### Login

After a player enters their credentials for logging into a game, the credentials will be processed using the `_login(username, password)` method. If the username and the password matches, the `Player` class of that player will be returned.

## Case Scenarios

### Case Scenario 1: A player register and login

#### A player Registers

A player will input their **username** and **password**, assume that the username they have inputted is unique. We then return some necessary player attributes.

#### A player logins

A player will input their **username** and **password** in order to login. We then verify if the username and password is correct, then log them in.

### Case Scenario 2: A player requests to see their necessary data

A player requests to see their necessary data, to be precise, these are the list of which should be shown **explicitly** when the player requests their data
- **Inventory**: Contains some necessary items attributes and amount of the item
- **Characters**: Contains some necessary character attributes and the experience point of each character
- **Level**: Contains the experience points and the level of a player

### Case Scenario 3: A player requests and completes a quest

NOTE: This part hasn't been written yet, but I will write it later I promise - TG

#### A player requests a quest

A player will request a quest based on quest ID, then we need to check if the player data matches the requirements to receive the quest. Then we provide them a quest they requested.

#### A player completes a quest

A player will submit a quest based on a quest ID, then we need to give them reward, containing **EXP**, **money** and **item**.

### Case Scenario 4: A player buys an item and/or a character from a shop

A player will buy an item and a character from a shop, we need to check the money and inventory of a player in order to let them buy the item or a character.

### Case Scenario 5: A player / An analyst wants to see the pathway for the quests

We need to fetch all the quests, then plot them into a directed graph. Possibly we can do the **Bredth's First Search** in order to recommend the quest pathway for players based on the quest predecessors and successors.

<!-- hehe boi -->

### Case Scenario 6: A guild leader wants to see the best player in a guild based on the Experience Points

Self-Explanatory

### Case Scenario 7: A player changes their username / password

#### A player changes username

A player will input their new username (assume that it is unique), and the password for the identification. We then change the username for them if the password is correct.

#### A player changes password

A player will input their old password and new password, we then verify the password and change the password for them.
