import pygame
import random

pygame.font.init()

# Global Variables
sWidth = 800
sHeight = 700
playWidth = 300
playHeight = 600
blockSize = 30

topLeftX = (sWidth - playWidth) // 2
topLeftY = sHeight - playHeight

# Shape Formats

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shapeColors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
               (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    rows = 20
    columns = 10

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shapeColors[shapes.index(shape)]
        self.rotation = 0


def createGrid(locked_pos={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def convertShapeFormat(shape):
    positions = []
    currentShape = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(currentShape):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def validSpace(shape, grid):
    acceptedPositions = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    acceptedPositions = [j for sub in acceptedPositions for j in sub]
    formatted = convertShapeFormat(shape)

    for pos in formatted:
        if pos not in acceptedPositions:
            if pos[1] > -1:
                return False
    return True


def checkLost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def getShape():
    global shapes, shapeColors
    return Piece(5, 0, random.choice(shapes))


def drawTextMiddle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    # surface.blit(label, (topLeftX + playWidth/2, topLeftY + playHeight/2))
    surface.blit(label, (topLeftX + playWidth/2 - (label.get_width()/2), topLeftY + playHeight/2 - (label.get_height()/2)))


def drawGrid(surface, row, col):
    sx = topLeftX
    sy = topLeftY

    for i in range(row):
        # Horizontal Lines
        pygame.draw.line(surface, (128, 128, 128), (sx, sy +
                                                    i*blockSize), (sx + playWidth, sy + i*blockSize))
        # Vertical Lines
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j *
                                                        blockSize, sy), (sx + j*blockSize, sy + playHeight))


def clearRows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x:x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc


def drawNextShape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))
    sx = topLeftX + playWidth + 50
    sy = topLeftY + playHeight/2 - 100
    nextShape = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(nextShape):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy - 30))

def updateScore(nscore):
    score = maxScore()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def maxScore():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score

def drawWindow(surface, grid, score=0, mScore=0):
    surface.fill((0, 0, 0))
    # Title
    font = pygame.font.SysFont("comicsans", 60)
    label = font.render("Tetris", 1, (255, 255, 255))

    surface.blit(label, (topLeftX + playWidth/2 - (label.get_width()/2), 30))

    # Score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: '+str(score), 1, (255,255,255))

    sx = topLeftX + playWidth + 50
    sy = topLeftY + playHeight/2 - 100

    surface.blit(label, (sx + 20, sy+ 160))

    # Max Score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Max Score: '+str(mScore), 1, (255,255,255))

    sx = topLeftX + playWidth + 50
    sy = topLeftY + playHeight/2 - 100

    surface.blit(label, (sx + 20, sy+ 185))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                surface, grid[i][j], (topLeftX + j*blockSize, topLeftY + i*blockSize, blockSize, blockSize), 0)

    # Draw Grid and Border
    drawGrid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (topLeftX,
                                            topLeftY, playWidth, playHeight), 5)


def main():
    global grid
    mScore = maxScore()
    lockedPosition = {}
    grid = createGrid(lockedPosition)

    changePiece = False
    run = True
    currentPiece = getShape()
    nextPiece = getShape()
    clock = pygame.time.Clock()
    fallTime = 0
    fallSpeed = 0.27
    levelTime = 0
    score = 0

    while run:
        grid = createGrid(lockedPosition)
        fallTime += clock.get_rawtime()
        levelTime += clock.get_rawtime()
        clock.tick()

        # Level speed increase
        if levelTime/1000 > 5:
            levelTime = 0
            if fallSpeed > 0.12:
                fallSpeed -= 0.005

        # Falling Piece
        if fallTime/1000 >= fallSpeed:
            fallTime = 0
            currentPiece.y += 1
            if not (validSpace(currentPiece, grid)) and currentPiece.y > 0:
                currentPiece.y -= 1
                changePiece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    currentPiece.x -= 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.x += 1
                elif event.key == pygame.K_RIGHT:
                    currentPiece.x += 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.x -= 1
                elif event.key == pygame.K_DOWN:
                    currentPiece.y += 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.y -= 1
                elif event.key == pygame.K_UP:
                    # Rotate shape
                    currentPiece.rotation += 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.rotation -= 1

        shapePos = convertShapeFormat(currentPiece)

        # add piece to the grid for drawing
        for i in range(len(shapePos)):
            x, y = shapePos[i]
            if y > -1:
                grid[y][x] = currentPiece.color

        # If piece hits ground
        if changePiece:
            for pos in shapePos:
                p = (pos[0], pos[1])
                lockedPosition[p] = currentPiece.color
            currentPiece = nextPiece
            nextPiece = getShape()
            changePiece = False
            score += clearRows(grid, lockedPosition)*10
            

        drawWindow(win, grid, score, mScore)
        drawNextShape(nextPiece, win)
        pygame.display.update()

        # Check if user lost
        if checkLost(lockedPosition):
            drawTextMiddle("You Lost", 40, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
            updateScore(score)

    
def mainMenu():
    run = True
    while run:
        win.fill((0,0,0))
        drawTextMiddle('Press any key to begin.', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.display.quit()


win = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption("Tetris")
mainMenu()
