select playerInventory.playerID, player.username, 
playerInventory.itemID, item.itemName, item.itemDescription, 
itemClass.itemClassName, playerInventory.amount
from playerInventory join player on playerInventory.playerID = player.playerID
join item on playerInventory.itemID = item.itemID
join itemClass on item.itemClassID = itemClass.itemClassID
WHERE player.username = "Ian"
