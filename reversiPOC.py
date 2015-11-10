import turtle as tt
from random import randrange
from sys import exit
import time
import os

def openScreen():
    userIn = wn.numinput('REVERSI','WELCOME TO REVERSI!\nEnter 1 to start a new game\nEnter 2 to load a game\nClick Cancel to quit',1,1,2)
    if userIn == None:
        exit()
    else:
        return int(userIn)

def loadGame():
    gamesList=[]
    cwd=os.getcwd()
    savedDir = os.path.join(cwd,'savedGames')
    for file in os.listdir(savedDir):
        if file.endswith('.reversi'):
            gamesList.append(file)
    text = ''
    for i in range(len(gamesList)):
        text = text+'\n'+str(i+1)+': '+str(os.path.splitext(gamesList[i])[0])
    userIn = (wn.numinput('Load Game','Enter number of a saved game. Cancel to quit.'+text,None,1,len(gamesList)))
    if userIn == None:
        openScreen()
    else:
        userIn = int(userIn)
        inFile = os.path.join(savedDir,gamesList[userIn-1])
        with open(inFile, "r") as game:
            lines = game.readlines()
            newGameState = []
            for i in range(len(lines)):
                if i < 8:
                    row = list(lines[i].strip('\n'))
                    newGameState.append(row)
                elif i == 8:
                    lastLine = lines[i].strip()
        global gameState,playerTurn,userColor
        colorDict = {'COLOR1':COLOR1,'COLOR2':COLOR2}
        gameState=newGameState
        playerTurn = colorDict[lastLine]
        userColor = colorDict[lastLine]
        setup()

def rules(turt):
    return

def setup():
    aroundBoard(board)
    drawPiece()

def drawBoard(turt):
    turt.pu()
    turt.goto(80,80)
    drawQuad(BRDSZ,BRDSZ,BGCOL,turt)
    drawLines(turt)
    turt.goto(400,80)
    turt.lt(ANGLE)
    drawLines(turt)

def aroundBoard(turt):
    turt.goto(242,62)
    turt.color('black')
    turt.pd()
    turt.write('*  R  E  V  E  R  S  I *', align='center', font=('',40,'bold'))
    turt.pu()
    turt.goto(240,60)
    turt.color('white')
    turt.pd()
    turt.write('*  R  E  V  E  R  S  I *', align='center', font=('',40,'bold'))
    turt.pu()
    turt.goto(120,450)
    turt.seth(270)
    drawQuad(20,80,'#CCC',turt,True)
    turt.goto(160,447)
    turt.write('EXIT GAME', align='center', font=('',14))
    turt.goto(280,450)
    turt.seth(270)
    drawQuad(20,80,'#CCC',turt,True)
    turt.goto(320,447)
    turt.write('SAVE GAME', align='center', font=('',14))

def drawQuad(length,width,color,turt,depth=False):
    if depth == False:
        turt.pd()
        turt.color(color)
        turt.begin_fill()
        for i in range(2):
            turt.fd(width)
            turt.lt(90)
            turt.fd(length)
            turt.lt(90)
        turt.end_fill()
        turt.pu()
    else:
        turt.pd()
        turt.color('black', color)
        turt.begin_fill()
        turt.pensize(1)
        turt.fd(length)
        turt.lt(90)
        turt.fd(width)
        turt.lt(90)
        turt.pensize(3)
        turt.fd(length)
        turt.lt(90)
        turt.fd(width)
        turt.lt(90)
        turt.end_fill()
        turt.pu()

def drawLines(turt):
    for i in range(LINES):
        turt.color(LNCOL)
        turt.pd()
        turt.fd(BRDSZ)
        turt.pu()
        turt.fd(-BRDSZ)
        turt.lt(ANGLE)
        turt.fd(BOXSZ)
        turt.lt(-ANGLE)

def drawPiece():
    for y in range(len(gameState)):
        for x in range(len(gameState[y])):
            if gameState[y][x] == 'B':
                color = COLOR1
                coordX = x * BOXSZ + 80
                coordY = y * BOXSZ + 80
                piece.goto(coordX+2,coordY+2)
                drawQuad(BOXSZ-4,BOXSZ-4,color,piece)
            elif gameState[y][x] == 'W':
                color = COLOR2
                coordX = x * BOXSZ + 80
                coordY = y * BOXSZ + 80
                piece.goto(coordX+2,coordY+2)
                drawQuad(BOXSZ-4,BOXSZ-4,color,piece)
    scorekeeper()

def scorekeeper():
    blkPc = 0
    whtPc = 0
    for i in range(len(gameState)):
        for j in range(len(gameState[i])):
            if gameState[i][j] == 'B':
                blkPc += 1
            if gameState[i][j] == 'W':
                whtPc += 1
    blkScor.clear()
    blkScor.goto(40,110)
    blkScor.write(str(blkPc), align='center', font=('',22,'bold'))
    whtScor.clear()
    whtScor.goto(440,110)
    whtScor.write(str(whtPc), align='center', font=('',22,'bold'))

def chooseRandomColour():
    headstails = randrange(0,2)
    if headstails == 1:
        user = COLOR1
    else:
        user = COLOR2
    return user

def saveGame():
    saveName = str(wn.textinput('Save Game','Name of game:')) + '.reversi'
    cwd=os.getcwd()
    outFile = os.path.join(cwd,'savedGames',saveName)
    colorDict = {COLOR1:'COLOR1',COLOR2:'COLOR2'}
    with open(outFile,'w') as gameFile:
        gameFile.writelines(''.join(str(j) for j in i) + '\n' for i in gameState)
        gameFile.write(colorDict[userColor])

def userClickInput(x,y):
    if (80 <= x <= 400) and (80 <= y <= 400):
        userMove(x,y,playerTurn)
    elif (280 <= x <= 360) and (430 <= y <=450):
        saveGame()
    elif (120 <= x <= 200) and (430 <= y <=450):
        exit()

def updateGameState(turn,gridX,gridY):
    global gameState
    if turn == COLOR1:
        playerValue = 'B'
    elif turn == COLOR2:
        playerValue = 'W'
    gameState[gridY][gridX] = playerValue

def fillMoves(x,y,direct1,direct2,endSearch,middleMoves,turn,bestMove):
    if turn == COLOR1:
        playerValue = 'B'
    elif turn == COLOR2:
        playerValue = 'W'
    while endSearch != 0:
        newX = x + direct1
        newY = y + direct2
        gameStateValue = returnGameStateValue(newX,newY)
        if newX < 0 or newY < 0 or newX > 7 or newY > 7:
            endSearch = 0
        elif gameStateValue != "O" and gameStateValue != playerValue:
            endSearch = 2
            middleMoves.append([newX, newY])
            fillMoves(newX,newY,direct1,direct2,endSearch,middleMoves,turn,bestMove)
            endSearch = 0
        elif gameStateValue == playerValue and endSearch == 2:
            if bestMove == False:
                for i in range(len(middleMoves)):
                    updateGameState(turn,middleMoves[i][0],middleMoves[i][1])
                    drawPiece()
            endSearch = 0
        else:
            endSearch = 0

def playerSwap(colour):
    if colour == COLOR1:
        return COLOR2
    else:
        return COLOR1

def bestMoveCalc(validList,turn):
    totalMoves = 0
    middleMoves = []
    totalList = []
    for x,y in validList:
        totalList[:] = []
        middleMoves[:] = []
        for direct1,direct2 in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
            middleMoves[:] = []
            fillMoves(x,y,direct1,direct2,1,middleMoves,turn,True)
            if len(middleMoves) > 0:
                for i in range(len(middleMoves)):
                    first = middleMoves[i][0]
                    second = middleMoves[i][1]
                    totalList.append([first,second])
        newList = []
        newList[:] = []
        for i in range(len(totalList)):
            num1 = totalList[i][0]
            num2 = totalList[i][1]
            newList.append(str(num1)+str(num2))
        tempList = set(newList)
        tempList = list(tempList)
        if len(tempList) > totalMoves:
            totalMoves = len(tempList)
            gridX = x
            gridY = y
    return (gridX,gridY)

def computerMove(turn):
    time.sleep(0.5)
    global playerTurn
    middleMoves = []
    validMove = False
    validList = findPieces(turn)
    (gridX,gridY) = bestMoveCalc(validList,turn)
    for i in range(len(validList)):
        if gridX == validList[i][0] and gridY == validList[i][1]:
            validMove = True
    if validMove == True:
        updateGameState(turn,gridX,gridY)
        drawPiece()
        for direct1, direct2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            middleMoves[:] = []
            fillMoves(gridX,gridY,direct1,direct2,1,middleMoves,turn, False)
        playerTurn = playerSwap(turn)
        nextPossMoves = findPieces(playerTurn)
        if len(nextPossMoves) == 0:
            playerTurn = playerSwap(playerTurn)
            nextPossMoves = findPieces(playerTurn)
            if len(nextPossMoves) == 0:
                gameOver()
            else:
                computerMove(playerTurn)

def userMove(x,y,turn):
    middleMoves = []
    global playerTurn
    validList = findPieces(turn)
    validMove = False
    gridX = int(x//40 - 2)
    gridY = int(y//40 - 2)
    for i in range(len(validList)):
        if gridX == validList[i][0] and gridY == validList[i][1]:
            validMove = True
    if validMove == True:
        updateGameState(turn,gridX,gridY)
        drawPiece()
        for direct1,direct2 in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
            middleMoves[:] = []
            fillMoves(gridX,gridY,direct1,direct2,1,middleMoves,turn,False)
        playerTurn = playerSwap(turn)
        nextPossMoves = findPieces(playerTurn)
        if len(nextPossMoves) == 0:
            playerTurn = playerSwap(playerTurn)
            nextPossMoves = findPieces(playerTurn)
            if len(nextPossMoves) == 0:
                gameOver()
        else:
            computerMove(playerTurn)

def findPieces(turn):
    possMoves = []
    if turn == COLOR1:
        gameStateValue = 'B'
    elif turn == COLOR2:
        gameStateValue = 'W'
    for y in range(8):
        for x in range(8):
            if gameState[y][x] == gameStateValue:
                for direct1, direct2 in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                    (gridX,gridY) = findPossibleMoves(y,x,direct1,direct2,gameStateValue,1)
                    if gridY >= 0:
                        possMoves.append([gridX,gridY])
    return possMoves

def findPossibleMoves(gridY,gridX,direct1,direct2,turn,endSearch):
    while endSearch != 0:
        playerTurn = turn
        newX = gridX + direct1
        newY = gridY + direct2
        gameStateValue = returnGameStateValue(newX,newY)
        if newX < 0 or newX > 7 or newY < 0 or newY > 7:
            endSearch = 0
            return(-1,-1)
        elif gameStateValue != "O" and gameStateValue != playerTurn:
            endSearch = 2
            (nextX, nextY) = findPossibleMoves(newY,newX,direct1,direct2,playerTurn,endSearch)
            endSearch = 0
            return (nextX, nextY)
        elif gameStateValue == "O" and endSearch == 2:
            return (newX, newY)
            endSearch = 0
        elif gameStateValue == "O":
            return (-1, -1)
            endSearch = 0
        else:
            return (-1, -1)
            endSearch = 0

def returnGameStateValue(x,y):
    if x < 0 or y < 0 or x > 7 or y > 7:
    	gameStateValue = -1
    else:
    	gameStateValue = gameState[y][x]
    return gameStateValue

def finalScore():
    blkPc = 0
    whtPc = 0
    for i in range(len(gameState)):
        for j in range(len(gameState[i])):
            if gameState[i][j] == 'B':
                blkPc += 1
            if gameState[i][j] == 'W':
                whtPc += 1
    return blkPc, whtPc

def gameOver():
    score1, score2 = finalScore()
    blkScor.clear()
    whtScor.clear()
    piece.clear()
    board.clear()
    if (userColor == COLOR1 and score1 > score2) or (userColor == COLOR2 and score1 < score2):
        bgdir = os.path.join(os.getcwd(),'img')
        bgpic = os.path.join(bgdir,'win.gif')
        wn.setworldcoordinates(-400,-400,400,400)
        wn.bgpic(bgpic)
    elif (userColor == COLOR1 and score1 < score2) or (userColor == COLOR2 and score1 > score2):
        bgdir = os.path.join(os.getcwd(),'img')
        bgpic = os.path.join(bgdir,'lose.gif')
        wn.bgpic(bgpic)

def main():
    drawBoard(board)
    userIn = openScreen()
    if userIn == 1:
        setup()
        global userColor
        userColor = chooseRandomColour()
    elif userIn == 2:
        loadGame()
    if userColor != playerTurn:
        time.sleep(1)
        computerMove(playerTurn)
    wn.onclick(userClickInput)

LINES = 9
ANGLE = 90
BOXSZ = 40
BRDSZ = (LINES - 1) * BOXSZ
BGCOL = '#228B22'
LNCOL = '#AAA'
COLOR1 = '#000'
COLOR2 = '#FFF'

wn = tt.Screen()
wn.setup(startx=None,starty=None)
wn.screensize(BOXSZ*12,BOXSZ*12)
wn.setworldcoordinates(0,BOXSZ*12,BOXSZ*12,0)
bgdir = os.path.join(os.getcwd(),'img')
bgpic = os.path.join(bgdir,'table.gif')
wn.bgpic(bgpic)
wn.title('PYTHON REVERSI')
wn.tracer(0)

blkScor=tt.Turtle()
blkScor.ht()
blkScor.pu()
blkScor.pencolor(COLOR1)

whtScor=tt.Turtle()
whtScor.ht()
whtScor.pu()
whtScor.pencolor(COLOR2)

board=tt.Turtle()
board.ht()

piece=tt.Turtle()
piece.ht()
piece.pu()

userColor = ''
playerTurn = COLOR1
gameState = [['O','O','O','O','O','O','O','O'],
             ['O','O','O','O','O','O','O','O'],
             ['O','O','O','O','O','O','O','O'],
             ['O','O','O','W','B','O','O','O'],
             ['O','O','O','B','W','O','O','O'],
             ['O','O','O','O','O','O','O','O'],
             ['O','O','O','O','O','O','O','O'],
             ['O','O','O','O','O','O','O','O']]

main()
wn.mainloop()
