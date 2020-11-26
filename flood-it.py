# Imports
from guizero import App, Waffle, Text, PushButton, info
import random

# Variables

colours = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]
palette_size = len(colours)
board_size = 14
moves_limit = 40 #at 40, 1w,3m_l
moves_taken = 0
game_over = False

# Functions
# Recursively floods adjacent squares
def flood(x, y, target, replacement):
    # Algorithm from https://en.wikipedia.org/wiki/Flood_fill
    if target == replacement:
        return False
    if board.get_pixel(x, y) != target:
        return False
    board.set_pixel(x, y, replacement)
    if y+1 <= board_size-1:   # South
        flood(x, y+1, target, replacement)
    if y-1 >= 0:            # North
        flood(x, y-1, target, replacement)
    if x+1 <= board_size-1:    # East
        flood(x+1, y, target, replacement)
    if x-1 >= 0:            # West
        flood(x-1, y, target, replacement)

# Check whether all squares are the same
def all_squares_are_the_same():
    squares = board.get_all()
    if all(colour == squares[0] for colour in squares):
        return True
    else:
        return False
 
 #fill board with color
def fill_board():
    #This is the simple, beginner way to loop through each x and y
    #for x in range(board_size):
        #for y in range(board_size):
            #board.set_pixel(x, y, random.choice(colours))
    #This solution uses an advanced feature called list comprehension 
    [board.set_pixel(x, y, random.choice(colours)) for y in range(board_size) for x in range(board_size)]

#assign colors to palette
def init_palette():
    for colour in colours:
        palette.set_pixel(colours.index(colour), 0, colour)
        
#flood board based on users choice of palette
def start_flood(x, y):
    flood_colour = palette.get_pixel(x, y)   #saves name of color chosen
    target = board.get_pixel(0,0) #where to start
    flood(0, 0, target, flood_colour) #call the flood function with parameters
    win_check()
    
def win_check():
    global moves_taken
    global moves_limit
    global game_over
    
    moves_taken += 1
    moves_left = moves_limit - moves_taken
    moves_text.value = str(moves_left) + " moves left"
    
    if moves_taken < moves_limit:
        if all_squares_are_the_same():
            win_text.value = "Winner Winner!"
            game_over = True
    else:
        win_text.value = "You lost :("
        game_over = True
        
    if game_over:
        palette.disable()
        reset_button.visible = True
        
    
#instructions
def how_to():
    if instruct_text.visible == False:
        instruct_text.visible = True
    else:
        instruct_text.visible = False
        
#Reset the game
def reset_game():
    global moves_taken
    global game_over
    game_over = False
    moves_taken = 0
    fill_board()
    palette.enable()
    win_text.value = ""
    moves_text.value = str(moves_limit) + " moves left"
    reset_button.visible = False
    
# ------------------------------
# App
app = App("Flood it")
board = Waffle(app, width = board_size, height = board_size, pad = 0)
palette = Waffle(app, width=palette_size, height=1, dotty=True, command=start_flood)
moves_text = Text(app, text = str(moves_limit) + " moves left")
win_text = Text(app)
instruct_button = PushButton(app, text="Help", command=how_to)
instruct_text = Text(app, text = """Starting from the top left square,
Pick a color on the palette to change the color of the square.
Match with neighboring squares to create a chain.
Fill the board before the moves limit to win! Good Luck!""", visible = False)
reset_button = PushButton(app, text = "Reset", command=reset_game, visible = False)

fill_board()
init_palette()

app.display()
# ------------------------------