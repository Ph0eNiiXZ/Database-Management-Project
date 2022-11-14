SELECT charClass.charClassID, charClass.charClassName, count(charClass.charClassID)
FROM player_character JOIN character ON player_character.charID = character.charID
JOIN charClass on character.charClassID = charClass.charClassID
GROUP BY charClass.charClassID
