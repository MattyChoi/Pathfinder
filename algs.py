from queue import PriorityQueue
from collections import deque
import pygame

# heuristic function, finds the manhattan distance between two points
# manhattan distance = L1 norm
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))      # f score, tiebreaker, node
    came_from = {}      # tracks where node came from
    g_score = {node: float("inf") for row in grid for node in row}        #stores g scores, initialize at inf
    g_score[start] = 0      # g score of start is always 0
    f_score = {node: float("inf") for row in grid for node in row}        #stores f scores, initialize at inf
    f_score[start] = h(start.get_pos(), end.get_pos())      # f score of start is heuristic

    open_set_hash = {start}     #creates hash, keeps track of items in open_set

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]     #only want the node, not g score nor count

        if current == end:      #draws path
            end.make_end()
            reconstruct_path(came_from, end, draw)
            start.make_start()
            return

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()
    return

def bfs(draw, grid, start, end):
    q = deque()
    q.append(start)
    visited = {start}
    came_from = {}

    while q:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = q.popleft()     #popping from the left makes us look at the neighbors first and then the neighbors of the neighbors

        if current == end:      #draws path
            end.make_end()
            reconstruct_path(came_from, end, draw)
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                q.append(neighbor)
                visited.add(neighbor)
                neighbor.make_open2()
        draw()

        if current != start:
            current.make_closed2()
            
    return False

def bider(draw, grid, start, end):
    qstart = deque()
    qend = deque()
    qstart.append(start)
    qend.append(end)
    visitStart = {start}
    visitEnd = {end}
    came_fromStart = {}
    came_fromEnd = {}

    while qstart or qend:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        currentStart = qstart.popleft()     #popping from the left makes us look at the neighbors first and then the neighbors of the neighbors
        currentEnd = qend.popleft()

        if currentStart in visitEnd:      #draws path
            currentStart.make_path()
            reconstruct_path(came_fromStart, currentStart, draw)
            reconstruct_path(came_fromEnd, currentStart, draw)
            start.make_start()
            end.make_end()
            return

        if currentEnd in visitStart:      #draws path
            currentEnd.make_path()
            reconstruct_path(came_fromStart, currentEnd, draw)
            reconstruct_path(came_fromEnd, currentEnd, draw)
            start.make_start()
            end.make_end()
            return

        for neighbor in currentStart.neighbors:
            if neighbor not in visitStart:
                came_fromStart[neighbor] = currentStart
                qstart.append(neighbor)
                visitStart.add(neighbor)
                neighbor.make_open()

        for neighbor in currentEnd.neighbors:
            if neighbor not in visitEnd:
                came_fromEnd[neighbor] = currentEnd
                qend.append(neighbor)
                visitEnd.add(neighbor)
                neighbor.make_open2()
        draw()

        if currentStart != start:
            currentStart.make_closed()

        if currentEnd != end:
            currentEnd.make_closed2()
            
    return