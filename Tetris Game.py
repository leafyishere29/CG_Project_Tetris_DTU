import pygame as pygame
import random

pygame.font.init()

width_s = 800
height_s = 700
width_win = 300  
height_win = 600  
size_blocks = 30

x_topleft = (width_s - width_win) // 2
y_topleft = height_s - height_win

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

S = [['.....',
      '......',
      '..00..',
      '.00...',
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
shape_colors = [(165, 0, 100), (255, 165, 0), (0, 0, 255), (255, 255, 0), (255, 0, 0), (0, 255, 255), (128, 0, 128)]

 
 
class Piece(object):
    rows = 20  
    columns = 10  
 
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0 
 
 
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid
 
 
def shape_convert(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
 
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
 
    return positions
 
 
def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = shape_convert(shape)
 
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
 
    return True
 
 
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
 
 
def get_shape():
    global shapes, shape_colors
 
    return Piece(5, 0, random.choice(shapes))
 
 
def center_text(text, size, color, surface):
    font = pygame.font.SysFont('calibri', size, bold=True)
    label = font.render(text, 1, color)
 
    surface.blit(label, (x_topleft + width_win/2 - (label.get_width() / 2), y_topleft + height_win/2 - label.get_height()/2))
 
 
def draw_grid(surface, row, col):
    sx = x_topleft
    sy = y_topleft
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + width_win, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + height_win))  # vertical lines
 
 
def row_break(grid, locked):
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
 
 
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (200,100,100))
 
    sx = x_topleft + width_win + 50
    sy = y_topleft + height_win/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
 
    surface.blit(label, (sx + 10, sy- 30))
 
 
def draw_window(surface):
    surface.fill((0,0,0))
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (100,0,255))
 
    surface.blit(label, (x_topleft + width_win / 2 - (label.get_width() / 2), 30))
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (x_topleft + j* 30, y_topleft + i * 30, 30, 30), 0)
 
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (x_topleft, y_topleft, width_win, height_win), 5)

 
 
def main():
    global grid
 
    locked_positions = {}  
    grid = create_grid(locked_positions)
 
    change_piece = False
    run = True
    cur_block = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
 
    while run:
        fall_speed = 0.27
 
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
 
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            cur_block.y += 1
            if not (valid_space(cur_block, grid)) and cur_block.y > 0:
                cur_block.y -= 1
                change_piece = True
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cur_block.x -= 1
                    if not valid_space(cur_block, grid):
                        cur_block.x += 1
 
                elif event.key == pygame.K_RIGHT:
                    cur_block.x += 1
                    if not valid_space(cur_block, grid):
                        cur_block.x -= 1
                elif event.key == pygame.K_UP:
                    cur_block.rotation = cur_block.rotation + 1 % len(cur_block.shape)
                    if not valid_space(cur_block, grid):
                        cur_block.rotation = cur_block.rotation - 1 % len(cur_block.shape)
 
                if event.key == pygame.K_DOWN:
                    cur_block.y += 1
                    if not valid_space(cur_block, grid):
                        cur_block.y -= 1
 
                if event.key == pygame.K_SPACE:
                   while valid_space(cur_block, grid):
                       cur_block.y += 1
                   cur_block.y -= 1
                   print(shape_convert(cur_block))  
 
        shape_pos = shape_convert(cur_block)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = cur_block.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = cur_block.color
            cur_block = next_piece
            next_piece = get_shape()
            change_piece = False
            row_break(grid, locked_positions)
 
        draw_window(win)
        draw_next_shape(next_piece, win)
        pygame.display.update()
 
        if check_lost(locked_positions):
            run = False
 
    center_text("You Lost", 40, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)
 
 
def main_menu():
    run = True
    while run:
        win.fill((0,0,0))
        center_text('Press any key to begin.....', 60, (255, 0, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
 
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()
 
 
win = pygame.display.set_mode((width_s, height_s))
pygame.display.set_caption('Tetris, Made By: Saarthak & Shubham')
 
main_menu()