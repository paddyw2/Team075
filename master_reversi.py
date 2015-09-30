# Team 075
# Team members: Patrick, Chi, Greg, Yang

# This program creates a Reversi game using Turtle Graphics

import turtle as tt

def draw_board():
    SIDES = 9
    ANGLE = 90
    SQUARES = 40
    WIDTH = 320
    drawBoard.pendown()

    for i in range(SIDES):
        drawBoard.forward(WIDTH)
        drawBoard.penup()
        drawBoard.forward(-WIDTH)
        drawBoard.right(ANGLE)
        drawBoard.forward(SQUARES)
        drawBoard.right(-ANGLE)
        drawBoard.pendown()

    drawBoard.penup()
    drawBoard.home()
    drawBoard.pendown()

    for i in range(SIDES):
        drawBoard.right(ANGLE)
        drawBoard.forward(WIDTH)
        drawBoard.penup()
        drawBoard.forward(-WIDTH)
        drawBoard.right(-ANGLE)
        drawBoard.forward(SQUARES)
        drawBoard.pendown()

    drawBoard.penup()
    drawBoard.forward(-255)
    drawBoard.left(ANGLE)
    drawBoard.forward(20)
    drawBoard.color("#333")
    drawBoard.write("R E V E R S I", move=False, align="left", font=("Helvetica", 24, "bold"))

    drawBoard.home()
    drawBoard.forward(20)
    drawBoard.right(-ANGLE)
    drawBoard.forward(5)
    drawBoard.right(ANGLE)
    for i in range(8):
        drawBoard.write(i,font=("Helvetica",16))
        drawBoard.forward(SQUARES)

    drawBoard.home()
    drawBoard.forward(-10)
    drawBoard.right(ANGLE)
    drawBoard.forward(20)
    for i in range(8):
        drawBoard.write(i, align="center", font=("Helvetica",16))
        drawBoard.forward(SQUARES)

    #Draws the welcome message and rules under the board
    drawBoard.home()
    drawBoard.right(ANGLE)
    drawBoard.forward(350)
    drawBoard.right(-ANGLE)
    drawBoard.forward(50)
    drawBoard.write("Welcome to this amazing game of Reversi!", move=False, align="left", font=("Helvetica", 14, "normal"))

    drawBoard.home()
    drawBoard.right(ANGLE)
    drawBoard.fd(WIDTH + 75)
    drawBoard.right(-ANGLE)
    drawBoard.forward(SQUARES * 4 + 15)
    drawBoard.write("How to play: Place your marker on the grid so that you make least one straight (horizontal,\nvertical, or diagonal) line between your new marker and another of your existing marker, with\none or more markers belonging to the opponent between them. All opponents markers in the\nline are captured. A player misses their turn if there are no valid moves.",align="center", font=("Helvetica",10,"normal"))
    
def plot(coord1, coord2, colour):
    coord1 = coord1 * 40
    coord2 = coord2 * 40 + 20
    drawBoard.home()
    drawBoard.forward(coord1)
    drawBoard.right(ANGLE)
    drawBoard.forward(coord2)
    drawBoard.color(colour)
    drawBoard.begin_fill()
    drawBoard.circle(20)
    drawBoard.end_fill()

def main():
    draw_board()
    plot(3,4, "#333")
    plot(4,4, "#fff")
    plot(4,3, "#333")
    plot(3,3, "#fff")
    print("Please enter your first move.")
    coordx = int(input("Row: "))
    coordy = int(input("Column: "))
    plot(coordx,coordy, "#333")
    wn.exitonclick()

# global variables

wn = tt.Screen()
wn.setup(startx=0,starty=0)
wn.setworldcoordinates(-60,-400,400,60)
wn.bgcolor("#26A65B")
drawBoard = tt.Turtle()
drawBoard.penup()
drawBoard.speed('fastest')
drawBoard.color("white")
drawBoard.ht()

main()
