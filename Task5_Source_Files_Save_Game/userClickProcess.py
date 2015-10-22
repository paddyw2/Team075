"""
Team 075: Yang Li, Chi Nguyen, Patrick Withams, Greg Young
This program creates a Reversi game using Turtle Graphics
"""

import turtle as tt
import sys

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

def drawSquare(length, turn, color, turtle):
    turtle.color(color)
    turtle.begin_fill()
    for i in range(4):
        turtle.fd(length)
        turtle.rt(turn)
    turtle.end_fill()

def drawGrid(LINES, ANGLE, BOXSZ, WIDTH):
    BGCOL = '#64A23E'
    LNCOL = 'white'

    drawSquare(WIDTH,ANGLE,BGCOL, board)
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

def drawPiece(coordx, coordy, color, BOXSZ, ANGLE):
    piece.pu()
    piece.home()
    coordx = coordx * BOXSZ
    coordy = coordy * BOXSZ
    piece.goto(coordx+2, -(coordy+2))
    drawSquare(BOXSZ-4, ANGLE, color, piece)

def drawQuit():
    color = "#e7e7e7"
    length = 30
    turn = 90
    board.pu()
    board.home()
    board.goto(-70, 70)
    board.color(color)
    board.begin_fill()
    for i in range(4):
        board.fd(length)
        board.rt(turn)
    board.end_fill()
    
def setup(LINES, ANGLE, BOXSZ, WIDTH, COLOR1, COLOR2):
    drawGrid(LINES,ANGLE,BOXSZ,WIDTH)
    drawPiece(3,4,COLOR1,BOXSZ,ANGLE)
    drawPiece(4,4,COLOR2,BOXSZ,ANGLE)
    drawPiece(4,3,COLOR1,BOXSZ,ANGLE)
    drawPiece(3,3,COLOR2,BOXSZ,ANGLE)
    drawQuit()


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

def fillMoves(x, y, direction1, direction2, end_search, middleMoves, colour):
    while end_search != 0:
        newx = x + direction1
        newy = y + direction2
        if newx < 0 or newy < 0 or newx > 7 or newy > 7:
            end_search = 0
        elif gameState[newx][newy] != "blank" and gameState[newx][newy] != playerTurn:
            end_search = 2
            middleMoves.append([newx, newy])
            fillMoves(newx, newy, direction1, direction2, end_search, middleMoves, colour)
            end_search = 0
        elif gameState[newx][newy] == playerTurn and end_search == 2:
            print("Time to colour!")
            for i in range(len(middleMoves)):
                gameState[(middleMoves[i][0])][(middleMoves[i][1])] = playerTurn
                drawPiece(middleMoves[i][0], middleMoves[i][1],colour,BOXSZ,ANGLE)               
            end_search = 0
        else:
            end_search = 0

def calcPossibleMoves(x, y, direction1, direction2, endSearch):
    while endSearch != 0:
        newX = x + direction1
        newY = y + direction2
        if newX < 0 or newY < 0 or newX > 7 or newY > 7:
            print("Off grid")
            return (-1, -1)
            endSearch = 0
        elif gameState[newX][newY] != "blank" and gameState[newX][newY] != playerTurn:
            endSearch = 2
            print("Looking further!")
            (newCoord1, newCoord2) = calcPossibleMoves(newX, newY, direction1, direction2, endSearch)
            endSearch = 0
            return (newCoord1, newCoord2)
        elif gameState[newX][newY] == "blank" and endSearch == 2:
            print("Move found!")
            return (newX, newY)
            endSearch = 0
        elif gameState[newX][newY] == "blank":
            print("Blaaaaaaaaaaaank!")
            print(playerTurn)
            print(newX, newY)
            return (-1, -1)
            endSearch = 0
        else:
            print("Another possibilty, maybe error.")
            return (-1, -1)
            endSearch = 0
            
def searchPossibleMoves():
    potMoves = []
    for i in range(8):
        for x in [0,1,2,3,4,5,6,7]:
            if gameState[i][x] == playerTurn:
                print("Current pieces:", i, x)
                for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                    (coordX, coordY) = calcPossibleMoves(i, x, direction1, direction2, 1)
                    # check that it returns a number
                    if coordX >= 0:
                        potMoves.append([coordX, coordY])
    return potMoves
    
def playerSwap(colour):
    if colour == COLOR1:
        return COLORNAME2
    else:
        return COLORNAME1

def userClickProcess(x,y):
    if playerTurn == COLORNAME1:
        colour = COLOR1
    else:
        colour = COLOR2
    coordx = int(x // 40)
    coordy = int(y // 40)
    coordy = (coordy - coordy) - (coordy + 1)
    if coordx == -2 and coordy == -2:
        sys.exit()
    else:
        userMove(coordx, coordy, colour)
    
def userMove(coordx, coordy, colour):
     # to allow player turn to be swapped
    global playerTurn
    
    middleMoves = []
    possibleMoves = searchPossibleMoves()
    print(possibleMoves)
    
    validMove = False
    for i in range(len(possibleMoves)):
        if possibleMoves[i][0] == coordx and possibleMoves[i][1] == coordy:
            validMove = True
    if validMove is True:
        gameState[coordx][coordy] = playerTurn
        drawPiece(coordx,coordy, colour, BOXSZ, ANGLE)
        for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            middleMoves[:] = []
            fillMoves(coordx, coordy, direction1, direction2, 1, middleMoves, colour)
        
        # check whether next player can go
        playerTurn = playerSwap(colour)
        nextPossibleMoves = searchPossibleMoves()
        if len(nextPossibleMoves) == 0:
            playerTurn = playerSwap(colour)
            nextPossibleMoves = searchPossibleMoves()
            if len(nextPossibleMoves) == 0:
                print("Game over!")
            else:
                print("No moves for the next player! Skipping a go!")
    else:
         print("Not a valid move!")

def main():
    wn.onclick(userClickProcess)

# global variables

wn = tt.Screen()
wn.setup(startx=0,starty=0)
wn.setworldcoordinates(-60,-400,400,60)
wn.bgcolor("#228B22")
board = tt.Turtle()
piece = tt.Turtle()
board.speed('fastest')
piece.speed('fastest')
board.ht()
piece.ht()

LINES = 9
ANGLE = 90
BOXSZ = 40
WIDTH = (LINES - 1) * BOXSZ
COLOR1 = '#333'
COLOR2 = '#fff'
COLORNAME1 = "black"
COLORNAME2 = "white"

## the important global variables ##

gameState = createGameState()
playerTurn = COLORNAME1

###############

setup(LINES, ANGLE, BOXSZ, WIDTH, COLOR1, COLOR2)

main()
wn.mainloop()