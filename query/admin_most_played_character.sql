SELECT x.charID, MAX(x.cnt) FROM (SELECT charID, count(playerID) as cnt FROM player_character group by charID) x;
