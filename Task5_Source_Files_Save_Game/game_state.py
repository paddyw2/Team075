import turtle as tt
import sys
import random

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

def randomPlayer():
    headstails = random.randrange(1, 3)
    if headstails != 1:
        user_colour = "black"
    else:
        user_colour = "white"
    print(user_colour)
    return user_colour

def loadDrawGameState():
    for i in range(8):
        for x in [0,1,2,3,4,5,6,7]:
            if game_state[i][x] == "white":
                drawPiece(i,x,"#fff",BOXSZ,ANGLE)
            elif game_state[i][x] == "black":
                drawPiece(i,x,"#333",BOXSZ,ANGLE)
            else:
                print("Blank position, no plot needed.")

def loadGameState():
    global player_turn
    global user
    outfile = open("gamestate.txt", "r")
    for line in outfile:
        each_line = line.split()
        if len(each_line) > 2:
            game_state.append(each_line)
        else:
            if len(each_line) > 1:
                player_turn = each_line[0]
                user = each_line[1]
    outfile.close()

def resetGameState():
    global user
    piece.clear()
    game_state[:] = []
    outfile = open("starting_positions.txt", "r")
    for line in outfile:
        each_line = line.split()
        game_state.append(each_line)
    outfile.close()
    empty_player_turn = ""
    empty_user = ""
    saveGame(game_state, empty_player_turn, empty_user)
    loadDrawGameState()
    user = randomPlayer()
    main(player_turn)

def saveGame(game_state_array, player_turn, user):
    outfile = open("gamestate.txt", "w")
    for i in range(len(game_state_array)):
        array_string = " ".join(game_state_array[i])
        outfile.write(array_string + "\n")
    outfile.write(player_turn+" "+user)
    outfile.close()

def quitGame():
    sys.exit()

def quitKey():
    quitGame()
    
def saveKey():
    print("This function will save the game state to file.")
    saveGame(game_state, player_turn, user)
    
def endGame():
    total_white = calcTotal("white")
    total_black = calcTotal("black")
    print("Black: ", total_black)
    print("White: ", total_white)
    if max(total_black, total_white) == total_black:
        print("The black player_turn wins!")
    elif max(total_black, total_white) == total_white:
        print("The white player_turn wins!")
    else:
        print("It was a draw!")
    print("Press 'q' at any time to quit the game, or press 'n' to start a new game.")
    
def calcTotal(player_turn):
    total_pieces = 0
    for i in range(8):
        for x in [0,1,2,3,4,5,6,7]:
            if game_state[i][x] == player_turn:
                total_pieces = total_pieces + 1
    return total_pieces
            
def bestMoveCalc(pos_moves, player_turn, colour):
    total_moves = 0
    middle_moves = []
    total_array = []
    for x,y in pos_moves:
        total_array[:] = []
        middle_moves[:] = []
        for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            middle_moves[:] = []
            print("Searching...")
            fillMoves(x,y,player_turn, direction1, direction2, 1, middle_moves, colour, True)
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
            coordx = x
            coordy = y
    return (x,y)
            
def fillMoves(x, y, player_turn, direction1, direction2, end_search, middle_moves, colour, best_move):
    while end_search != 0:
        newx = x + direction1
        newy = y + direction2
        if newx < 0 or newy < 0 or newx > 7 or newy > 7:
            return -1
            end_search = 0
        elif game_state[newx][newy] != "blank" and game_state[newx][newy] != player_turn:
            end_search = 2
            middle_moves.append([newx, newy])
            fillMoves(newx, newy, player_turn, direction1, direction2, end_search, middle_moves, colour, best_move)
            end_search = 0
        elif game_state[newx][newy] == player_turn and end_search == 2:
            if best_move == True:
                print("Just looking for the best move!")
            else:
                print("Time to colour!")
                for i in range(len(middle_moves)):
                    game_state[(middle_moves[i][0])][(middle_moves[i][1])] = player_turn
                    drawPiece(middle_moves[i][0],middle_moves[i][1],colour,BOXSZ,ANGLE)   
            end_search = 0
        else:
            end_search = 0

def possibleMoves(x, y, player_turn, direction1, direction2, end_search):
    while end_search != 0:
        newx = x + direction1
        newy = y + direction2
        if newx < 0 or newy < 0 or newx > 7 or newy > 7:
            return (-1, -1)
            end_search = 0
        elif game_state[newx][newy] != "blank" and game_state[newx][newy] != player_turn:
            end_search = 2
            (new_coord1, new_coord2) = possibleMoves(newx, newy, player_turn, direction1, direction2, end_search)
            end_search = 0
            return (new_coord1, new_coord2)
        elif game_state[newx][newy] == "blank" and end_search == 2:
            return (newx, newy)
            end_search = 0
        else:
            return (-1, -1)
            end_search = 0
    
def searchFunction(player_turn, game_state):
    pot_moves = []
    pot_moves[:] = []
    for i in range(8):
        for x in [0,1,2,3,4,5,6,7]:
            if game_state[i][x] == player_turn:
                print("Current pieces:", i, x)
                for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                    (coord_x, coord_y) = possibleMoves(i, x, player_turn, direction1, direction2, 1)
                    if coord_x >= 0:
                        pot_moves.append([coord_x, coord_y])
    print("Potential moves: ", pot_moves)
    return pot_moves

def userMove(x, y, player_turn, colour, opp_player_turn):
    global remain_moves
    middle_moves = []
    coordx = int(x // 40)
    coordy = int(y // 40)
    coordy = (coordy - coordy) - (coordy + 1)
    pot_moves = searchFunction(player_turn, game_state)
    if len(pot_moves) > 0:
        choice = False
        for i in range(len(pot_moves)):
            if pot_moves[i][0] == coordx and pot_moves[i][1] == coordy:
                choice = True
        if choice == True:
            game_state[coordx][coordy] = player_turn
            drawPiece(coordx, coordy, colour,BOXSZ, ANGLE)
            for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                middle_moves[:] = []
                fillMoves(coordx, coordy, player_turn, direction1, direction2, 1, middle_moves, colour, False)  
            player_turn = opp_player_turn
        else:
            print("Not a valid move! Try again!")

        main(player_turn)
    else:
        if remain_moves == 1:
            remain_moves = 2
            print("No moves! You miss a go!")
            player_turn = opp_player_turn
            main(player_turn)
        else:
            print("Neither player_turn can go! Game over!")
            endGame()
    
def computerMove(player_turn, colour, opp_player_turn):
    global remain_moves
    middle_moves = []
    potent_moves = searchFunction(player_turn, game_state)
    if len(potent_moves) > 0:
        moves_array = []
        total_moves = 0
        (coordx,coordy) = bestMoveCalc(potent_moves, player_turn, colour)
        game_state[coordx][coordy] = player_turn
        drawPiece(coordx, coordy, colour,BOXSZ, ANGLE)
        for direction1, direction2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            middle_moves[:] = []
            fillMoves(coordx, coordy, player_turn, direction1, direction2, 1, middle_moves, colour, False)  
        player_turn = opp_player_turn
        main(player_turn)
    else:
        if remain_moves == 1:
            remain_moves = 2
            print("No moves! You miss a go!")
            player_turn = "black"
            main(player_turn)
        else:
            print("Neither player_turn can go! Game over!")
            endGame()
            
def coordBlack(x,y):
    userMove(x, y, "black", "#333", "white")
    
def coordWhite(x,y):
    userMove(x, y, "white", "#fff", "black")
    
def main(player_turn):
    if user == "white":
        if player_turn == "black":
            print("BLACK player_turn __________________ !")
            computerMove("black", "#333", "white")
        else:
            print("WHITE player_turn __________________ !")
            wn.onclick(coordWhite)
    else:
        
        if player_turn == "black":
            print("BLACK player_turn __________________ !")
            wn.onclick(coordBlack)
        else:
            print("WHITE player_turn __________________ !")
            computerMove("white", "#fff", "black")
            
    wn.onkey(quitKey, "q")
    wn.onkey(saveKey, "s")
    wn.onkey(resetGameState, "n")
    wn.listen()

# global variables

wn = tt.Screen()
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
COLOR1 = ('#333')
COLOR2 = ('#fff')

drawGrid(LINES,ANGLE,BOXSZ,WIDTH)

game_state = []

player_turn = "black"
remain_moves = 1

user = randomPlayer()
loadGameState()
loadDrawGameState()

main(player_turn)
wn.mainloop()