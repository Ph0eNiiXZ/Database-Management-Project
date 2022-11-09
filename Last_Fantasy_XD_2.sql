CREATE TABLE `player` (
  `playerID` varchar(50) PRIMARY KEY,
  `username` varchar(16),
  `passwordHash` varchar(255),
  `exp` numeric,
  `money` int,
  `rank_score` numeric,
  `guildID` varchar(50)
);

CREATE TABLE `guild` (
  `guildID` varchar(50) PRIMARY KEY,
  `guildName` varchar(16),
  `guildExp` numeric
);

CREATE TABLE `character` (
  `charID` varchar(16) PRIMARY KEY,
  `charName` varchar(16),
  `charDescription` text,
  `charClassID` varchar(16),
  `charHP` numeric,
  `charATK` numeric,
  `charDEF` numeric,
  `price` int
);

CREATE TABLE `item` (
  `itemID` varchar(16) PRIMARY KEY,
  `itemName` varchar(100),
  `itemTypeID` varchar(16),
  `itemClassID` varchar(16),
  `itemDescription` text,
  `price` int
);

CREATE TABLE `quest` (
  `questID` varchar(32) PRIMARY KEY,
  `questName` text,
  `questDescription` text,
  `prereqsEXP` numeric,
  `expReward` numeric,
  `moneyReward` int
);

CREATE TABLE `dungeon` (
  `dungeonID` varchar(32) PRIMARY KEY,
  `dungeonName` text,
  `expReward` numeric,
  `moneyReward` int
);

CREATE TABLE `monster` (
  `monsterID` varchar(32) PRIMARY KEY,
  `monsterName` text,
  `monsterDesc` text,
  `monsterHP` numeric,
  `monsterATK` numeric,
  `monsterDEF` numeric,
  `monsterEXPReward` numeric
);

CREATE TABLE `cutscene` (
  `cutsceneID` varchar(16) PRIMARY KEY,
  `cutsceneName` text
);

CREATE TABLE `character_dialog` (
  `dialogID` varchar(16) PRIMARY KEY,
  `cutsceneID` varchar(16),
  `characterID` varchar(16),
  `order` int,
  `dialog` text
);

CREATE TABLE `monster_dialog` (
  `dialogID` varchar(16) PRIMARY KEY,
  `cutsceneID` varchar(16),
  `monsterID` varchar(32),
  `order` int,
  `dialog` text
);

CREATE TABLE `quest_prereqs_item` (
  `questID` varchar(32),
  `itemID` varchar(16),
  PRIMARY KEY (`questID`, `itemID`)
);

CREATE TABLE `quest_prereqs_dungeon` (
  `questID` varchar(32),
  `dungeonPreReqsID` varchar(32),
  PRIMARY KEY (`questID`, `dungeonPreReqsID`)
);

CREATE TABLE `quest_prereqs_quest` (
  `questID` varchar(32),
  `questPreReqsID` varchar(32),
  PRIMARY KEY (`questID`, `questPreReqsID`)
);

CREATE TABLE `quest_reward_item` (
  `questID` varchar(32),
  `itemID` varchar(16),
  `chance` numeric,
  PRIMARY KEY (`questID`, `itemID`)
);

CREATE TABLE `player_character` (
  `playerID` varchar(50),
  `charID` varchar(16),
  `charEXP` numeric,
  PRIMARY KEY (`playerID`, `charID`)
);

CREATE TABLE `player_quest` (
  `playerID` varchar(50),
  `questID` varchar(32),
  PRIMARY KEY (`playerID`, `questID`)
);

CREATE TABLE `playerInventory` (
  `playerID` varchar(50),
  `itemID` varchar(16),
  `amount` int,
  PRIMARY KEY (`playerID`, `itemID`)
);

CREATE TABLE `dungeon_quest_prereqs` (
  `dungeonID` varchar(32),
  `questPreReqsID` varchar(32),
  PRIMARY KEY (`dungeonID`, `questPreReqsID`)
);

CREATE TABLE `dungeon_item_reward` (
  `dungeonID` varchar(32),
  `itemID` varchar(16),
  `chance` numeric,
  PRIMARY KEY (`dungeonID`, `itemID`)
);

CREATE TABLE `dungeon_monster` (
  `dungeonID` varchar(32),
  `monsterID` varchar(32),
  `chanceSpawn` numeric,
  PRIMARY KEY (`dungeonID`, `monsterID`)
);

CREATE TABLE `charClass` (
  `charClassID` varchar(16) PRIMARY KEY,
  `charClassName` text,
  `charClassDesc` text
);

CREATE TABLE `itemClass` (
  `itemClassID` varchar(16) PRIMARY KEY,
  `itemClassName` text,
  `itemClassDesc` text
);

CREATE TABLE `itemType` (
  `itemTypeID` varchar(16) PRIMARY KEY,
  `itemTypeName` text,
  `itemTypeDesc` text
);

CREATE TABLE `level` (
  `level` int PRIMARY KEY,
  `exp_requirements` numeric
);

CREATE TABLE `player_rank` (
  `rank_name` varchar(50) PRIMARY KEY,
  `rank_order` int,
  `rank_division_count` int,
  `score_requirements_per_div` int
);

CREATE TABLE transactions (
  transaction_id varchar(64) PRIMARY KEY NOT NULL,
  player_id varchar(50) NOT NULL,
  item_id varchar(16),
  character_id varchar(16),
  used boolean NOT NULL
)

-- ALTER TABLE `player` ADD FOREIGN KEY (`guildID`) REFERENCES `guild` (`guildID`);

-- ALTER TABLE `character_dialog` ADD FOREIGN KEY (`cutsceneID`) REFERENCES `cutscene` (`cutsceneID`);

-- ALTER TABLE `character_dialog` ADD FOREIGN KEY (`characterID`) REFERENCES `character` (`charID`);

-- ALTER TABLE `monster_dialog` ADD FOREIGN KEY (`cutsceneID`) REFERENCES `cutscene` (`cutsceneID`);

-- ALTER TABLE `monster_dialog` ADD FOREIGN KEY (`monsterID`) REFERENCES `monster` (`monsterID`);

-- ALTER TABLE `quest_prereqs_item` ADD FOREIGN KEY (`questID`) REFERENCES `quest` (`questID`);

-- ALTER TABLE `quest_prereqs_item` ADD FOREIGN KEY (`itemID`) REFERENCES `item` (`itemID`);

-- ALTER TABLE `quest_prereqs_dungeon` ADD FOREIGN KEY (`questID`) REFERENCES `quest` (`questID`);

-- ALTER TABLE `quest_prereqs_dungeon` ADD FOREIGN KEY (`dungeonPreReqsID`) REFERENCES `dungeon` (`dungeonID`);

-- ALTER TABLE `quest_prereqs_quest` ADD FOREIGN KEY (`questID`) REFERENCES `quest` (`questID`);

-- ALTER TABLE `quest_prereqs_quest` ADD FOREIGN KEY (`questPreReqsID`) REFERENCES `quest` (`questID`);

-- ALTER TABLE `quest_reward_item` ADD FOREIGN KEY (`questID`) REFERENCES `quest` (`questID`);

-- ALTER TABLE `quest_reward_item` ADD FOREIGN KEY (`itemID`) REFERENCES `item` (`itemID`);

-- ALTER TABLE `player_character` ADD FOREIGN KEY (`playerID`) REFERENCES `player` (`playerID`);

-- ALTER TABLE `player_character` ADD FOREIGN KEY (`charID`) REFERENCES `character` (`charID`);

-- ALTER TABLE `player_quest` ADD FOREIGN KEY (`playerID`) REFERENCES `player` (`playerID`);

-- ALTER TABLE `player_quest` ADD FOREIGN KEY (`questID`) REFERENCES `quest` (`questID`);

-- ALTER TABLE `playerInventory` ADD FOREIGN KEY (`playerID`) REFERENCES `player` (`playerID`);

-- ALTER TABLE `playerInventory` ADD FOREIGN KEY (`itemID`) REFERENCES `item` (`itemID`);

-- ALTER TABLE `dungeon_quest_prereqs` ADD FOREIGN KEY (`dungeonID`) REFERENCES `dungeon` (`dungeonID`);

-- ALTER TABLE `dungeon_quest_prereqs` ADD FOREIGN KEY (`questPreReqsID`) REFERENCES `quest` (`questID`);

-- ALTER TABLE `dungeon_item_reward` ADD FOREIGN KEY (`dungeonID`) REFERENCES `dungeon` (`dungeonID`);

-- ALTER TABLE `dungeon_item_reward` ADD FOREIGN KEY (`itemID`) REFERENCES `item` (`itemID`);

-- ALTER TABLE `dungeon_monster` ADD FOREIGN KEY (`dungeonID`) REFERENCES `dungeon` (`dungeonID`);

-- ALTER TABLE `dungeon_monster` ADD FOREIGN KEY (`monsterID`) REFERENCES `monster` (`monsterID`);

-- ALTER TABLE `character` ADD FOREIGN KEY (`charClassID`) REFERENCES `charClass` (`charClassID`);

-- ALTER TABLE `item` ADD FOREIGN KEY (`itemClassID`) REFERENCES `itemClass` (`itemClassID`);

-- ALTER TABLE `item` ADD FOREIGN KEY (`itemTypeID`) REFERENCES `itemType` (`itemTypeID`);
