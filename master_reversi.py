"""
Team 075: Yang Li, Chi Nguyen, Patrick Withams, Greg Young
This program creates a Reversi game using Turtle Graphics
"""

import turtle as tt

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

def drawSquare(length, turn, color):
    board.color(color)
    board.begin_fill()
    for i in range(4):
        board.fd(length)
        board.rt(turn)
    board.end_fill()

def drawGrid(LINES, ANGLE, BOXSZ, WIDTH):
    BGCOL = '#64A23E'
    LNCOL = 'white'

    drawSquare(WIDTH,ANGLE,BGCOL)
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
    board.pu()
    board.home()
    coordx = coordx * BOXSZ
    coordy = coordy * BOXSZ
    board.goto(coordx+2, -(coordy+2))
    drawSquare(BOXSZ-4, ANGLE, color)

def setup(LINES, ANGLE, BOXSZ, WIDTH, COLOR1, COLOR2):
    drawGrid(LINES,ANGLE,BOXSZ,WIDTH)
    drawPiece(3,4,COLOR1,BOXSZ,ANGLE)
    drawPiece(4,4,COLOR2,BOXSZ,ANGLE)
    drawPiece(4,3,COLOR1,BOXSZ,ANGLE)
    drawPiece(3,3,COLOR2,BOXSZ,ANGLE)

def main():
    LINES = 9
    ANGLE = 90
    BOXSZ = 40
    WIDTH = (LINES - 1) * BOXSZ
    COLOR1 = ('#333')
    COLOR2 = ('#fff')
    turn = 1

    setup(LINES, ANGLE, BOXSZ, WIDTH, COLOR1, COLOR2)

    while turn < 4:
        coordx = int(input("Row: "))
        coordy = int(input("Column: "))
        if turn//2 == 0:
            drawPiece(coordx,coordy, COLOR1, BOXSZ, ANGLE)
        else:
            drawPiece(coordx,coordy, COLOR2, BOXSZ, ANGLE)
        turn += 1
    wn.exitonclick()

# global variables
wn = tt.Screen()
wn.setup(startx=0,starty=0)
wn.setworldcoordinates(-60,-400,400,60)
wn.bgcolor("#228B22")
board = tt.Turtle()
piece = tt.Turtle()
board.speed('fastest')
board.ht()
piece.ht()

main()
