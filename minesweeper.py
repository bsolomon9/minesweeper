import pygame,random,itertools

#parameters for how big the board is (square) and how many mines are on it
SIZE = 25
MINES = 50

#initializes pygame and the window itself
pygame.init()
win =  pygame.display.set_mode((SIZE*16, SIZE*16))
pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])
clock = pygame.time.Clock()

#generates the board
def generate(minecount,gamesize):
    #initializing the finished list and the list of mines
    new = [[0 for i in range(SIZE)] for x in range(SIZE)]
    minelist = [[random.randint(0,SIZE-1),random.randint(0, SIZE-1)] for i in range(minecount)]
    
    #filtering out duplicate mines
    mines = [i for n, i in enumerate(minelist) if i not in minelist[n]]

    #adding mines to the board and doing the numbers
    for mine in mines:
        new[mine[0]][mine[1]] = 9
        for neighbour in neighbours_of(mine,gamesize):
            if new[neighbour[0]][neighbour[1]] != 9:
                #dumb way of doing it but the better way just refused to work and this one wants to be reasonable with me
                new[neighbour[0]][neighbour[1]] = sum([1 for tile in neighbours_of([neighbour[0],neighbour[1]],gamesize) if new[tile[0]][tile[1]] == 9])
    
    return new

#get the neighbour of a given tile
def neighbours_of(cell,size):
    for c in itertools.product(*(range(n-1, n+2) for n in cell)):
        if c != cell and all(0 <= n < size for n in c):
            yield c

#reveals a given tile
def reveal(pboard,board,mx,my,size,sprite_translate,window):
    square = board[mx][my]

    #recursively reveals every neighbouring 0
    if square == 0:
        pboard[mx][my] = 0
        for neighbour in neighbours_of([mx,my],size):
            if pboard[neighbour[0]][neighbour[1]] == 10 and board[neighbour[0]][neighbour[1]] != 9:
                drawtile(pboard,window,sprite_translate,neighbour)
                pboard = reveal(pboard,board,neighbour[0],neighbour[1],size,sprite_translate,window)

    else: pboard[mx][my] = square
    drawtile(pboard,window,sprite_translate,[mx,my])
    return pboard

#draws the whole board (one time use)
def drawboard(pboard,sprite_translate,window):
    for y, row in enumerate(pboard):
        for x in range(len(row)):
            window.blit(sprite_translate[pboard[x][y]],[x*16,y*16])
    pygame.display.flip()

#draws an individual tile
def drawtile(pboard,window,sprite_translate,tile):
    window.blit(sprite_translate[pboard[tile[0]][tile[1]]],[tile[0]*16,tile[1]*16])

#gets where the mouse is in terms of tile
def get_mousepos(position,size):
    #find the row its in
    for y, row in enumerate(playerboard):
        if pygame.Rect(0,y*16,size*16,16).collidepoint(position):

            #finds the exact tile in that row
            for i in range(len(row)):
                if pygame.Rect(i*16,y*16,16,16).collidepoint(position):
                    return[i,y]

#loads all the sprites (up tp the number 6)
unknown = pygame.image.load(r"minesweepersprites\minesweeper_unknown.png").convert()
zero = pygame.image.load(r"minesweepersprites\minesweeper0.png").convert()
one = pygame.image.load(r"minesweepersprites\minesweeper1.png").convert()
two = pygame.image.load(r"minesweepersprites\minesweeper2.png").convert()
three = pygame.image.load(r"minesweepersprites\minesweeper3.png").convert()
four = pygame.image.load(r"minesweepersprites\minesweeper4.png").convert()
five = pygame.image.load(r"minesweepersprites\minesweeper5.png").convert()
six = pygame.image.load(r"minesweepersprites\minesweeper6.png").convert()
mine = pygame.image.load(r"minesweepersprites\minesweeper_mine.png").convert()
flag = pygame.image.load(r"minesweepersprites\minesweeper_flag.png").convert()

#translates the numbers on the boards into sprites for drawing to the screen
sprite_translator = {
    0:zero,
    1:one,
    2:two,
    3:three,
    4:four,
    5:five,
    6:six,
    9:mine,
    10:unknown,
    11:flag
}

#initializes the player board (what the player sees)
playerboard = [[10 for i in range(SIZE)] for x in range(SIZE)]

#initializes the board with everything shown
board = generate(MINES,SIZE)

drawboard(playerboard,sprite_translator,win)

#main loop (infinite)
run = True
while run:
    clock.tick(10)
    #manage events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        #triggers if the a mouse button is pressesd
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            sqr = get_mousepos(pos,SIZE)
            mx = sqr[0]
            my = sqr[1]

            #left click(reveal)
            if event.button == 1:
                if board[mx][my] == 9:
                    print('BOOM')
                    run = False
                else:
                    reveal(playerboard, board, mx, my, SIZE,sprite_translator,win)
                    pygame.display.flip()
                    if str(playerboard).replace('11','9').replace('10','9') == str(board):
                        print("You have cleared the board")
                        run = False

            #right click (flag)
            elif event.button == 3:
                if playerboard[mx][my] == 10:playerboard[mx ][my] = 11
                elif playerboard[mx][my] == 11:playerboard[mx][my] = 10
                drawtile(playerboard,win,sprite_translator,[mx,my])
                pygame.display.flip()

                if str(playerboard).replace('11','9').replace('10','9') == str(board):
                    print("You have cleared the board")
                    run = False

            #middle click (reveals all the neighbours of the block clicked)
            elif event.button == 2:
                if playerboard[mx][my] != 10 and playerboard[mx][my] != 11 and playerboard[mx][my] != 0:
                    for neighbour in neighbours_of([mx,my],SIZE):
                        if playerboard[neighbour[0]][neighbour[1]] == 10:
                            if board[neighbour[0]][neighbour[1]] == 9:
                                print('BOOM')
                                run = False
                            reveal(playerboard, board, neighbour[0], neighbour[1],SIZE,sprite_translator,win)
            pygame.display.flip()

            if str(playerboard).replace('11','9').replace('10','9') == str(board):
                print("You have cleared the board")
                run = False