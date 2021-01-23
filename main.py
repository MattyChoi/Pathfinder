import pygame
from algs import *
from init_pygame import *

WIDTH = 600
BUTTON = 60
WIN = pygame.display.set_mode((WIDTH, WIDTH + BUTTON))
pygame.display.set_caption("A* Path Finding Algorithm")

def main(win, width, bton):
    ROWS = 30
    grid = make_grid(ROWS, width)

    start = end = algo = None

    run = True

    alg = button(0, width, width // 2, bton, text='Choose Algorithm: A, B, or 2')
    reset = button(width // 2 , width, width // 2, bton, text='Reset')

    pygame.font.init()

    while run:
        draw(win, grid, ROWS, width, alg, reset)

        win.fill(WHITE)
        for row in grid:
            for node in row:
                node.draw(win)
        draw_grid(win, ROWS, width)
        alg.draw(win)
        reset.draw(win)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]: # left
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                if col < ROWS:
                    node = grid[row][col]
                    if not start:
                        start = node
                        start.make_start()
                    elif not end:
                        if node != start:
                            end = node
                            end.make_end()
                    elif node != end and node != start:
                        node.make_bar()
                elif reset.isOver(pos):
                    start = None
                    end = None
                    algo = None
                    alg.text = "Choose Algorithm: A, B, or 2"
                    grid = make_grid(ROWS, width)
                    '''
                    if node.is_bar():
                        node.undo()
                    else:
                        node.make_bar()
                    '''
            elif pygame.mouse.get_pressed()[2]: # right
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    if algo == "a":
                        astar(lambda: draw(WIN, grid, ROWS, width, alg, reset), grid, start, end)
                    elif algo == "b":
                        bfs(lambda: draw(WIN, grid, ROWS, width, alg, reset), grid, start, end)
                    elif algo == "2":
                        bider(lambda: draw(WIN, grid, ROWS, width, alg, reset), grid, start, end)
                if event.key == pygame.K_a:
                    alg.text = "A* algorithm"
                    algo = "a"
                elif event.key == pygame.K_b:
                    alg.text = "BFS algorithm"
                    algo = "b"
                elif event.key == pygame.K_2:
                    alg.text = "Bidirectional BFS algorithm"
                    algo = "2"


    pygame.quit()


if __name__ == '__main__':
    main(WIN, WIDTH, BUTTON)