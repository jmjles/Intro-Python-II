from room import Room
from player import Player
from item import Item
# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

# Add Items to Game
items = {
    'torch': Item('Torch', "As simple as it is, it allows you to walk in the dark."),
    'stick': Item('Stick', "The only thing that can protect you, not very comforting is it?"),
    'sword': Item('Sword', "A Metal sword, far better than a stick."),
    'bone': Item("Bone", 'A human femur bone, a good sign to be wary'),
}

# Add items to Rooms
room['narrow'].items.append(items['bone'])
room['treasure'].items.append(items['sword'])
#
# Main
#

# Make a new player object that is currently in the 'outside' room.
player1 = Player('JmFatal', room['outside'])
player1.inventory = [items['torch'], items['stick']]

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
command = ' '


def possibleCommands(room):
    acceptableCommands = ['q','i','m']
    if room.n_to != None:
        acceptableCommands.append('n')
    if room.s_to != None:
        acceptableCommands.append('s')
    if room.e_to != None:
        acceptableCommands.append('e')
    if room.w_to != None:
        acceptableCommands.append('w')
    if len(room.items) > 0:
        acceptableCommands.append('grab')
    if len(player1.inventory) > 0:
        acceptableCommands.append('drop')
    return acceptableCommands


def filterCommand(command, room):
    acceptableCommands = possibleCommands(room)
    for aCommand in acceptableCommands:
        if aCommand == command:
            global valid
            valid = True
    if valid == False:
        print('Please enter a valid command')
        print(f'Commands: {acceptableCommands}')


while command[0] != 'q':
    print(f'\nCurrent Location: {player1.current_room.name}')
    print(f'Direction: \n{player1.current_room.description}\n')
    print(f'\nAvailable Commands: {possibleCommands(player1.current_room)}')
    command = input("Awaiting your command:").lower().split(' ')
    print('----------')
    valid = False
    
    filterCommand(command[0], player1.current_room)
    if valid:
        movementComands = ('n','s','e','w')
        if command[0] in movementComands:
            player1.current_room = getattr(player1.current_room, f'{command[0]}_to')
        if command[0] == 'i':
            print('My Inventory:')
            for item in player1.inventory:
                print(item.name)
                print(f'Description: {item.description}')
        if command[0] == 'm':
            print('Items On The Floor:')
            for item in player1.current_room.items:
                print(item.name)
                print(f'Description: {item.description}')
        if command[0] == 'drop':
            if len(command) != 2:
                print("The correct usage: drop [ITEM]")
            else:
                itemFound = False
                for item in player1.inventory:
                    if item.name.lower() == command[1]:
                        player1.inventory.remove(item)
                        player1.current_room.items.append(item)
                        print(f'You dropped the {command[1].title()}.')
                        itemFound = True
                if itemFound == False:
                    print("You don't have that item.")
        if command[0] == 'grab':
            if len(command) != 2:
                print("The correct usage: grab [ITEM]")
            else:
                itemFound = False
                for item in player1.current_room.items:
                    if item.name.lower() == command[1]:
                        player1.inventory.append(item)
                        player1.current_room.items.remove(item)
                        print(f'You took the {command[1].title()}.')
                        itemFound = True
                if itemFound == False:
                    print(f"There is no {command[1].title()} in the room.")
            
            
