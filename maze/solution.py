import collections
from maze.maze import Maze
from maze.cell import Cell


def bfs(maze: Maze, root: Cell, exit: Cell):

    visited, queue = set(), collections.deque([root])
    visited.add((root.x, root.y))
    prev = {}

    while queue:

        vertex = queue.popleft()
        print(vertex, end=" ")

        for neighbor in maze.get_neighbors_open(vertex):
            position = (neighbor.x, neighbor.y)
            prev[position] = (vertex.x, vertex.y)
            if position not in visited:
                visited.add(position)
                queue.append(neighbor)
                if position == (neighbor.x, neighbor.y)
                    return 
