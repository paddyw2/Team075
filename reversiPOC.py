"""
Team 075: Yang Li, Chi Nguyen, Patrick Withams, Greg Young
This program creates a Reversi game using Turtle Graphics
"""

import copy
import os
import time
from sys import exit
import turtle as tt
from random import randrange

def setupGameboard():
    '''Sets up the gameboard by drawing the grid and surrounding items'''
    setup.goto(80,80)
    drawQuad(320,320,'#228B22',setup)
    drawGrid(setup)
    writeTitle(setup)
    drawButtons(setup)

def drawQuad(width,height,color,turt,depth=False):
    '''Draws filled quadrilaterals with given Turtle.

    Arguments:
    width (int) -- the left to right size
    height (int) -- the top to bottom size
    color (str) -- the fill color
    turt (Turtle) -- the Turtle that is used to draw quadrilateral
    depth (bool) -- if True, will give the appearance of a 3D box (default False)
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
        turt.pd()
        turt.color('black', color)
        turt.begin_fill()
        turt.pensize(1)
        turt.fd(width)
        turt.lt(90)
        turt.fd(height)
        turt.lt(90)
        turt.pensize(3)
        turt.fd(width)
        turt.lt(90)
        turt.fd(height)
        turt.lt(90)
        turt.end_fill()
        turt.pu()

def drawGrid(turt):
    '''Draws the playing grid on the game board.

    Argument:
    turt (Turtle)-- the Turtle used to draw the grid
    '''
    turt.color('#AAA')
    drawLines(turt)
    turt.goto(400,80)
    turt.lt(90)
    drawLines(turt)

def drawLines(turt):
    '''Draws the lines for the playing grid.

    Argument:
    turt (Turtle) -- the Turtle used to draw the lines
    '''
    for i in range(9):
        turt.pd()
        turt.fd(320)
        turt.pu()
        turt.fd(-320)
        turt.lt(90)
        turt.fd(40)
        turt.lt(-90)

def writeTitle(turt):
    '''Write 'REVERSI' with drop shadow above grid'''
    turt.goto(242,62)
    turt.color('#000')
    turt.pd()
    turt.write('*  R  E  V  E  R  S  I *', align='center', font=('',40,'bold'))
    turt.pu()
    turt.goto(240,60)
    turt.color('#FFF')
    turt.pd()
    turt.write('*  R  E  V  E  R  S  I *', align='center', font=('',40,'bold'))
    turt.pu()

def drawButtons(turt):
    '''Draws "buttons" on the game screen to demarcate areas for the user to
    click to either exit the game or save it.

    Argument:
    turt (Turtle) -- the Turtle used to draw the buttons
    '''
    turt.goto(80,450)
    turt.seth(270)
    drawQuad(20,80,'white',turt,True)
    turt.goto(120,447)
    turt.write('RULES',align='center',font=('',14))
    turt.goto(200,450)
    turt.seth(270)
    drawQuad(20,80,'white',turt,True)
    turt.goto(240,447)
    turt.write('SAVE',align='center',font=('',14))
    turt.goto(320,450)
    turt.seth(270)
    drawQuad(20,80,'white',turt,True)
    turt.goto(360,447)
    turt.write('EXIT',align='center',font=('',14))

def openingWindow():
    '''Input window where the user chooses an option from a list using
    numeric input. Can start a new game or load a saved game. If the Cancel
    button is pressed the game exits, otherwise it returns the integer value of
    the input.
    '''
    userIn = wn.numinput('','WELCOME TO REVERSI!\n\nChoose an option or Cancel '
                         'to quit.\n\n1) New Game\n2) Load Game\n',1,1,3)
    if userIn == None:
        exit()
    else:
        return int(userIn)

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
    xCoord = col * 40 + 80
    yCoord = row * 40 + 80
    piece.goto(xCoord+2,yCoord+2)
    global gameState
    if color == COLOR1:
        gameState[row][col] = 'B'
    else:
        gameState[row][col] = 'W'
    drawQuad(36,36,color,piece)
    scorekeeper()

def loadGame():
    '''Produces a list of saved games from savedGames directory and the user
    uses numerical input to select the game to load. The savedGames directory
    must be in the same directory as this .py file.
    '''
    gamesList = []
    '''Getting the path to the savedGames directory and appending saved games to
    gamesList.
    '''
    try:
        cwd = os.getcwd()
        savedDir = os.path.join(cwd,'savedGames')
        for file_ in os.listdir(savedDir):
            if file_.endswith('.reversi'):
                gamesList.append(file_)
        # Bring up user input window and wait for numberical input that corresponds
        # to a game file.
        txt = ''
        for i in range(len(gamesList)):
            txt += '\n' + str(i + 1) + ') ' + str(os.path.splitext(gamesList[i])[0])
        userIn = (wn.numinput('Load Game','Enter number of a saved game:' +
                 txt,None,1,len(gamesList)))
        while userIn == None:
            userIn = (wn.numinput('Load Game','Enter number of a saved game:' +
                      txt,None,1,len(gamesList)))
        userIn = int(userIn)
        # Opens the file selected by the user and reads the contents
        inFile = os.path.join(savedDir,gamesList[userIn-1])
        with open(inFile, 'r') as game:
            lines = game.readlines()
            newGameState = []
            for i in range(len(lines)):
                if i < 8:
                    row = list(lines[i].strip('\n'))
                    newGameState.append(row)
                elif i == 8:
                    lastLine = lines[i].strip()
        # Change global variables to reflect where the game was when user saved.'''
        colorDict = {'COLOR1' : COLOR1, 'COLOR2' : COLOR2}
        global gameState, playerTurn, userColor
        gameState = newGameState
        playerTurn = colorDict[lastLine]
        userColor = colorDict[lastLine]
        drawLoadedPieces()
    except:
        print("The savedGames directory does not exist.")
        newGame()

def drawLoadedPieces():
    '''Uses gameState to draw all the pieces from the saved game.'''
    for row in range(len(gameState)):
        for col in range(len(gameState[row])):
            if gameState[row][col] == 'B':
                color = COLOR1
                xCoord = col * 40 + 80
                yCoord = row * 40 + 80
                piece.goto(xCoord+2,yCoord+2)
                drawQuad(36,36,color,piece)
            elif gameState[row][col] == 'W':
                color = COLOR2
                xCoord = col * 40 + 80
                yCoord = row * 40 + 80
                piece.goto(xCoord+2,yCoord+2)
                drawQuad(36,36,color,piece)
    scorekeeper()

def scorekeeper():
    '''Uses gameState to count the number of each player's pieces and displays
    the total beside the gameboard.
    '''
    blkPc = 0
    whtPc = 0
    for i in range(len(gameState)):
        for j in range(len(gameState[i])):
            if gameState[i][j] == 'B':
                blkPc += 1
            if gameState[i][j] == 'W':
                whtPc += 1
    color1score.clear()
    color1score.goto(40,110)
    color1score.write(str(blkPc),align='center',font=('',22,'bold'))
    color2score.clear()
    color2score.goto(440,110)
    color2score.write(str(whtPc),align='center',font=('',22,'bold'))
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
    activePopup = True
    popup.goto(100,300)
    popup.seth(270)
    drawQuad(280,120,'#333',popup)
    popup.color('white')
    popup.goto(240,220)
    text1 = '{0} player goes first, your color is {1}'.format(
            COLOR1.capitalize(),userColor.capitalize())
    popup.write(text1,align='center',font=('',18))
    popup.goto(240,280)
    text2 = 'Click to continue...'
    popup.write(text2,align='center',font=('',18))

def loadGameAlert():
    '''Draws popup to alert users of their color after loaded game.'''
    global activePopup
    activePopup = True
    popup.goto(100,300)
    popup.seth(270)
    drawQuad(280,120,'#333',popup)
    popup.color('white')
    popup.goto(240,220)
    text1 = 'Your turn, your color is {0}'.format(userColor.capitalize())
    popup.write(text1,align='center',font=('',18))
    popup.goto(240,280)
    text2 = 'Click to continue...'
    popup.write(text2,align='center',font=('',18))

def userClickInput(x,y):
    '''Takes the input from a user click and depending the values executes the
    corresponding function.

    Arguments:
    x (float) -- x coordinate of where the user clicked
    y (float) -- y coordinate of where the user clicked
    '''
    global activePopup
    global gameHasEnded
    if activePopup == True:
        popup.clear()
        activePopup = False
        if gameHasEnded:
            newGame()
            gameHasEnded = False
    else:
        if (80 <= x <= 400) and (80 <= y <= 400):
            userMove(x,y)
        elif (80 <= x <= 160) and (430 <= y <=450):
            rules()
        elif (200 <= x <= 280) and (430 <= y <=450):
            saveGame()
        elif (320 <= x <= 400) and (430 <= y <=450):
            exit()

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
    global playerTurn
    validList = getValidMoves()
    gridX = int(xCoord // 40 - 2)
    gridY = int(yCoord // 40 - 2)
    if [gridX,gridY] in validList:
        drawPiece(gridX,gridY,playerTurn)
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
                endGame()
        else:
            computerMove()

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
    global playerTurn
    time.sleep(0.5)
    validList = getValidMoves()
    # AI based on diff setting
    if difficultySetting == 0:
        gridX,gridY = AI1(validList)
    elif difficultySetting == 1:
        gridX,gridY = AI3(validList)
    elif difficultySetting == 2:
        gridX,gridY = AI3(validList)
    drawPiece(gridX,gridY,'orange')
    time.sleep(1)
    drawPiece(gridX,gridY,playerTurn)
    flipList = []
    for dirX,dirY in dirList:
        flipList = toFlip(gridX,gridY,dirX,dirY,flipList)
        for col,row in flipList:
            drawPiece(col,row,playerTurn)
    playerTurn = playerSwap()
    validList = getValidMoves()
    if len(validList) == 0:
        playerTurn = playerSwap()
        validList = getValidMoves()
        if len(validList) == 0:
            endGame()
        else:
            computerMove()

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

# choosing moves by their position worth
def AI2(possibleMoves):
    # coordinates ranked by favourability
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

    for coord in possibleMoves:
        if coord in best99:
             return (coord[0], coord[1])

    for coord in possibleMoves:
        if coord in second8:
	        return (coord[0], coord[1])

    for coord in possibleMoves:
        if coord in third7:
	        return (coord[0], coord[1])

    for coord in possibleMoves:
        if coord in fourth6:
	        return (coord[0], coord[1])

    for coord in possibleMoves:
        if coord in fifth4:
	        return (coord[0], coord[1])

    for coord in possibleMoves:
        if coord in sixth0:
	        return (coord[0], coord[1])

    for coord in possibleMoves:
        if coord in seventh_3:
	        return (coord[0], coord[1])

    for coord in possibleMoves:
        if coord in eigth_4:
	        return (coord[0], coord[1])

    for coord in possibleMoves:
        if coord in ninth_8:
	        return (coord[0], coord[1])

    for coord in possibleMoves:
        if coord in tenth_24:
	        return (coord[0], coord[1])
        else:
	        print("We have a problem")


# choosing moves by their position worth, with extra twist
def AI3(possibleMoves):
    # coordinates ranked by favourability
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

    for coord in possibleMoves:
        if coord in best99:
             return (coord[0], coord[1])

    # takes 2nd, 3rd, 4th and 5th best moves, and picks the one
    # that takes most pieces
    refinedMoves = []
    for coord in possibleMoves:
        if coord in (second8 + third7 + fourth6 + fifth4):
	        refinedMoves.append([coord[0], coord[1]])

    if len(refinedMoves) > 1:
        return(AI1(refinedMoves))
    elif len(refinedMoves) == 1:
        return refinedMoves[0][0], refinedMoves[0][1]

    for coord in possibleMoves:
        if coord in sixth0:
	        return (coord[0], coord[1])

    for coord in possibleMoves:
        if coord in seventh_3:
	        return (coord[0], coord[1])

    for coord in possibleMoves:
        if coord in eigth_4:
	        return (coord[0], coord[1])

    for coord in possibleMoves:
        if coord in ninth_8:
	        return (coord[0], coord[1])

    for coord in possibleMoves:
        if coord in tenth_24:
	        return (coord[0], coord[1])
        else:
	        print("We have a problem")


def endGame():
    '''Once no more move can be made the game will end and a popup displaying
    the winning color will be made.'''
    global activePopup
    global gameHasEnded
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
    popup.goto(100,380)
    popup.seth(270)
    drawQuad(280,280,'#333',popup)
    popup.color('white')
    popup.goto(240,220)
    popup.write('Game Over',align='center',font=('',22,''))
    if winner != 'draw':
        popup.goto(240,300)
        popup.write('{0} Wins!!!'.format(winner),align='center',font=('',22,''))
    else:
        popup.goto(240,300)
        popup.write('It\'s a draw!',align='center',font=('',22,''))

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
        while saveName in gamesList:
            saveName = wn.textinput('','File exists.\nName of game:')
        if saveName != None:
            cwd=os.getcwd()
            outFile = os.path.join(cwd,'savedGames',saveName + '.reversi')
            colorDict = {COLOR1:'COLOR1',COLOR2:'COLOR2'}
            with open(outFile,'w') as gameFile:
                gameFile.writelines(''.join(str(j) for j in i) +
                                    '\n' for i in gameState)
                gameFile.write(colorDict[userColor])
    except:
        print("The savedGames directory does not exist. Game not saved.")

def rules():
    '''When the rules 'button' is clicked this will bring up a popup that will
    contain the rules of Reversi for the user to read.'''
    global activePopup
    activePopup = True
    popup.goto(100,380)
    popup.seth(270)
    drawQuad(280,280,'#333',popup)
    popup.color('white')
    popup.goto(240,220)
    popup.write('Under Construction',align='center',font=('',22,''))

def newGame():
    global gameState, playerTurn
    playerTurn = COLOR1
    piece.clear()
    gameState = copy.deepcopy(origGameState)
    userIn = openingWindow()
    if userIn == 1:
        drawInitialPieces()
        global userColor
        userColor = chooseRandomColor()
        newGameAlert()
    elif userIn == 2:
        loadGame()
        loadGameAlert()
    if userColor != playerTurn:
        time.sleep(1)
        popup.clear()
        computerMove()

def main():
    setupGameboard()
    userIn = openingWindow()
    if userIn == 1:
        drawInitialPieces()
        global userColor
        userColor = chooseRandomColor()
        newGameAlert()
    elif userIn == 2:
        loadGame()
        loadGameAlert()
    if userColor != playerTurn:
        time.sleep(1)
        popup.clear()
        computerMove()
    wn.onclick(userClickInput)

'''Global variables used to initialize the game window.'''
wn = tt.Screen()
wn.setup(startx=None,starty=None)
wn.screensize(900,900)
wn.setworldcoordinates(0,480,480,0)
bgdir = os.path.join(os.getcwd(),'img')
bgpic = os.path.join(bgdir,'table.gif')
wn.bgpic(bgpic)
wn.title('PYTHON REVERSI')
wn.tracer(0)

setup = tt.Turtle()
setup.ht()
setup.pu()

'''Global variables and constants.'''
COLOR1 = 'black'
COLOR2 = 'white'

piece = tt.Turtle()
piece.ht()
piece.pu()

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

difficultySetting = 2
userColor = ''
playerTurn = COLOR1
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
gameState = copy.deepcopy(origGameState)
dirList = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]

main()
wn.mainloop()
