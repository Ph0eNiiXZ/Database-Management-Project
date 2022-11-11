select player_character.playerID, player.username, 
player_character.charID, character.charName, player_character.charEXP,
character.charHP, character.charATK, character.charDEF, charClass.charClassName
from player_character join player on player_character.playerID = player.playerID
join character on player_character.charID = character.charID
join charClass on character.charClassID = charClass.charClassID
where player.username = "Echo";
