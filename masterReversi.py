"""
Team 075: Yang Li, Chi Nguyen, Patrick Withams, Greg Young
This program creates a Reversi game using Turtle Graphics
"""

import turtle as tt
import random

# draws the horizontal and diagonal lines for the game board
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

# draws any filled in rectangle or square needed, with whatever turtle is used as a parameter
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
def drawPiece(coordx, coordy, color, BOXSZ, ANGLE):
    piece.pu()
    piece.home()
    coordx = coordx * BOXSZ
    coordy = coordy * BOXSZ
    piece.goto(coordx+2, -(coordy+2))
    drawRectangle(BOXSZ-4,BOXSZ-4,ANGLE,color,piece)

# calls the drawGrid function to set board up and then draws the four starting pieces. called once
# on startup.
def setup(LINES, ANGLE, BOXSZ, WIDTH, COLOR1, COLOR2):
    print('''
    
     welcome to...
     
    R E V E R S I!
    
    ''')
    drawGrid(LINES,ANGLE,BOXSZ,WIDTH)
    drawPiece(3,4,COLOR1,BOXSZ,ANGLE)
    drawPiece(4,4,COLOR2,BOXSZ,ANGLE)
    drawPiece(4,3,COLOR1,BOXSZ,ANGLE)
    drawPiece(3,3,COLOR2,BOXSZ,ANGLE)

# creates a 2d list with 8 lists inside. then for each of these lists, the item "blank" is appended
# eight times. this then represents the game state. each list represents a row, and then each position
# in that list represents a column. so gameState[2][3] would hold the value for row 2, column 3. once
# the blank list is created the starting coordinates are updated to hold the values either "black" or
# "white".
def createGameState():
    gameState = [[],[],[],[],[],[],[],[]]
    for i in range(8):
        for x in [0,1,2,3,4,5,6,7]:
            gameState[x].append("blank")
    gameState[3][3] = COLORNAME2
    gameState[3][4] = COLORNAME1
    gameState[4][3] = COLORNAME1
    gameState[4][4] = COLORNAME2
    return gameState

# once a move has been chosen and verified to be valid, the middle moves, or moves in between, need to
# be determined and coloured. to do this, the chosen move coordinate is taken and for each possible
# direction, a search is performed backwards until either the direction is determined to be either a
# valid colouring direction or an invalid one. if it is valid, the coordinates in between the chosen move
# and the end point are coloured the current players colours.
def fillMoves(x, y, direction1, direction2, endSearch, middleMoves, colour):
    while endSearch != 0:
        newx = x + direction1
        newy = y + direction2
        if newx < 0 or newy < 0 or newx > 7 or newy > 7:
            endSearch = 0
        elif gameState[newx][newy] != "blank" and gameState[newx][newy] != playerTurn:
            endSearch = 2
            middleMoves.append([newx, newy])
            fillMoves(newx, newy, direction1, direction2, endSearch, middleMoves, colour)
            endSearch = 0
        elif gameState[newx][newy] == playerTurn and endSearch == 2:
            for i in range(len(middleMoves)):
                gameState[(middleMoves[i][0])][(middleMoves[i][1])] = playerTurn
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
        if newX < 0 or newY < 0 or newX > 7 or newY > 7:
            return (-1, -1)
            endSearch = 0
        elif gameState[newX][newY] != "blank" and gameState[newX][newY] != playerTurn:
            endSearch = 2
            (newCoord1, newCoord2) = calcPossibleMoves(newX, newY, direction1, direction2, endSearch)
            endSearch = 0
            return (newCoord1, newCoord2)
        elif gameState[newX][newY] == "blank" and endSearch == 2:
            return (newX, newY)
            endSearch = 0
        elif gameState[newX][newY] == "blank":
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
            if gameState[i][x] == playerTurn:
                for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]: # numbers in list represent all possible directions
                    (coordX, coordY) = calcPossibleMoves(i, x, direction1, direction2, 1)
                    # check that it returns a number
                    if coordX >= 0:
                        potMoves.append([coordX, coordY])
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
    totalPieces = 0
    for i in range(8):
        for x in [0,1,2,3,4,5,6,7]:
            if gameState[i][x] == player:
                totalPieces = totalPieces + 1
    return totalPieces

# function to chose automated random computer move, delete if auto option not needed
def randomCoordinates(posMoves):
    num1 = random.randrange(0,len(posMoves))
    return (posMoves[num1][0], posMoves[num1][1])

# this controls what happens when it is a player's turn. first, it calculates the possible moves
# the player has. then it takes their input for their next move. if their move matches once of the
# possible moves, then it is valid. if not, end the function without changing the player turn
# and re-enter main function loop that will call the function again, giving the user another chance.
# if it is valid, add that move to the gameState list, and then colour it the player's colour. next,
# calculate what moves now need to be filled in. finally, check whether next player can go.
def userMove(colour):
    # to allow player turn to be swapped and endGameIndicator to be updated
    global playerTurn
    global endGameIndicator
    print(playerTurn[:1].upper() + playerTurn[1:], "player's turn!") # playerTurn is converted to caps
    middleMoves = []
    possibleMoves = searchPossibleMoves()
    print("Possible moves:", possibleMoves)
    print("Please enter your chosen coordinates.")
    # this is the manual input option, uncomment and delete line 222 for manual
    coordx = int(input("Row: "))
    coordy = int(input("Column: "))
	# this is the automated computer line, uncomment for auto option
    #(coordx, coordy) = randomCoordinates(possibleMoves) # this automatically choses move
    validMove = False
    # check if chosen move is valid
    for i in range(len(possibleMoves)):
        if possibleMoves[i][0] == coordx and possibleMoves[i][1] == coordy:
            validMove = True
    if validMove is True:
        # update gameState with move and colour coordinate
        gameState[coordx][coordy] = playerTurn
        drawPiece(coordx,coordy, colour, BOXSZ, ANGLE)
        # fill in and update gameStatefor all other pieces to be coloured
        for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]: # numbers in list represent all possible directions
            middleMoves[:] = []
            fillMoves(coordx, coordy, direction1, direction2, 1, middleMoves, colour)

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
                endGameIndicator = 0
            else: # if they do have moves, then other player just misses a turn
                print("No moves for the next player! Skipping a go!")
    else:
        print("Not a valid move, try again!")
    
# calls the setup functiont to draw the board. creates a while loop that triggers the userMove
# function with the colour of the current player.
def main():
    setup(LINES, ANGLE, BOXSZ, WIDTH, COLOR1, COLOR2)
    while endGameIndicator != 0:
        if playerTurn == COLORNAME1:
            userMove(COLOR1)
        elif playerTurn == COLORNAME2:
            userMove(COLOR2)
    print("Thanks for playing!")

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
COLORNAME1 = "black"
COLORNAME2 = "white"

# global variables (not possible to make local - they need to affect everything)

gameState = createGameState()
playerTurn = COLORNAME1
endGameIndicator = 1

# call main function to start the game
main()
# exit on click, not mainloop, because the program isn't clicky yet
wn.exitonclick()