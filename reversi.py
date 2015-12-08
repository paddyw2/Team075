"""
CPSC 231, December 2015 - Team 7 Reversi
Team Members: Yang Li, Chi Nguyen, Patrick Withams, Greg Young

Summary: This program creates a Reversi game using Turtle Graphics

Sources: http://www.samsoft.org.uk/reversi/strategy.htm - The position value
strategy for AI2() and AI3() were inspired by this website.

pcb.gif - http://images8.alphacoders.com/403/403441.gif
mudcracks.gif - http://math.marywood.edu/~tfkent/research/fractal_soil/crack_2_19%20-%20photo.gif
dirt.gif - https://bethmorleyblog.files.wordpress.com/2014/11/dirt-tiled-2.gif
fractal - http://farm3.static.flickr.com/2757/4521273677_b9a7df50c7_o.gif

Description: Reversi is a two player game that is played using an 8x8 board.
Each player starts with two alternating centred pieces and the aim of the game
is to have the most of pieces on the board. Each player takes a turn and can
place their piece anywhere on the board so that a straight or diagonal line from
one of their original pieces to their placed piece is created with only the
opponent pieces in the centre, essentially surrounding the opponent pieces. Once
the move is made, the surrouded opponent pieces will be changed to the player's
colour, and the next player will then go. If any player has no possible moves at
any time, they simply skip their go. The game ends when both player's cannot
take any more turns, and the winner is the player with the most pieces.

The program starts by welcoming the user, and asking them to choose to either
start a new game, or load a previous game. They are then asked to choose the
difficulty level for the game. The starting pieces are loaded, and a popup
window indicates which colour the human player has been assigned, and which
player goes first. Throughout the game each player's turn is indicated by a
line drawn under each scoreboard on either side of the screen. These also keep
track on the number of pieces each player has.

There are six buttons below the game board - their purpose is as follows:

Rules: This triggers a popup window that describes the rules of the game to the
user.
New Game: This clears the current game, and sets up a new one, choosing the
player colour at random again, and prompting the user for difficulty.
Save: This allows the user to save their current game state by entering a name.
If the name is used by another game, the user is asked to confirm before they
overwrite the old game.
Hints On/Off: This toggles the hints markers which show the possible moves for
the human player.
Load Game: This allows the player to load a previous game at any point.
Exit: This terminates the program.

Difficulty Settings:

There are three different settings that the computer uses: AI1, AI2, and AI3.

AI1 is commonly known as the 'greedy' method and simply chooses the move that
captures the most pieces. If there are two or more pieces that capture the same
number of pieces, a random choice is made between them.

AI2 uses a mixture of the 'greedy' method and a positional value method. It
notes that the corner moves are always the most favourable (see samsoft source)
and that the second from corner moves (i.e. 1,1 or 6,6) are the least favourable.
It then looks through the possible moves, and if there are any corner moves it
chooses them. If there are more than one, it passes the list to AI1 to find out
which takes the most pieces. If there are no corner moves, it then looks through
the possible moves again to see if there are any other moves, other than the second
from corner moves (i.e. 6,6). If there are, it creates a list and if there is
more than one it passes this list to AI1 to decide which move takes the most
pieces. If there is just one move, it simply chooses that move. Lastly, if there
are no other options, it chooses one of the second from corner moves.

AI3 also uses a mixture of 'greedy' and positional value methods, but only uses
the AI1 function if there are more than one moves of same positional value. It
is far more strict on its adherenece to the positional value method. It
notes that each move on the board has a positional value, and always tries to
play a move with the highest value possible. Corner moves are the most valuable,
and so it searches the possible moves for one of those. If none are found, it
moves onto the next value of moves, and searches for one of those instead. If
there are more than one move of the same value, it sends a list of these values
to AI1 to determine which move takes the most pieces.

"""

import copy
import os
import time
import turtle as tt
from sys import exit
from random import randrange

# global constants
PIECE_SIZE  = 50
ROWS = 8
BOARD_SIZE = PIECE_SIZE * ROWS

BOARD_TOP_LEFT_X = - (BOARD_SIZE / 2)
BOARD_TOP_LEFT_Y =  BOARD_SIZE / 2

FONTSIZE = int(PIECE_SIZE/4)
FONTSIZE_SMALL = FONTSIZE - 4
FONTSIZE_LARGE = FONTSIZE + 4
FONTSIZE_XLARGE = FONTSIZE * 3

BOARD_COLOUR = '#228B22'
BORDER_COLOUR = '#AAA'
HINTS_COLOUR = 'orange'
COMP_FIRST_FLIP = 'orange'

COLOR1 = 'black'
COLOR2 = 'white'

# Turtle screen
wn = tt.Screen()
wn.setup(startx=None,starty=None)

# setting random background picture of Turtle screen or green if images aren't
# available
try:
    bgdir = os.path.join(os.getcwd(),'img')
    bglst = os.listdir(bgdir)
    randnum = randrange(0,len(bglst))
    bgpic = os.path.join(bgdir,bglst[randnum])
    wn.bgpic(bgpic)
except:
    wn.bgcolor("green")

wn.title('R E V E R S I')
wn.tracer(0)

# Turtles
setup = tt.Turtle()
setup.ht()
setup.pu()

piece = tt.Turtle()
piece.ht()
piece.pu()

hint = tt.Turtle()
hint.ht()
hint.pu()

scoreBg = tt.Turtle()
scoreBg.ht()
scoreBg.pu()

color1score = tt.Turtle()
color1score.ht()
color1score.pu()
color1score.color(COLOR1)

color2score = tt.Turtle()
color2score.ht()
color2score.pu()
color2score.color(COLOR2)

popup = tt.Turtle()
popup.ht()
popup.pu()

turnturt = tt.Turtle()
turnturt.pensize(3)
turnturt.ht()
turnturt.pu()

# global variables

difficultySetting = 0
hintsEnabled = False
userColor = ''
playerTurn = COLOR1
# a blank gameboard
origGameState = [['O','O','O','O','O','O','O','O'],
                 ['O','O','O','O','O','O','O','O'],
                 ['O','O','O','O','O','O','O','O'],
                 ['O','O','O','O','O','O','O','O'],
                 ['O','O','O','O','O','O','O','O'],
                 ['O','O','O','O','O','O','O','O'],
                 ['O','O','O','O','O','O','O','O'],
                 ['O','O','O','O','O','O','O','O']]
activePopup = False
gameHasEnded = False
moveInProgress = False
# gameboard used for game being played, a copy of a blank state for new games
gameState = copy.deepcopy(origGameState)
# list of directions for traversing the gameboard
dirList = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]

# game functions

def setupGameboard():
    '''Sets up the gameboard by drawing the grid and surrounding items'''
    boardBottomLeftY = ( - BOARD_TOP_LEFT_Y)
    setup.goto(BOARD_TOP_LEFT_X, boardBottomLeftY)
    drawQuad(BOARD_SIZE, BOARD_SIZE,BOARD_COLOUR,setup)
    drawScoreBg(scoreBg)
    drawGrid(setup)
    writeTitle(setup)
    drawButtons(setup)

def drawScoreBg(turt):
    ''' Draws backround and border for score trackers.

    Arguments:
    turt (turtle object) -- allows for a choice of turtle
    '''
    scoreBoardLeftX = BOARD_TOP_LEFT_X - PIECE_SIZE
    scoreBoardLeftY = BOARD_TOP_LEFT_Y - (PIECE_SIZE * 2)
    scoreBoardRightX = - BOARD_TOP_LEFT_X + PIECE_SIZE
    scoreBoardRightY = BOARD_TOP_LEFT_Y - (PIECE_SIZE * 2)

    # background
    turt.goto(scoreBoardLeftX - (PIECE_SIZE/2), scoreBoardLeftY - (PIECE_SIZE/4))
    drawQuad(PIECE_SIZE, PIECE_SIZE,BOARD_COLOUR,turt)
    turt.color(BORDER_COLOUR)
    turt.pd()
    # grey border
    for i in range(4):
        turt.fd(PIECE_SIZE)
        turt.lt(90)
    turt.pu()
    # background
    turt.goto(scoreBoardRightX - (PIECE_SIZE/2), scoreBoardRightY - (PIECE_SIZE/4))
    drawQuad(PIECE_SIZE, PIECE_SIZE,BOARD_COLOUR,turt)
    # grey border
    turt.color(BORDER_COLOUR)
    turt.pd()
    for i in range(4):
        turt.fd(PIECE_SIZE)
        turt.lt(90)
    turt.pu()


def drawQuad(width,height,color,turt,depth=False):
    '''Draws filled quadrilaterals with given Turtle.

    Arguments:
    width (int) -- the left to right size
    height (int) -- the top to bottom size
    color (str) -- the fill color
    turt (Turtle) -- the Turtle that is used to draw quadrilateral
    depth (bool) -- if True, will give the look of a 3D box (default False)
    '''
    if depth == False:
        turt.pd()
        turt.color(color)
        turt.begin_fill()
        for i in range(2):
            turt.fd(height)
            turt.lt(90)
            turt.fd(width)
            turt.lt(90)
        turt.end_fill()
        turt.pu()
    else:
        # used for 'buttons'
        turt.pd()
        turt.color('black', color)
        turt.begin_fill()
        turt.pensize(1)
        turt.fd(height)
        turt.lt(90)
        turt.pensize(3)
        turt.fd(width)
        turt.lt(90)
        turt.pensize(3)
        turt.fd(height)
        turt.lt(90)
        turt.pensize(1)
        turt.fd(width)
        turt.lt(90)
        turt.end_fill()
        turt.pu()

def drawGrid(turt):
    '''Draws the playing grid on the game board.

    Argument:
    turt (Turtle)-- the Turtle used to draw the grid
    '''
    boardTopRightX = BOARD_TOP_LEFT_X + BOARD_SIZE
    boardBottomRightY = (-BOARD_TOP_LEFT_Y)
    turt.color(BORDER_COLOUR)
    drawLines(turt)
    turt.goto(boardTopRightX, boardBottomRightY)
    turt.lt(90)
    drawLines(turt)

def drawLines(turt):
    '''Draws the lines for the playing grid.

    Argument:
    turt (Turtle) -- the Turtle used to draw the lines
    '''
    for i in range(9):
        turt.pd()
        turt.fd(BOARD_SIZE)
        turt.pu()
        turt.fd(-BOARD_SIZE)
        turt.lt(90)
        turt.fd(PIECE_SIZE)
        turt.lt(-90)

def writeTitle(turt):
    '''Write 'REVERSI' with drop shadow above grid'''
    boardCenter = 0
    boardTitleArea = (BOARD_SIZE / 2) + (PIECE_SIZE / 2)

    turt.goto(boardCenter, boardTitleArea)
    turt.color('black')
    turt.pd()
    turt.write('*  R  E  V  E  R  S  I *', align='center',
    font=('',FONTSIZE_XLARGE,'bold'))
    turt.pu()
    turt.goto(boardCenter - 2, boardTitleArea + 2)
    turt.color('white')
    turt.pd()
    turt.write('*  R  E  V  E  R  S  I *', align='center',
    font=('',FONTSIZE_XLARGE,'bold'))
    turt.pu()

def drawButtons(turt):
    '''Draws "buttons" on the game screen to demarcate areas for the user to
    click to either exit the game or save it.

    Argument:
    turt (Turtle) -- the Turtle used to draw the buttons
    '''

    buttonWidth = PIECE_SIZE * 2
    buttonHeight = PIECE_SIZE / 2

    button1StartPosX = BOARD_TOP_LEFT_X
    button1StartPosY = (- BOARD_SIZE / 2) - (PIECE_SIZE / 3)

    button2StartPosX = button1StartPosX + (PIECE_SIZE * 3)
    button2StartPosY = button1StartPosY

    button3StartPosX = button1StartPosX + (PIECE_SIZE * 6)
    button3StartPosY = button1StartPosY

    button4StartPosX = button1StartPosX + (PIECE_SIZE * 3)
    button4StartPosY = (button1StartPosY - (PIECE_SIZE / 1.5))

    button5StartPosX = BOARD_TOP_LEFT_X
    button5StartPosY = (button1StartPosY - (PIECE_SIZE / 1.5))

    button6StartPosX = button1StartPosX + (PIECE_SIZE * 6)
    button6StartPosY = (button1StartPosY - (PIECE_SIZE / 1.5))

    drawIndividualButtons(button1StartPosX, button1StartPosY, turt, 'RULES')
    drawIndividualButtons(button2StartPosX, button2StartPosY, turt, 'SAVE')
    drawIndividualButtons(button3StartPosX, button3StartPosY, turt, 'EXIT')
    drawIndividualButtons(button4StartPosX, button4StartPosY, turt, 'HINTS ON/OFF')
    drawIndividualButtons(button5StartPosX, button5StartPosY, turt, 'NEW GAME')
    drawIndividualButtons(button6StartPosX, button6StartPosY, turt, 'LOAD GAME')

def drawIndividualButtons(startX, startY, turt, text):
    ''' Draws individual buttons below game board.

    Arguments:
    startX (int) -- starting x coordinate for drawing
    startY (int) -- starting y coordinate for drawing
    turt (turtle object) -- the choice of turtle
    message (str) -- the text for the button
    '''
    buttonWidth = PIECE_SIZE * 2
    buttonHeight = PIECE_SIZE / 2
    turt.goto(startX, startY)
    turt.seth(270)
    drawQuad(buttonWidth, buttonHeight,'white',turt,True)
    turt.goto(startX + PIECE_SIZE, startY - PIECE_SIZE / 2.5)
    turt.write(text,align='center',font=('',FONTSIZE_SMALL))

def drawHint(col, row, color):
    ''' Draws possible moves for the player, make possible moves easier to
    observe. The hint turtle starts in the centre of the position and stamps
    a circle.

    Arguments:
    col (int) -- column coordinate
    row (int) -- row coordinate
    colour (str) -- the colour to draw the circle with
    '''
    xCoord = (col * PIECE_SIZE) + BOARD_TOP_LEFT_X
    yCoord = (row * PIECE_SIZE) + BOARD_TOP_LEFT_X
    # as stamps centre around a coordinate, rather starting from
    # the corner like filling squares, the centre of each position
    # is calculated below. This is slightly different to the
    # drawPiece function.
    hint.goto(xCoord+(PIECE_SIZE/2),yCoord+(PIECE_SIZE/2))
    hint.color(color)
    hint.shape("circle")
    hint.stamp()

def openingWindow():
    '''Input window where the user chooses an option from a list using
    numeric input. Can start a new game or load a saved game. If the Cancel
    button is pressed the game exits, otherwise it returns the integer value of
    the input.
    '''
    userIn = wn.numinput('Welcome','WELCOME TO REVERSI!\n\nChoose an option or'
                        ' Cancel to quit.\n\n1) New Game\n2) Load Game\n',1,1,2)
    if userIn == None:
        exit()
    else:
        return int(userIn)

def changeDifficulty(popup=True):
    '''Change difficultySetting.

    Arguments:
    popup (bool) -- optional parameter that indicates whether or not a popup
    input box is triggered. If True, or not provided, the user can change the
    difficulty. If not, the title is updated to reflect the current level only.
    '''
    global difficultySetting
    global wn
    if popup:
        difflist = ["Easy", "Medium", "Hard"]
        userIn = wn.numinput('Choose Difficulty','Current difficulty setting: '+
                             difflist[difficultySetting]+'\n\nChoose an option:'
                             '\n\n1) Easy\n2) Medium\n3) Hard',1,1,3)
        if userIn != None:
            difficultySetting = int(userIn) - 1

    if difficultySetting == 2:
        wn.title('R E V E R S I - Difficulty Level: Hard')
    elif difficultySetting == 1:
        wn.title('R E V E R S I - Difficulty Level: Medium')
    else:
        wn.title('R E V E R S I - Difficulty Level: Easy')


def drawInitialPieces():
    '''Commands to draw the initial 4 pieces of a new game'''
    drawPiece(3,3,COLOR2)
    drawPiece(3,4,COLOR1)
    drawPiece(4,3,COLOR1)
    drawPiece(4,4,COLOR2)

def drawPiece(col,row,color):
    '''Draws the player's new piece and flipped pieces using the global Turtle
    name piece and updates the global variable gameState.

    Arguments:
    row (int) -- the row number of the gameboard grid (0-7)
    col (int)-- the column number of the gameboard grid (0-7)
    color (string) -- the color of the game piece to be drawn
    '''
    piece.pu()
    xCoord = (col * PIECE_SIZE) + BOARD_TOP_LEFT_X
    yCoord = (row * PIECE_SIZE) + BOARD_TOP_LEFT_X
    piece.goto(xCoord+2,yCoord+2)
    global gameState
    if color == COLOR1:
        gameState[row][col] = 'B'
    else:
        gameState[row][col] = 'W'
    drawQuad(PIECE_SIZE - 4,PIECE_SIZE - 4,color,piece)
    scorekeeper()

def loadGame():
    '''Produces a list of saved games from savedGames directory and the user
    uses numerical input to select the game to load. The savedGames directory
    must be in the same directory as this .py file.
    '''
    gamesList = []
    #Getting the path to the savedGames directory and appending saved games to
    # gamesList.
    try:
        cwd = os.getcwd()
        savedDir = os.path.join(cwd,'savedGames')
        for file_ in os.listdir(savedDir):
            if file_.endswith('.reversi'):
                gamesList.append(file_)
        # Bring up user input window and wait for numberical input that
        # corresponds to a game file.
        txt = ''
        for i in range(len(gamesList)):
            txt += ('\n' + str(i + 1) + ') ' +
            str(os.path.splitext(gamesList[i])[0]))
        userIn = (wn.numinput('Load Game','Enter the number of a saved game:' +
                 txt,1,1,len(gamesList)))
        while userIn == None:
            userIn = (wn.numinput('Load Game','You must enter the number of a saved game:' +
                      txt,1,1,len(gamesList)))
        userIn = int(userIn)
        # Opens the file selected by the user and reads the contents
        inFile = os.path.join(savedDir,gamesList[userIn-1])
        with open(inFile, 'r') as game:
            lines = game.readlines()
            newGameState = []
            for i in range(len(lines)):
                if i < ROWS:
                    row = list(lines[i].strip('\n'))
                    newGameState.append(row)
                elif i == ROWS:
                    colorLine = lines[i].strip()
                elif i == ROWS + 1:
                    diffLine = lines[i].strip()
                elif i == ROWS + 2:
                    hintsLine = lines[i].strip()
        # change global variables to reflect where the game was when user saved.
        loadGameDetails(colorLine, diffLine, hintsLine, lines, newGameState)
        # visually draw gamestate on board
        drawLoadedPieces()
    except:
        # for debugging
        print("Error. The savedGames directory may not exist, or there may be" +
        " no saved games to load, for example.")
        exit()

def loadGameDetails(colorLine, diffLine, hintsLine, lines, newGameState):
    '''Takes the details of a saved game, and updates the global game
    variables to load this previous game state.

    Arguments:
    colorLine (str) -- the line of the saved text file that represents the player
    colour.
    diffLine (str) -- the line of the text file that represents the difficulty
    setting
    hintsLine (str) -- the line of the text file that represents whether hints
    were enabled or not.
    lines (list) -- the contents of the text file, changed into a list of line
    strings.
    newGameState (list) -- the updated gamestate list
    '''
    global gameState, playerTurn, userColor, difficultySetting, hintsEnabled
    colorDict = {'COLOR1' : COLOR1, 'COLOR2' : COLOR2}
    playerTurn = colorDict[colorLine]
    userColor = colorDict[colorLine]
    gameState = newGameState
    # check that saved game has diff and hints info
    if len(lines) > ROWS + 1:
        difficultySetting = int(diffLine)
        # update window title with diff setting
        changeDifficulty(False)
        if hintsLine == "True":
            hintsEnabled = True
        else:
            hintsEnabled = False

def drawLoadedPieces():
    '''Uses gameState to draw all the pieces from the saved game.'''
    piece.clear()
    hint.clearstamps()
    for row in range(len(gameState)):
        for col in range(len(gameState[row])):
            if gameState[row][col] == 'B':
                drawPiece(col, row, COLOR1)
            elif gameState[row][col] == 'W':
                drawPiece(col, row, COLOR2)
    scorekeeper()

def turnIndicator():
    '''Draws a line under the score of the current player's turn.'''
    scoreBoardLeftX = BOARD_TOP_LEFT_X - PIECE_SIZE
    scoreBoardLeftY = BOARD_TOP_LEFT_Y - (PIECE_SIZE * 2)
    scoreBoardRightX = - BOARD_TOP_LEFT_X + PIECE_SIZE
    scoreBoardRightY = BOARD_TOP_LEFT_Y - (PIECE_SIZE * 2)

    if playerTurn == COLOR1:
        turnturt.clear()
        turnturt.color(COLOR1)
        turnturt.goto(scoreBoardLeftX - (PIECE_SIZE /4),scoreBoardLeftY)
        turnturt.pd()
        turnturt.fd(PIECE_SIZE/2)
        turnturt.pu()
    else:
        turnturt.clear()
        turnturt.color(COLOR2)
        turnturt.goto(scoreBoardRightX - (PIECE_SIZE/4),scoreBoardRightY)
        turnturt.pd()
        turnturt.fd(PIECE_SIZE/2)
        turnturt.pu()

def scorekeeper():
    '''Uses gameState to count the number of each player's pieces and displays
    the total beside the gameboard.
    '''
    scoreBoardLeftX = BOARD_TOP_LEFT_X - PIECE_SIZE
    scoreBoardLeftY = BOARD_TOP_LEFT_Y - (PIECE_SIZE * 2)
    scoreBoardRightX = - BOARD_TOP_LEFT_X + PIECE_SIZE
    scoreBoardRightY = BOARD_TOP_LEFT_Y - (PIECE_SIZE * 2)

    color1score.clear()
    color2score.clear()

    blkPc = 0
    whtPc = 0
    turnIndicator()
    for i in range(len(gameState)):
        for j in range(len(gameState[i])):
            if gameState[i][j] == 'B':
                blkPc += 1
            if gameState[i][j] == 'W':
                whtPc += 1
    color1score.goto(scoreBoardLeftX, scoreBoardLeftY)
    color1score.write(str(blkPc),align='center',font=('',FONTSIZE_LARGE,'bold'))
    color2score.goto(scoreBoardRightX, scoreBoardRightY)
    color2score.write(str(whtPc),align='center',font=('',FONTSIZE_LARGE,'bold'))

    return blkPc, whtPc

def chooseRandomColor():
    '''Randomly select 0 or 1 and returns the value of the color assigned to
    the user.
    '''
    headstails = randrange(0,2)
    if headstails == 1:
        color = COLOR1
    else:
        color = COLOR2
    return color

def newGameAlert():
    '''Draws popup to alert users of their color.'''
    global activePopup
    smallPopupStartX = BOARD_TOP_LEFT_X + (PIECE_SIZE / 2)
    smallPopupStartY = BOARD_TOP_LEFT_Y - (PIECE_SIZE * 2.5)
    smallPopupSizeX = PIECE_SIZE * 7
    smallPopupSizeY = PIECE_SIZE * 3

    activePopup = True
    popup.goto(smallPopupStartX, smallPopupStartY)
    popup.seth(270)
    drawQuad(smallPopupSizeX, smallPopupSizeY, '#333',popup)
    popup.color('white')
    popup.goto(smallPopupStartX + (smallPopupSizeX / 2), smallPopupStartY - (smallPopupSizeY / 2))
    text1 = '{0} player goes first, your color is {1}'.format(
            COLOR1.capitalize(),userColor.capitalize())
    popup.write(text1,align='center',font=('',FONTSIZE))
    popup.goto(smallPopupStartX + (smallPopupSizeX/2), smallPopupStartY - (PIECE_SIZE*2))
    text2 = 'Click to continue...'
    popup.write(text2,align='center',font=('',FONTSIZE))

def loadGameAlert():
    '''Draws popup to alert users of their color after loaded game.'''
    global activePopup
    smallPopupStartX = BOARD_TOP_LEFT_X + (PIECE_SIZE / 2)
    smallPopupStartY = BOARD_TOP_LEFT_Y - (PIECE_SIZE * 2.5)
    smallPopupSizeX = PIECE_SIZE * 7
    smallPopupSizeY = PIECE_SIZE * 3

    activePopup = True
    popup.goto(smallPopupStartX, smallPopupStartY)
    popup.seth(270)
    drawQuad(smallPopupSizeX, smallPopupSizeY,'#333',popup)
    popup.color('white')
    popup.goto(smallPopupStartX + (smallPopupSizeX / 2), smallPopupStartY - (smallPopupSizeY / 2))
    text1 = 'Your turn, your color is {0}'.format(userColor.capitalize())
    popup.write(text1,align='center',font=('',FONTSIZE))
    popup.goto(smallPopupStartX + (smallPopupSizeX/2), smallPopupStartY - (PIECE_SIZE*2))
    text2 = 'Click to continue...'
    popup.write(text2,align='center',font=('',FONTSIZE))

def userClickInput(x,y):
    '''Takes the input from a user click and depending the values executes the
    corresponding function.

    Arguments:
    x (float) -- x coordinate of where the user clicked
    y (float) -- y coordinate of where the user clicked
    '''
    global activePopup, gameHasEnded, moveInProgress

    buttonWidth = PIECE_SIZE * 2
    buttonHeight = PIECE_SIZE / 2

    button1StartPosX = BOARD_TOP_LEFT_X
    button1StartPosY = (- BOARD_SIZE / 2) - (PIECE_SIZE / 3)

    button2StartPosX = button1StartPosX + (PIECE_SIZE * 3)
    button2StartPosY = button1StartPosY

    button3StartPosX = button1StartPosX + (PIECE_SIZE * 6)
    button3StartPosY = button1StartPosY

    button4StartPosX = button1StartPosX + (PIECE_SIZE * 3)
    button4StartPosY = (button1StartPosY - (PIECE_SIZE / 1.5))

    button5StartPosX = BOARD_TOP_LEFT_X
    button5StartPosY = (button1StartPosY - (PIECE_SIZE / 1.5))

    button6StartPosX = button1StartPosX + (PIECE_SIZE * 6)
    button6StartPosY = (button1StartPosY - (PIECE_SIZE / 1.5))

    boardCoordLeft = BOARD_TOP_LEFT_X
    boardCoordRight = BOARD_TOP_LEFT_X + BOARD_SIZE

    if activePopup == True:
        popup.clear()
        activePopup = False
        if gameHasEnded:
            gameHasEnded = False
            newGame()
            hint.clearstamps()
    else:
        if ((boardCoordLeft <= x <= boardCoordRight) and
        (boardCoordLeft <= y <= boardCoordRight) and
        (not moveInProgress)):
            userMove(x,y)
        elif ((button1StartPosX <= x <= button1StartPosX + buttonWidth) and
        (button1StartPosY - buttonHeight <= y <=  button1StartPosY)):
            rules()
        elif ((button2StartPosX <= x <= button2StartPosX + buttonWidth) and
        (button2StartPosY - buttonHeight <= y <=  button2StartPosY)):
            saveGame()
        elif ((button3StartPosX <= x <= button3StartPosX + buttonWidth) and
        (button3StartPosY - buttonHeight <= y <=  button3StartPosY)):
            exit()
        elif ((button4StartPosX <= x <= button4StartPosX + buttonWidth) and
        (button4StartPosY - buttonHeight <= y <=  button4StartPosY)):
            toggleHints()
        elif ((button5StartPosX <= x <= button5StartPosX + buttonWidth) and
        (button5StartPosY - buttonHeight <= y <=  button5StartPosY)):
            hint.clearstamps()
            newGame("new")
        elif ((button6StartPosX <= x <= button6StartPosX + buttonWidth) and
        (button6StartPosY - buttonHeight <= y <=  button6StartPosY)):
            newGame("load")

def userMove(xCoord, yCoord):
    '''Performs the actions a user needs in order to make their move. First by
    finding the valid moves, checking if the clicked square is a valid move and
    if it is then finds the locations of the pieces to be 'flipped'. Then checks
    if the other player has valid moves to decide if it becomes the next
    player's turn.

    Arguments:
    xCoord (int) -- x value from input click
    yCoord (int) -- y value from input click
    userColor (str) -- the user's piece color
    '''
    global playerTurn, moveInProgress
    moveInProgress = True
    validList = getValidMoves()
    gridX = int(xCoord // PIECE_SIZE - 2)
    gridY= int(yCoord // PIECE_SIZE - 2)
    gridX = abs(gridX + 6)
    gridY = abs(gridY + 6)
    if [gridX,gridY] in validList:
        drawPiece(gridX,gridY,playerTurn)
        hint.clearstamps()
        flipList = []
        for dirX,dirY in dirList:
            flipList = toFlip(gridX,gridY,dirX,dirY,flipList)
            for col,row in flipList:
                drawPiece(col,row,userColor)
        playerTurn = playerSwap()
        validList = getValidMoves()
        if len(validList) == 0:
            playerTurn = playerSwap()
            validList = getValidMoves()
            if len(validList) == 0:
                moveInProgress = False
                endGame()
        else:
            moveInProgress = False
            computerMove()
    # to take into account invalid board clicks
    moveInProgress = False

def showHints(possibleMoves):
    '''If global hintsEnabled is set to True,
    all possible moves for the player are
    stamped on the game board.

    Arguments:
    possibleMoves (list) -- a list of the players possible moves
    '''
    if hintsEnabled:
        for move in possibleMoves:
            drawHint(move[0],move[1],HINTS_COLOUR)

def toggleHints():
    '''Changes the global hintsEnabled to boolean value
    opposite to its current value. If it is changed to
    True, the users moves will be drawn with showHints.
    If changed to False, the hint turtle is cleared.
    '''
    global hintsEnabled
    if hintsEnabled:
        hintsEnabled = False
        hint.clearstamps()
    else:
        hintsEnabled = True
        validMoves = getValidMoves()
        showHints(validMoves)


def getValidMoves():
    '''Finds the pieces for the current player and uses their coordinates and
    the find_moves function to search for legal moves. Returns a 2D list of
    row and column values.
    '''
    validMoves = []
    if playerTurn == COLOR1:
        playerValue = 'B'
    else:
        playerValue = 'W'
    for col in range(8):
        for row in range(8):
            if isValidMove(playerValue,col,row) == True:
                validMoves.append([col,row])
    return validMoves

def isValidMove(playerValue,col,row):
    '''Test each square on the board and tests that if the square was chosen
    whether or not any opponent's tiles would be flipped. Returns a boolean.

    Arguments:
    playerValue (str) -- the value of the current player in the gameState
    col (int) -- the column of the square being checked
    row (int) -- the row of the square being checked
    '''
    x = col
    y = row
    if playerValue == 'B':
        otherPlayer = 'W'
    else:
        otherPlayer = 'B'
    if gameState[y][x] != 'O':
        return False
    for dirX, dirY in dirList:
        x = col
        y = row
        x += dirX
        y += dirY
        if (0 <= x <= 7 and 0 <= y <= 7) and gameState[y][x] == otherPlayer:
            x += dirX
            y += dirY
            if not (0 <= x <= 7 and 0 <= y <= 7):
                continue
            while gameState[y][x] == otherPlayer:
                x += dirX
                y += dirY
                if not (0 <= x <= 7 and 0 <= y <= 7):
                    break
            if not (0 <= x <= 7 and 0 <= y <= 7):
                continue
            if gameState[y][x] == playerValue:
                return True
        else:
            continue
    return False

def toFlip(gridX,gridY,dirX,dirY,inList):
    '''Finds the opponents pieces to 'flip' after a valid move is chosen.

    Arguments:
    gridX (int) -- the column value from the grid
    gridY (int)-- the row value from the grid
    dirX (int) -- how far to move in the x direction
    dirY (int) -- how far to move in the y direction
    inList (list) -- the list of row and column values of pieces to 'flip'
    '''
    flipList = inList[:]
    if playerTurn == COLOR1:
        playerValue = 'B'
    elif playerTurn == COLOR2:
        playerValue = 'W'
    newX = gridX + dirX
    newY = gridY + dirY
    if not (0 <= newX <= 7 and 0 <= newY <= 7):
        flipList = []
        return flipList
    else:
        gameStateValue = gameState[newY][newX]
        if gameStateValue != playerValue and gameStateValue != 'O':
            flipList.append([newX,newY])
            flipList = toFlip(newX,newY,dirX,dirY,flipList)
            return flipList
        elif gameStateValue == playerValue:
            return flipList
        else:
            flipList = []
            return flipList

def playerSwap():
    '''Swaps the playerTurn global variable. Returns variable containing a
    string.
    '''
    if playerTurn == COLOR1:
        return COLOR2
    else:
        return COLOR1

def computerMove():
    '''Performs the functions allowing the AI to take its turn.'''
    global playerTurn, moveInProgress
    moveInProgress = True
    time.sleep(0.5)
    validList = getValidMoves()
    # choose AI based on diff setting
    if difficultySetting == 0:
        gridX,gridY = AI1(validList)
    elif difficultySetting == 1:
        gridX,gridY = AI2(validList)
    elif difficultySetting == 2:
        gridX,gridY = AI3(validList)
    drawPiece(gridX,gridY,COMP_FIRST_FLIP)
    time.sleep(1)
    drawPiece(gridX,gridY,playerTurn)
    flipList = []
    for dirX,dirY in dirList:
        flipList = toFlip(gridX,gridY,dirX,dirY,flipList)
        for col,row in flipList:
            drawPiece(col,row,playerTurn)
            hint.clearstamps()
    playerTurn = playerSwap()
    validList = getValidMoves()
    if len(validList) == 0:
        playerTurn = playerSwap()
        validList = getValidMoves()
        if len(validList) == 0:
            moveInProgress = False
            endGame()
        else:
            computerMove()
    else:
        turnIndicator()
        moveInProgress = False
        showHints(validList)

def AI1(inList):
    '''Calculates the optimal move for the AI in which its score increases the
    most. Returns the row and column values.

    Arguments:
    inList (list) -- the list of valid moves for the AI
    '''
    validList = inList[:]
    bestList = []
    totFlip = 0
    bestX = 0
    bestY = 0
    for gridX,gridY in validList:

        totalFlipList = []
        for dirX,dirY in dirList:
            flipList = []
            flipList = toFlip(gridX,gridY,dirX,dirY,flipList)
            totalFlipList += flipList
        if len(totalFlipList) > totFlip:
            totFlip = len(totalFlipList)
            bestList[:] = []
            bestList.append([gridX,gridY])
        elif len(totalFlipList) == totFlip:
            bestList.append([gridX,gridY])
    randIndex = randrange(0,len(bestList))
    bestMove = bestList[randIndex]
    return bestMove[0],bestMove[1]

def isMoveInListAI3(possibleMoves, listToCheck):
    '''Checks if any of the possible moves are in
    the list provided. If they are, they are added
    to the refined list, and if there is at least
    one move, the list is passed to the AI1 function
    to determine which of these refined moves takes
    the most pieces. If no moves are found, (-1,-1)
    is returned to indicate this.

    Arguments:
    possibleMoves (list) -- list of the computer's possible moves
    listToCheck (list) -- the list based on position value for
    possibleMoves to be checked against.
    '''
    refinedCoords = []
    # check to see if any of possible moves are
    # in list of desirable moves, if so, add them
    # to refinedMoves
    for coord in possibleMoves:
        if coord in listToCheck:
            refinedCoords.append([coord[0],coord[1]])
    # if desirable moves are found, pick a random one
    if len(refinedCoords) > 0:
        return(AI1(refinedCoords))
    else:
        # if none are found, return impossible
        # move to indicate this
        return (-1,-1)

def AI3(possibleMoves):
    '''Chooses best move by their position worth. If there is
    a corner move, choose that. If not, continue to next best
    category, etc.

    Arguments:
    possibleMoves (list) -- the list of valid moves for the AI
    '''
    best99 = [[0,0], [0,7],[7,0], [7,7]]
    second8 = [[0,2],[2,0],[0,5],[5,0],[7,2],[2,7],[7,5],[5,7]]
    third7 = [[2,2], [5,2],[2,5],[5,5]]
    fourth6 = [[0,3],[3,0],[4,0],[0,4], [7,3],[3,7],[7,4],[4,7]]
    fifth4 = [[3,2],[2,3],[4,2],[2,4],[5,3],[3,5],[5,4],[4,5]]
    sixth0 = [[3,3],[3,4],[4,3],[4,4]]
    seventh_3 = [[3,1],[1,3],[4,1],[1,4],[6,3],[3,6],[4,6],[6,4]]
    eigth_4 = [[2,1],[1,2],[5,1],[1,5],[6,2],[2,6],[5,6],[6,5]]
    ninth_8 = [[0,1],[1,0],[0,6],[6,0],[7,1],[1,7],[7,6],[6,7]]
    tenth_24 = [[1,1],[6,6],[6,1],[1,6]]

    if isMoveInListAI3(possibleMoves, best99) != (-1,-1):
        return isMoveInListAI3(possibleMoves, best99)
    elif isMoveInListAI3(possibleMoves, second8) != (-1,-1):
        return isMoveInListAI3(possibleMoves, second8)
    elif isMoveInListAI3(possibleMoves, third7) != (-1,-1):
        return isMoveInListAI3(possibleMoves, third7)
    elif isMoveInListAI3(possibleMoves, fourth6) != (-1,-1):
        return isMoveInListAI3(possibleMoves, fourth6)
    elif isMoveInListAI3(possibleMoves, fifth4) != (-1,-1):
        return isMoveInListAI3(possibleMoves, fifth4)
    elif isMoveInListAI3(possibleMoves, sixth0) != (-1,-1):
        return isMoveInListAI3(possibleMoves, sixth0)
    elif isMoveInListAI3(possibleMoves, seventh_3) != (-1,-1):
        return isMoveInListAI3(possibleMoves, seventh_3)
    elif isMoveInListAI3(possibleMoves, eigth_4) != (-1,-1):
        return isMoveInListAI3(possibleMoves, eigth_4)
    elif isMoveInListAI3(possibleMoves, ninth_8) != (-1,-1):
        return isMoveInListAI3(possibleMoves, ninth_8)
    else:
        return isMoveInListAI3(possibleMoves, tenth_24)


def isMoveInListAI2(possibleMoves, listToCheck):
    '''Checks to see if any of the possible moves are
    in the list provided. If any, they are added to a new
    refined list and this is then passed to the AI1 function
    to determine which of these refined moves takes the most
    pieces. If none are found, (-1,-1) coordinates are
    returned to indicate this.

    Arguments:
    possibleMoves (list) -- list of the computer's possible moves
    listToCheck (list) -- the list based on position value for
    possibleMoves to be checked against.
    '''
    refinedMoves = []
    # check to see if any of possible moves are
    # in list of desirable moves, if so, add them
    # to refinedMoves
    for coord in possibleMoves:
        if coord in listToCheck:
	        refinedMoves.append([coord[0], coord[1]])
    # if there is more than one move to choose from, select by
    # passing to AI1, aka greedy
    if len(refinedMoves) > 1:
        return(AI1(refinedMoves))
    elif len(refinedMoves) == 1:
        return refinedMoves[0][0], refinedMoves[0][1]
    else:
        # if no desirable moves are found, return
        # impossible move to indicate this
        return (-1,-1)

def AI2(possibleMoves):
    '''Follows same principles as AI2 function, except that
    if there are moves that rank second to fifth, the move
    that takes the most pieces is chosen.

    Arguments:
    possibleMoves (list) -- the list of valid moves for the AI
    '''
    best99 = [[0,0], [0,7],[7,0], [7,7]]
    second8 = [[0,2],[2,0],[0,5],[5,0],[7,2],[2,7],[7,5],[5,7]]
    third7 = [[2,2], [5,2],[2,5],[5,5]]
    fourth6 = [[0,3],[3,0],[4,0],[0,4], [7,3],[3,7],[7,4],[4,7]]
    fifth4 = [[3,2],[2,3],[4,2],[2,4],[5,3],[3,5],[5,4],[4,5]]
    sixth0 = [[3,3],[3,4],[4,3],[4,4]]
    seventh_3 = [[3,1],[1,3],[4,1],[1,4],[6,3],[3,6],[4,6],[6,4]]
    eigth_4 = [[2,1],[1,2],[5,1],[1,5],[6,2],[2,6],[5,6],[6,5]]
    ninth_8 = [[0,1],[1,0],[0,6],[6,0],[7,1],[1,7],[7,6],[6,7]]
    tenth_24 = [[1,1],[6,6],[6,1],[1,6]]

    # define lists to check
    bestMoves = best99
    secondBestMoves = second8 + third7 + fourth6 + fifth4
    thirdBestMoves = sixth0 + seventh_3 + eigth_4 + ninth_8
    middleMoves = secondBestMoves + thirdBestMoves
    worstMoves = tenth_24

    if isMoveInListAI2(possibleMoves, bestMoves) != (-1,-1):
        return isMoveInListAI2(possibleMoves, best99)
    elif isMoveInListAI2(possibleMoves, middleMoves) != (-1,-1):
        return isMoveInListAI2(possibleMoves, middleMoves)
    else:
        return isMoveInListAI2(possibleMoves, worstMoves)

def endGame():
    '''Once no more move can be made the game will end and a popup displaying
    the winning color will be made.'''
    global activePopup
    global gameHasEnded
    largePopupStartX = BOARD_TOP_LEFT_X + (PIECE_SIZE / 2)
    largePopupStartY = BOARD_TOP_LEFT_X + (BOARD_SIZE - PIECE_SIZE / 2)
    largePopupSize = (PIECE_SIZE * 7)

    gameHasEnded = True
    activePopup = True
    score1, score2 = scorekeeper()
    if score1 > score2:
        winner = COLOR1.capitalize()
    elif score2 > score1:
        winner = COLOR2.capitalize()
    else:
        winner = 'Draw'
    popup.home()
    popup.goto(largePopupStartX, largePopupStartY)
    popup.seth(270)
    drawQuad(largePopupSize, largePopupSize,'#333',popup)
    popup.color('white')
    popup.goto(largePopupStartX + (largePopupSize / 2), largePopupStartY - PIECE_SIZE)
    popup.write('Game Over',align='center',font=('',FONTSIZE_LARGE,''))
    if winner != 'draw':
        popup.goto(largePopupStartX + (largePopupSize / 2), largePopupStartY - (PIECE_SIZE*2))
        popup.write('{0} Wins!!!'.format(winner),align='center',
        font=('',FONTSIZE_LARGE,''))
    else:
        popup.goto(largePopupStartX + (largePopupSize / 2), largePopupStartY - (PIECE_SIZE*2))
        popup.write('It\'s a draw!',align='center',font=('',FONTSIZE_LARGE,''))
    popup.goto(largePopupStartX + (largePopupSize / 2), largePopupStartY - (PIECE_SIZE*4))
    popup.write('Click to start a new game.',align='center',font=('',FONTSIZE_LARGE,''))

def saveGame():
    '''When the user clicks the save 'button' they will be given a dialogue in
    which they can save the game with a unique name.'''
    gamesList = []
    try:
        cwd = os.getcwd()
        savedDir = os.path.join(cwd,'savedGames')
        for file_ in os.listdir(savedDir):
            filename, fileext = os.path.splitext(file_)
            if fileext == '.reversi':
                gamesList.append(filename)
        saveName = wn.textinput('','Name of game:')
        if saveName in gamesList:
            saveName = wn.textinput('','Game already exists.\n' +
            'To overwrite the game, please re-enter the name.\nName of game:')
        if saveName != None and saveName != "":
            cwd=os.getcwd()
            outFile = os.path.join(cwd,'savedGames',saveName + '.reversi')
            colorDict = {COLOR1:'COLOR1',COLOR2:'COLOR2'}
            with open(outFile,'w') as gameFile:
                gameFile.writelines(''.join(str(j) for j in i) +
                                    '\n' for i in gameState)
                gameFile.write(colorDict[userColor])
                gameFile.write('\n' + str(difficultySetting))
                gameFile.write('\n' + str(hintsEnabled))
        elif saveName == "":
            blankNameChoice = wn.numinput('Welcome','Nothing entered\n\n' +
                        'Choose an option\n\n1) Try again\n2) Cancel\n',1,1,2)
            if blankNameChoice == 1:
                saveGame()
    except:
        # for debugging
        print("Error. The savedGames directory may not exist, for example.")
        exit()

def rules():
    '''When the rules 'button' is clicked this will bring up a popup that will
    contain the rules of Reversi for the user to read.'''
    global activePopup
    largePopupStartX = BOARD_TOP_LEFT_X + (PIECE_SIZE / 2)
    largePopupStartY = BOARD_TOP_LEFT_X + (BOARD_SIZE - PIECE_SIZE / 2)
    largePopupSize = (PIECE_SIZE * 7)

    activePopup = True
    popup.goto(largePopupStartX, largePopupStartY)
    popup.seth(270)
    drawQuad(largePopupSize, largePopupSize,'#333',popup)
    popup.color('white')
    popup.goto(largePopupStartX + (largePopupSize / 2), largePopupStartY - PIECE_SIZE)
    popup.write('Reversi Rules',align='center',font=('',FONTSIZE_LARGE,''))
    popup.goto(largePopupStartX + (largePopupSize / 2), largePopupStartY - (PIECE_SIZE*5.5))
    popup.write('''
How to play:
Place your marker on the grid so that
you make at least one straight line
(horizontal, vertical, or diagonal)
between your new marker and another one
of your existing markers. One or more
markers belonging to the opponent must
be between them. All opponents markers
in the line are then captured and changed
to your colour. A player misses their turn
if there are no valid moves. The game ends
when there are no valid moves. The player
with the most tiles wins.
    ''',align='center',font=('',FONTSIZE,''))

def newGame(option="choice"):
    ''' Creates and starts a new game or loads saved game. '''
    global gameState, playerTurn
    playerTurn = COLOR1
    gameState = copy.deepcopy(origGameState)
    if option == "new":
        userIn = 1
    elif option == "load":
        userIn = 2
    else:
        userIn = openingWindow()
    if userIn == 1:
        piece.clear()
        drawInitialPieces()
        global userColor
        userColor = chooseRandomColor()
        changeDifficulty()
        if userColor == playerTurn:
            validList = getValidMoves()
            showHints(validList)
        newGameAlert()
    elif userIn == 2:
        loadGame()
        if userColor == playerTurn:
            validList = getValidMoves()
            showHints(validList)
        loadGameAlert()
    if userColor != playerTurn:
        time.sleep(1)
        popup.clear()
        computerMove()

def main():
    ''' Starts the game upon executing file '''
    setupGameboard()
    newGame()
    wn.onclick(userClickInput)

# call main function to start game
if __name__ == '__main__':
    main()

wn.mainloop()
