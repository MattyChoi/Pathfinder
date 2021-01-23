from Algorithm import *
from init_pygame import *

WIDTH = 700
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = end = None

    run = True
    started = False

    while run:
        draw(WIN, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]: # left
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start:
                    start = node
                    start.make_start()
                elif not end:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_bar()
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
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    astar_algorithm(lambda: draw(WIN, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


    pygame.quit()


if __name__ == '__main__':
    main(WIN, WIDTH)