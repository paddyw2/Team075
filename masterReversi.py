"""
Team 075: Yang Li, Chi Nguyen, Patrick Withams, Greg Young
This program creates a Reversi game using Turtle Graphics
"""

#=========================================================#
#                                                         #
# Source: http://www.samsoft.org.uk/reversi/strategy.htm  #
#                                                         #
#=========================================================#

import turtle as tt
import random
import sys
import time


# writes a popup that displays which player won the game
def endgamePopup(winner):
    global endgameWindowActive
    global activePopup
    activePopup = True
    endgameWindowActive = True
    popup.home()
    popup.goto(60,-80)
    popup.color('#232323')
    popup.begin_fill()
    for i in range(2):
        popup.fd(200)
        popup.rt(90)
        popup.fd(160)
        popup.rt(90)
    popup.end_fill()
    popup.color("white")
    popup.goto(160, -120)
    popup.write('''
Game Over!
    ''',align='center',font=('',18,''))
    if winner != 'draw':
        popup.goto(160, -160)
        popup.write('''
''' + winner + ''' Wins!
    ''',align='center',font=('',14,''))
    else:
        popup.goto(160, -160)
        popup.write('''
		It's a draw!
        ''',align='center',font=('',14,''))

# popup that displays the instructione
def instructionPopup():    
    global instructionWindowActive
    global activePopup
    instructionWindowActive = True
    activePopup = True
    popup.home()
    popup.goto(60,-60)
    popup.color('#232323')
    popup.begin_fill()
    for i in range(4):
        popup.fd(200)
        popup.rt(90)
    popup.end_fill()
    popup.color("white")
    popup.goto(80, -250)
    popup.write('''
How to play: Place your marker
on the grid so that you make
least one straight (horizontal,
vertical, or diagonal) line
between your new marker and
another of your existing marker,
with one or more markers
belonging to the opponent
between them. All opponents
markers in the line are captured.
A player misses their turn if
there are no valid moves.
    ''',align='left',font=('',14,''))

# writes rectangle with ? on it in the location that triggers the instructions popup
def instructionButton():
    instructions.home()
    instructions.goto(360, 80)
    instructions.color('red')
    instructions.begin_fill()
    for i in range(4):
        instructions.fd(40)
        instructions.rt(90)
    instructions.end_fill()
    instructions.color("white")
    instructions.goto(380, 45)
    instructions.write("?", align='left',font=('',18,''))

# writes rectangle with Quit on it in the location that triggers the instructions popup
def quitButton():
    quit.home()
    quit.goto(-70, 80)
    quit.color('red')
    quit.begin_fill()
    for i in range(4):
        quit.fd(40)
        quit.rt(90)
    quit.end_fill()
    quit.color("white")
    quit.goto(-60, 45)
    quit.write("Quit", align='left',font=('',18,''))


# draws the horizontal and vertical lines for the game board
def drawLines(num, long, short, turn, color):
    for i in range(num):
        board.color(color)
        board.pd()
        board.fd(long)
        board.pu()
        board.fd(-long)
        board.rt(turn)
        board.fd(short)
        board.rt(-turn)

# draws any color-filled in rectangle or square needed, with whatever turtle is used as a parameter
def drawRectangle(length, width, turn, color, turt):
    turt.pu()
    turt.color(color)
    turt.begin_fill()
    for i in range(2):
        turt.fd(length)
        turt.rt(turn)
        turt.fd(width)
        turt.rt(turn)
    turt.end_fill()

# calls the drawLines and drawRectangle functions to set the game board up. also writes the title
# above the board and the instructions below the board. this function is called once on start up in
# the setup function.
def drawGrid(LINES, ANGLE, BOXSZ, WIDTH):
    BGCOL = '#64A23E'
    LNCOL = 'white'

    drawRectangle(WIDTH, WIDTH,ANGLE,BGCOL, board)
    drawLines(LINES, WIDTH, BOXSZ, ANGLE,LNCOL)
    board.setpos(WIDTH,0)
    board.rt(ANGLE)
    drawLines(LINES, WIDTH, BOXSZ, ANGLE, LNCOL)

    board.pu()
    board.goto(WIDTH//2,20)
    board.color('black')
    board.pd()
    board.write('  R  E  V  E  R  S  I  ', align='center', font=('',36,'bold'))

# takes a coordinate, like 3,2, and converts it into a drawable coordinate that the drawRectangle
# function can use. used to draw pieces chosen by players on the board.
def drawPiece(gridX, gridY, color, BOXSZ, ANGLE):
    piece.pu()
    piece.home()
    gridX = gridX * BOXSZ
    gridY = gridY * BOXSZ
    piece.goto(gridX+2, -(gridY+2))
    drawRectangle(BOXSZ-4,BOXSZ-4,ANGLE,color,piece)

# draws score board with current scores
def scoreboard():
    black.clear()
    black.home()
    black.pu()
    black.pencolor(COLOR1)
    black.goto(-33, -30)
    blackPieces = calcWinner("black")
    black.write(blackPieces, align='center', font=('',22))
    white.clear()
    white.home()
    white.pu()
    white.pencolor(COLOR2)
    white.goto(355, -30)
    whitePieces = calcWinner("white")
    white.write(whitePieces, align='center', font=('',22))


# calls the drawGrid function to set board up and then draws the four starting pieces. called once
# on startup.
def setup(LINES, ANGLE, BOXSZ, WIDTH, COLOR1, COLOR2):
    print('''

     welcome to...

    R E V E R S I!

    ''')
    print("Click the top left corner at any time to quit")
    print("Click on the question mark to view the instructions")
    drawGrid(LINES,ANGLE,BOXSZ,WIDTH)
    drawPiece(3,4,COLOR1,BOXSZ,ANGLE)
    drawPiece(4,4,COLOR2,BOXSZ,ANGLE)
    drawPiece(4,3,COLOR1,BOXSZ,ANGLE)
    drawPiece(3,3,COLOR2,BOXSZ,ANGLE)
    scoreboard()
    # update gamestate string to have starting positions marked
    updateGameState("w", 3, 3)
    updateGameState("b", 3, 4)
    updateGameState("b", 4, 3)
    updateGameState("w", 4, 4)
    # draw instructions button
    instructionButton()
    quitButton()

# Creates a 2D array where the game state will be stored
def createGameState():
    gameState = [[],[],[],[],[],[],[],[]]
    for x in range(8):
        for y in range(8):
            gameState[y].append("blank")
    gameState[3][3] = COLORNAME2
    gameState[3][4] = COLORNAME1
    gameState[4][3] = COLORNAME1
    gameState[4][4] = COLORNAME2
    return gameState

# Updates the gamestate in position [gridX][gridY] with the current player
# colour
def updateGameState(player, gridX, gridY):
    global gameState
    gameState[gridX][gridY] = player

# Checks if the coordinates passed are within the board range and returns the position of piece in the gameState based on its coordinates. Returns -1 if the coordinate is off the board.
def returnGameStatePosition(x,y):
    if x < 0 or y < 0 or x > 7 or y > 7:
    	gameStatePosition = -1
    else:
    	gameStatePosition = gameState[x][y]
    return gameStatePosition

# choosing moves by their position worth
def hardCalc(possibleMoves, colour):
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

# choosing moves by the number of pieces they take
# for every possible move, the total number of pieces filled in is calculated and the move
# that takes or 'fills in' the most pieces is chosen. playerColour parameter may be unused.
def bestMoveCalc(possibleMoves, colour):
    totalMoves = 0
    middleMoves = []
    totalList = []
	# for every coordinate in possible moves list
    for x,y in possibleMoves:
        # lists need to be emptied at each loop
        totalList[:] = []
        middleMoves[:] = []
		# nested loop: for each coordinate, check each direction to see what moves would be filled in
        for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:

            middleMoves = fillMoves(x,y, direction1, direction2, 1, colour)

            # take the result of that particular direction and add it to the list of moves
            if len(middleMoves) > 0:
                for i in range(len(middleMoves)):
                    first = middleMoves[i][0]
                    second = middleMoves[i][1]
                    totalList.append([first, second])
        # we now have a 2d list of the total coords
		# convert that list into regular list so that each coordinate is a unique string that
		# can be checked for duplication. (2,1 has to be 21, because an addition etc. could be
		# replicated with 1,2 which is a different coordinate.)
        newList = []
        newList[:] = []
        for i in range(len(totalList)):
            num1 = totalList[i][0]
            num2 = totalList[i][1]
            newList.append(str(num1)+str(num2))
        # call set method on list to remove duplicates and convert back to list type
        tempList = set(newList)
        tempList = list(tempList)
        # if the total number of filled in pieces is greater than the running total,
		# update the coordinates to be chosen as the best move with the coordinates
		# being checked
        if len(tempList) > totalMoves:
            totalMoves = len(tempList)
            gridX = x
            gridY = y
	# *** added difficulty ***
	# this checks if there are any corner moves, and if there are, chooses them
    for x in possibleMoves:
        if x == [0,0] or x == [7,7] or x == [0,7] or x == [7,0]:
            gridX = x[0]
            gridY = x[1]
    # print(gridX, gridY)
    return (gridX,gridY)

# once a move has been chosen and verified to be valid, the middle moves, or moves in between, need to
# be determined and coloured. to do this, the chosen move coordinate is taken and for each possible
# direction, a search is performed backwards until the direction is determined to be either a
# valid colouring direction or an invalid one. if it is valid, the coordinates in between the chosen move
# and the end point are coloured the current players colours.
def fillMoves(x, y, direction1, direction2, endSearch, colour):
    middleMoves = []
    while endSearch != 0:
        newx = x + direction1
        newy = y + direction2
        gameStatePos = returnGameStatePosition(newx,newy)
        if newx < 0 or newy < 0 or newx > 7 or newy > 7:
            return -1
        elif gameStatePos != "blank" and gameStatePos != playerTurn:
            endSearch = 2
            returnedMoves = fillMoves(newx, newy, direction1, direction2, endSearch, colour)
            middleMoves.append([newx, newy])
            if returnedMoves != -1:
                return (middleMoves + returnedMoves)
            else:
                return -1
        elif gameStatePos == playerTurn and endSearch == 2:
            return [middleMoves]
        else:
            return -1

# after the searchPossibleMoves function calculates the player's current pieces, their possible moves
# are then calculated below. for each of the current player's pieces on the board, all directions are
# searched until either a valid move is reached, or an indicator that the direction will never hold a
# valid move is reached. if a valid move is found, the coordinates are returned in a tuple.
def calcPossibleMoves(x, y, direction1, direction2, endSearch):
    while endSearch != 0:
        newX = x + direction1
        newY = y + direction2
        gameStatePos = returnGameStatePosition(newX,newY)
        if newX < 0 or newY < 0 or newX > 7 or newY > 7:
            return (-1, -1)
        elif gameStatePos != "blank" and gameStatePos != playerTurn:
            endSearch = 2
            (newCoord1, newCoord2) = calcPossibleMoves(newX, newY, direction1, direction2, endSearch)
            return (newCoord1, newCoord2)
        elif gameStatePos == "blank" and endSearch == 2:
            return (newX, newY)
        elif gameStatePos == "blank":
            return (-1, -1)
        else:
            return (-1, -1)

# searches the gameState list for values matching the current player's colour. for each piece that is
# found, the calcPossibleMoves function is called for all directions and if the return value is not
# (-1,-1), which signifies no valid moves for that direction, then the values are appeneded to the
# potMoves list, which is returned by the function.
def searchPossibleMoves():
    potMoves = []
    for x in range(8):
        for y in range(8):
            gameStatePos = returnGameStatePosition(x,y)
            if gameState[x][y] == playerTurn:
                for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]: # numbers in list represent all possible directions
                    (gridX, gridY) = calcPossibleMoves(x, y, direction1, direction2, 1)
                    # check that it returns a number
                    if gridX >= 0:
                        potMoves.append([gridX, gridY])
    return potMoves

# used to swap the current player value when one turn is over
def playerSwap(colour):
    if colour == COLOR1:
        return COLORNAME2
    else:
        return COLORNAME1

# used to get opposite colour code
def colourSwap(colour):
    if colour == COLOR1:
        return COLOR2
    else:
        return COLOR1

# print player totals and calculate the winner
def gameOver():
    print("The final game state is:", gameState)
    totalWhite = calcWinner("white")
    totalBlack = calcWinner("black")
    print("Black: ", totalBlack)
    print("White: ", totalWhite)
    if totalWhite == totalBlack:
        print("It was a draw!")
        endgamePopup('draw')
    elif totalBlack > totalWhite:
        print("The black player wins!")
        endgamePopup('Black')
    else:
        print("The white player wins!")
        endgamePopup('White')

# search gameState for parameter, and everytime player is found, update total. when finished searching
# the list, return the total.
def calcWinner(player):
    if player == "white":
        piece = "w"
    else:
        piece = "b"
    totalPieces = 0
    for i in range(8):
        for x in range(8):
            if gameState[i][x] == piece:
                totalPieces += 1
    return totalPieces

# checks to see whether the user clicks on board or exit button
def userClickProcess(x,y):
    global activePopup
    if playerTurn == COLORNAME1:
        colour = COLOR1
    else:
        colour = COLOR2
    gridX = int(x // 40)
    gridY = -(int(y // 40)) - 1
    if (0 <= gridX <= 7) and (0 <= gridY <= 7) and activePopup != True:
        userMove(colour, gridX, gridY)
    elif gridX == -2 and gridY == -2:
        sys.exit()
    elif gridX == 9 and gridY == -2:
        instructionPopup()
    elif activePopup == True:
        if instructionWindowActive:
            popup.clear()
            activePopup = False
        elif endgameWindowActive:
            # take exit/new game input click coordinates
            popup.clear()
            activePopup = False

# triggers computer move. very similar to userMove function with the exception of
# calling the bestMoveCalc function to generate the chosen coordinates
def computerMove():
    time.sleep(0.5)
    # to allow player turn to be swapped
    global playerTurn
    if playerTurn == COLORNAME1:
        colour = COLOR1
    else:
        colour = COLOR2

    middleMoves = []
    possibleMoves = searchPossibleMoves()
    if difficultySetting == 0:
        (gridX,gridY) = bestMoveCalc(possibleMoves, colour)
    elif difficultySetting == 1:
        (gridX,gridY) = hardCalc(possibleMoves, colour)
    validMove = False
    # check if chosen move is valid
    for i in range(len(possibleMoves)):
        if possibleMoves[i][0] == gridX and possibleMoves[i][1] == gridY:
            validMove = True
    if validMove is True:
        # update gameState with move and colour coordinate
        updateGameState(playerTurn, gridX, gridY)
        drawPiece(gridX,gridY, colour, BOXSZ, ANGLE)
        # fill in and update gameStatefor all other pieces to be coloured
        movesToFill = []
        for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]: # numbers in list represent all possible directions
            middleMoves = fillMoves(gridX, gridY, direction1, direction2, 1, colour)
            if middleMoves != -1:
                movesToFill = movesToFill + middleMoves

        for i in range(len(movesToFill)):
            if movesToFill[i] != []:
                updateGameState(playerTurn, movesToFill[i][0], movesToFill[i][1])
                drawPiece(movesToFill[i][0], movesToFill[i][1],colour,BOXSZ,ANGLE)

		# update scoreboard
        scoreboard()
        # check whether next player can go
        playerTurn = playerSwap(colour)
        nextPossibleMoves = searchPossibleMoves()
        if len(nextPossibleMoves) == 0: # if they can't go
            newColour = colourSwap(colour) # swap colour so playerSwap below works
            playerTurn = playerSwap(newColour) # change colour back to player who just went
            nextPossibleMoves = searchPossibleMoves() # calculate that player's possible moves
            if len(nextPossibleMoves) == 0: # if they also have no moves, then the game is over
                print("Game over!")
                gameOver()
            else: # if they do have moves, then other player just misses a turn
                print("No moves for the next player! Skipping a go!")
                computerMove()
        else:
            if playerTurn == "b":
                currentPlayer = "Black"
            else:
                currentPlayer = "White"
            print(currentPlayer, "player's turn!") # playerTurn is converted to caps
    else:
        print("Not a valid move, try again!")

# this controls what happens when it is a player's turn. first, it calculates the possible moves
# the player has. then it takes their input for their next move. if their move matches once of the
# possible moves, then it is valid. if not, end the function without changing the player turn
# and re-enter main function loop that will call the function again, giving the user another chance.
# if it is valid, add that move to the gameState list, and then colour it the player's colour. next,
# calculate what moves now need to be filled in. finally, check whether next player can go.
def userMove(colour, gridX, gridY):
    # to allow player turn to be swapped
    global playerTurn
    middleMoves = []
    possibleMoves = searchPossibleMoves()
    validMove = False
    # check if chosen move is valid
    for i in range(len(possibleMoves)):
        if possibleMoves[i][0] == gridX and possibleMoves[i][1] == gridY:
            validMove = True
    if validMove is True:
        # update gameState with move and colour coordinate
        updateGameState(playerTurn, gridX, gridY)
        drawPiece(gridX,gridY, colour, BOXSZ, ANGLE)
        # fill in and update gameStatefor all other pieces to be coloured
        movesToFill = []
        for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]: # numbers in list represent all possible directions
            middleMoves = fillMoves(gridX, gridY, direction1, direction2, 1, colour)
            if middleMoves != -1:
                movesToFill = movesToFill + middleMoves

        for i in range(len(movesToFill)):
            if movesToFill[i] != []:
                updateGameState(playerTurn, movesToFill[i][0], movesToFill[i][1])
                drawPiece(movesToFill[i][0], movesToFill[i][1],colour,BOXSZ,ANGLE)
		# update scoreboard
        scoreboard()
        # check whether next player can go
        playerTurn = playerSwap(colour)
        nextPossibleMoves = searchPossibleMoves()
        if len(nextPossibleMoves) == 0: # if they can't go
            newColour = colourSwap(colour) # swap colour so playerSwap below works
            playerTurn = playerSwap(newColour) # change colour back to player who just went
            nextPossibleMoves = searchPossibleMoves() # calculate that player's possible moves
            if len(nextPossibleMoves) == 0: # if they also have no moves, then the game is over
                print("Game over!")
                gameOver()
            else: # if they do have moves, then other player just misses a turn
                print("No moves for the next player! Skipping a go!")
        else:
            # print player turn
            if playerTurn == "b":
                currentPlayer = "Black"
            else:
                currentPlayer = "White"
            print(currentPlayer, "player's turn!") # playerTurn is converted to caps
            computerMove()
    else:
        print("Not a valid move, try again!")

# generate either black or white at random
def chooseRandomColour():
    # assign user a colour at random
    headstails = random.randrange(1, 3)
    if headstails == 1:
        user = "black"
    else:
        user = "white"
    return user

# calls the setup functiont to draw the board. creates a while loop that triggers the userMove
# function with the colour of the current player.
def main():
	# assign human player colour
    user = chooseRandomColour()
    setup(LINES, ANGLE, BOXSZ, WIDTH, COLOR1, COLOR2)
    # black player always goes first
    print("Black player's turn!")
    # if computer is black, let it go first
    if user == "white":
        computerMove()
    # once the computer has gone it will now wait for a click
    wn.onclick(userClickProcess)

# global constants
wn = tt.Screen()
wn.setup(startx=0,starty=0)
wn.setworldcoordinates(-60,-400,400,60)
wn.bgcolor("#228B22")
instructions = tt.Turtle()
instructions.pu()
instructions.ht()
instructions.speed('fastest')
quit = tt.Turtle()
quit.pu()
quit.ht()
quit.speed('fastest')
popup = tt.Turtle()
popup.pu()
popup.ht()
popup.speed('fastest')
board = tt.Turtle()
piece = tt.Turtle()
black = tt.Turtle() #turtle for black score
white = tt.Turtle() #turtle for white score
black.speed('fastest')
white.speed('fastest')
board.speed('fastest')
piece.speed('fastest')
board.ht()
piece.ht()
black.ht()
white.ht()
LINES = 9
ANGLE = 90
BOXSZ = 40
WIDTH = (LINES - 1) * BOXSZ
COLOR1 = ('#333')
COLOR2 = ('#fff')
COLORNAME1 = "b"
COLORNAME2 = "w"

# global variables (not possible to make local - they need to affect everything)
# this is necessary as the click event cannot pass parameters except x,y
# an "o" represents a blank position - all blank to start
activePopup = False
gameState = createGameState()
playerTurn = COLORNAME1
instructionWindowActive = False
endgameWindowActive = False
difficultySetting = 1
# call main function to start the game
main()
# loop main function click event
wn.mainloop()
