"""
Team 075: Yang Li, Chi Nguyen, Patrick Withams, Greg Young
This program creates a Reversi game using Turtle Graphics
"""

import turtle as tt
import random
import sys

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

    board.pu()
    board.goto(WIDTH//2,-(WIDTH+65))
    board.write('How to play: Place your marker on the grid so that you make least one straight (horizontal,\nvertical, or diagonal) line between your new marker and another of your existing marker, with\none or more markers belonging to the opponent between them. All opponents markers in the\nline are captured. A player misses their turn if there are no valid moves.',align='center',font=('',14,''))

# takes a coordinate, like 3,2, and converts it into a drawable coordinate that the drawRectangle
# function can use. used to draw pieces chosen by players on the board.
def drawPiece(gridX, gridY, color, BOXSZ, ANGLE):
    piece.pu()
    piece.home()
    gridX = gridX * BOXSZ
    gridY = gridY * BOXSZ
    piece.goto(gridX+2, -(gridY+2))
    drawRectangle(BOXSZ-4,BOXSZ-4,ANGLE,color,piece)

def scoreboard():
    black.pu()
    black.pencolor(COLOR1)
    black.goto(-33, -30)
    black.write('##', align='center', font=('',22))
    white.pu()
    white.pencolor(COLOR2)
    white.goto(355, -30)
    white.write('##', align='center', font=('',22))


# calls the drawGrid function to set board up and then draws the four starting pieces. called once
# on startup.
def setup(LINES, ANGLE, BOXSZ, WIDTH, COLOR1, COLOR2):
    print('''

     welcome to...

    R E V E R S I!

    ''')
    print("Click the top left corner at any time to quit")
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

# creates gamestate variable as one long string, with moves marked as either "o" for blank,
# "w" for white, and "b" for black
def updateGameState(player, gridX, gridY):
    global gameState
    finalPosition = (gridX * 8) + gridY
    gameState = gameState[:finalPosition] + player + gameState[(finalPosition + 1):]

# returns the position of piece in the gameState string based on its coordinates
def returnStringPosition(x,y):
    stringPosition = (x * 8) + y
    return stringPosition


def bestMoveCalc(pos_moves, player_turn, colour):
    total_moves = 0
    middle_moves = []
    total_array = []
    for x,y in pos_moves:
        total_array[:] = []
        middle_moves[:] = []
        for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            middle_moves[:] = []
            fillMoves(x,y, direction1, direction2, 1, middle_moves, colour, True)
            if len(middle_moves) > 0:
                for i in range(len(middle_moves)):
                    first = middle_moves[i][0]
                    second = middle_moves[i][1]
                    total_array.append([first, second])

        new_array = []
        new_array[:] = []
        for i in range(len(total_array)):
            num1 = total_array[i][0]
            num2 = total_array[i][1]
            new_array.append(str(num1)+str(num2))

        temp_array = set(new_array)
        temp_array = list(temp_array)
        # end of small duplicate remover
        if len(temp_array) > total_moves:
            total_moves = len(temp_array)
            gridX = x
            gridY = y
    return (gridX,gridY)



# once a move has been chosen and verified to be valid, the middle moves, or moves in between, need to
# be determined and coloured. to do this, the chosen move coordinate is taken and for each possible
# direction, a search is performed backwards until the direction is determined to be either a
# valid colouring direction or an invalid one. if it is valid, the coordinates in between the chosen move
# and the end point are coloured the current players colours.
def fillMoves(x, y, direction1, direction2, endSearch, middleMoves, colour, bestMove):
    while endSearch != 0:
        newx = x + direction1
        newy = y + direction2
        stringPos = returnStringPosition(newx,newy)
        if newx < 0 or newy < 0 or newx > 7 or newy > 7:
            endSearch = 0
        elif gameState[stringPos] != "o" and gameState[stringPos] != playerTurn:
            endSearch = 2
            middleMoves.append([newx, newy])
            fillMoves(newx, newy, direction1, direction2, endSearch, middleMoves, colour, bestMove)
            endSearch = 0
        elif gameState[stringPos] == playerTurn and endSearch == 2:
            if not bestMove:
                for i in range(len(middleMoves)):
                    updateGameState(playerTurn, middleMoves[i][0], middleMoves[i][1])
                    drawPiece(middleMoves[i][0], middleMoves[i][1],colour,BOXSZ,ANGLE)
            endSearch = 0
        else:
            endSearch = 0

# after the searchPossibleMoves function calculates the player's current pieces, their possible moves
# are then calculated below. for each of the current player's pieces on the board, all directions are
# searched until either a valid move is reached, or an indicator that the direction will never hold a
# valid move is reached. if a valid move is found, the coordinates are returned in a tuple.
def calcPossibleMoves(x, y, direction1, direction2, endSearch):
    while endSearch != 0:
        newX = x + direction1
        newY = y + direction2
        stringPos = returnStringPosition(newX,newY)
        if newX < 0 or newY < 0 or newX > 7 or newY > 7:
            return (-1, -1)
            endSearch = 0
        elif gameState[stringPos] != "o" and gameState[stringPos] != playerTurn:
            endSearch = 2
            (newCoord1, newCoord2) = calcPossibleMoves(newX, newY, direction1, direction2, endSearch)
            endSearch = 0
            return (newCoord1, newCoord2)
        elif gameState[stringPos] == "o" and endSearch == 2:
            return (newX, newY)
            endSearch = 0
        elif gameState[stringPos] == "o":
            return (-1, -1)
            endSearch = 0
        else:
            return (-1, -1)
            endSearch = 0

# searches the gameState list for values matching the current player's colour. for each piece that is
# found, the calcPossibleMoves function is called for all directions and if the return value is not
# (-1,-1), which signifies no valid moves for that direction, then the values are appeneded to the
# potMoves list, which is returned by the function.
def searchPossibleMoves():
    potMoves = []
    for i in range(8):
        for x in [0,1,2,3,4,5,6,7]:
            stringPos = returnStringPosition(i,x)
            if gameState[stringPos] == playerTurn:
                for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]: # numbers in list represent all possible directions
                    (gridX, gridY) = calcPossibleMoves(i, x, direction1, direction2, 1)
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
    elif totalBlack > totalWhite:
        print("The black player wins!")
    else:
        print("The white player wins!")

# search gameState for parameter, and everytime player is found, update total. when finished searching
# the list, return the total.
def calcWinner(player):
    if player == "white":
        piece = "w"
    else:
        piece = "b"
    totalPieces = gameState.count(piece)
    return totalPieces

def userClickProcess(x,y):
    if playerTurn == COLORNAME1:
        colour = COLOR1
    else:
        colour = COLOR2
    gridX = int(x // 40)
    gridY = -(int(y // 40)) - 1
    if (0 <= gridX <= 7) and (0 <= gridY <= 7):
        userMove(colour, gridX, gridY)
    elif gridX == -2 and gridY == -2:
        sys.exit()

def computerMove():
    # to allow player turn to be swapped
    global playerTurn
    if playerTurn == COLORNAME1:
        colour = COLOR1
    else:
        colour = COLOR2

    middleMoves = []
    possibleMoves = searchPossibleMoves()
    (gridX,gridY) = bestMoveCalc(possibleMoves, playerTurn, colour)
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
        for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]: # numbers in list represent all possible directions
            middleMoves[:] = []
            fillMoves(gridX, gridY, direction1, direction2, 1, middleMoves, colour, False)

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
        for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]: # numbers in list represent all possible directions
            middleMoves[:] = []
            fillMoves(gridX, gridY, direction1, direction2, 1, middleMoves, colour, False)

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
# an "o" represents a blank position - all blank to start
gameState = "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
playerTurn = COLORNAME1

# call main function to start the game
main()
# exit on click, not mainloop, because the program isn't clicky yet
wn.mainloop()
