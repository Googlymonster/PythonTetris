import pygame
import random

pygame.font.init()

# Global Variables
sWidth = 800
sHeight = 700
playWidth = 300
playHeight = 600
blockSize = 30

topLeftX = (sWidth - playHeight) // 2
topLeftY = sHeight - playHeight

# Shape Formats

S = [[
    '.....',
    '.....',
    '..00.',
    '.00..',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '...0.',
    '.....']]
Z = []
I = []
O = []
J = []
L = []
T = []

shapes = [S, Z, I, O, J, L, T]
shapeColors =[(0,255,0),(255,0,0),(0,255,255),(255,255,0),(255,165,0),(0,0,255),(128,0,128)]

class Piece(object):
    rows = 20
    columns = 10
    
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shapeColors[shapes.index(shape)]
        self.rotation = 0

def createGrid(locked_pos = {}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid

def convertShapeFormat():
    pass

def validSpace():
    pass

def checkLost():
    pass

def getShape():
    return Piece(5, 0, random.choice(shapes))

def drawTextMiddle():
    pass

def drawGrid(surface, grid):
    sx = topLeftX
    sy = topLeftY

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*blockSize), (sx + playWidth, sy + i*blockSize))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j*blockSize, sy), (sx + j*blockSize, sy + playHeight))            


def clearRows():
    pass

def drawNextShape():
    pass

def drawWindow(surface, grid):
    surface.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 60)
    label = font.render("Tetris", 1, (255,255,255))

    surface.blit(label, (topLeftX + playWidth/2 - (label.get_width()/2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (topLeftX + j*blockSize, topLeftY + i*blockSize, blockSize, blockSize), 0)
        
    pygame.draw.rect(surface,(255, 0, 0), (topLeftX, topLeftY, playWidth, playHeight), 4)
    drawGrid(surface, grid)
    pygame.display.update()

def main(win):
    lockedPosition = {}
    grid = createGrid(lockedPosition)
    changePiece = False
    run = True
    currentPiece = getShape()
    nextPiece = getShape()
    clock = pygame.time.Clock()
    fallTime = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    currentPiece.x -= 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece += 1
                if event.key == pygame.K_RIGHT:
                    currentPiece.x += 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece -= 1
                if event.key == pygame.K_DOWN:
                    currentPiece.y += 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.y -= 1
                if event.key == pygame.K_UP:
                    currentPiece.rotation += 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.rotation -= 1
    drawWindow(win, grid)

def mainMenu(win):
    main(win)

win = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_pation("Tetris")
mainMenu(win)