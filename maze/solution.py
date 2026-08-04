import collections
from maze.maze import Maze
from maze.cell import Cell


def bfs(maze: Maze, root: Cell):

    visited, queue = set(), collections.deque([root])
    visited.add((root.x, root.y))

    while queue:

        vertex = queue.popleft()
        print(vertex, end=" ")

        for neighbour in maze.neighbors(vertex):
            position = (neighbour.x, neighbour.y)
            if position not in visited:
                visited.add(position)
                queue.append(neighbour)
