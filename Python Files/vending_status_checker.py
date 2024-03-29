import json

class InventoryItem:
    def __init__( self, itemName ):
        # The name of the beverage, we work under the assumption there will only be one InventoryItem
        # for each named beverage
        self.name = itemName
        # The total number of this beverage item that were stocked last time we stocked the machines
        self.totalStocked = 0
        # The total number of this beverage item still left in the vending machines
        self.totalInStock = 0
        # The total number of slots that have this beverage
        self.totalSlots = 0
        
    def addToStocked( self, stockAmt ):
        self.totalStocked = self.totalStocked + stockAmt
        
    def addToInStock( self, inStockAmt ):
        self.totalInStock = self.totalInStock + inStockAmt
        
    def incrementSlots( self ):
        self.totalSlots = self.totalSlots + 1

    def getNumberSold( self ):
        return self.totalStocked - self.totalInStock
    
    def getSoldPct( self ):
        return self.getNumberSold() / self.totalStocked
    
    # We have an assumption here that the total number beverages that can be stocked
    # in a slot is 8 beverages.
    def getStockNeed( self ):
        return 8 * self.totalSlots - self.totalInStock
    
    def getName( self ):
        return self.name

    def getNumberInStock( self ):
        return self.totalInStock

    def __repr__( self ):
        return '{} In Stock: {}, Stocked: {}, Slots: {}'.format( self.name, self.totalInStock, self.totalStocked, self.totalSlots )

def main():
    inventoryFileNames = ["REID_1F_20171004.json", "REID_2F_20171004.json", "REID_3F_20171004.json"]
    
    # This dictionary maps from the name of a beverage to the InventoryItem object that represents
    # how much of that beverage is currently stocked in the vending machines, how much was stocked
    # last time, and how many vending machines slots the beverage is present in.
    itemNameToInventoryItem = {}
    
    # For each inventory file we have
    for inventoryFileName in inventoryFileNames: 
        inventoryFile = open( inventoryFileName, 'r' )
        
        # Read the JSON data into a Dictionary
        inventoryData = json.loads( inventoryFile.read() )
         
        contents = inventoryData['contents']
        
        # For each row of beverages in the vending machine
        for row in contents:
            
            # Each slot of beverages in the row of beverages
            for slot in row['slots']:
                itemName = slot['item_name']
                # Get the InventoryItem for this beverage using its name as the key into the dictionary
                # The InventoryItem object is used for accumulating our total stock counts of this beverage.
                # The get method returns a new InventoryItem with this beverage's name if we do not already
                # have one.
                inventoryItem = itemNameToInventoryItem.get( itemName, InventoryItem( itemName ) )
                
                # Update the propertiesof this InventoryItem, adding in how many beverages were stocked in
                # this slot and how many are currently still stocked in this slot
                inventoryItem.addToStocked( slot['last_stock'] )
                inventoryItem.addToInStock( slot['current_stock'] )
                inventoryItem.incrementSlots();
                
                # Store this InventoryItem object in the dictionary in case this was the first time we
                # encountered this beverage and an InventoryItem object is not already in the dictionary
                itemNameToInventoryItem[itemName] = inventoryItem

    # We've completed stock counting, now the user will decide how the data should be reported
    sortChoice = ''
    # Create a list of all the InventoryItem object we have so that later we can use the
    # sort method to order the items in the list as the user requests
    inventoryItemsList = list( itemNameToInventoryItem.values() )
    
    while sortChoice != 'q':
        sortChoice = input('Sort by (n)ame, (p)ct sold, (s)tocking need, or (q) to quit: ')
        
        # Use the user's choice to decide how the list should be sorted
        if sortChoice == 'n':
            inventoryItemsList.sort( key=InventoryItem.getName )
        elif sortChoice == 'p':
            inventoryItemsList.sort( key=InventoryItem.getSoldPct )
            inventoryItemsList.reverse()
        elif sortChoice == 's':
            inventoryItemsList.sort( key=InventoryItem.getStockNeed )
            inventoryItemsList.reverse()
        
        # Output the list in the requested sorted order
        print( 'Item Name            Sold     % Sold     In Stock Stock needs')
        for item in inventoryItemsList:
            print( '{:20} {:8} {:8.2f}% {:8} {:8}'.format( item.getName(), item.getNumberSold(), item.getSoldPct() * 100, item.getNumberInStock(), item.getStockNeed()))
        print()
    
main()
