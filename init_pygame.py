import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width #x position in window (from 0 to WIDTH)
        self.y = col * width #y position in window (from 0 to WIDTH)
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows    #width times total_rows = width of window (approx WIDTH)

    #gets the position
    def get_pos(self):
        return self.row, self.col

    #checks if closed by blocks
    def is_closed(self):
        return self.color == RED

    def is_closed2(self):
        return self.color == BLUE

    # checks if open by blocks
    def is_open(self):
        return self.color == GREEN

    # checks if open by blocks
    def is_open2(self):
        return self.color == YELLOW

    # checks if there is a barrier
    def is_bar(self):
        return self.color == BLACK

    # start block is orange
    def is_start(self):
        return self.color == ORANGE

    # end block is turquoise
    def is_end(self):
        return self.color == TURQUOISE

    # resets the block by changing all the blocks to white
    def reset(self):
        self.color = WHITE

    # make a cube closed
    def make_closed(self):
        self.color = RED

    def make_closed2(self):
        self.color = BLUE

    # make a cube open
    def make_open(self):
        self.color = GREEN

    # make a cube open
    def make_open2(self):
        self.color = YELLOW

    # makes a barrier
    def make_bar(self):
        self.color = BLACK

    # makes the start block
    def make_start(self):
        self.color = ORANGE

    # makes the end block
    def make_end(self):
        self.color = TURQUOISE

    # colors the path
    def make_path(self):
        self.color = PURPLE

    # draws the cube on screen
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        dir = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        self.neighbors = []
        for dr, dc in dir:
            r = self.row + dr
            c = self.col + dc
            if (r < self.total_rows and r >= 0 and c >= 0 and c < self.total_rows and not grid[r][c].is_bar()):
                self.neighbors.append(grid[r][c])


    def __lt__(self, other):
        return False

class button():
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win):
        #Call this method to draw the button on the screen
        pygame.draw.rect(win, BLACK, (self.x,self.y, self.width,self.height+4),0)
            
        pygame.draw.rect(win, WHITE, (self.x + 2,self.y + 2,self.width-4,self.height-4),0)
        
        font = pygame.font.SysFont('comicsans', 20)
        text = font.render(self.text, 1, BLACK)
        win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


def make_grid(rows, width):
    grid = []
    gap = width // rows #width of cubes
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width, alg, reset):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    alg.draw(win)
    reset.draw(win)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col