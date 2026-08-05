from collections import deque
from maze.maze import Maze
from maze.cell import Cell


def bfs(maze: Maze, root: Cell, target: Cell) -> list[Cell]:
    visited = set()
    queue = deque([root])
    parents = {}

    visited.add((root.x, root.y))

    while queue:
        vertex = queue.popleft()

        if vertex == target:
            break

        for neighbour in maze.get_neighbors_open(vertex):
            position = (neighbour.x, neighbour.y)

            if position not in visited:
                visited.add(position)
                parents[position] = vertex
                queue.append(neighbour)

    target_position = (target.x, target.y)

    if target_position not in parents and root != target:
        return []

    path = []
    current = target

    while current != root:
        path.append(current)
        current = parents[(current.x, current.y)]

    path.append(root)
    path.reverse()

    return path


def path_to_directions(path: list[Cell]) -> str:
    directions = []

    for current, next_cell in zip(path, path[1:]):
        dx = next_cell.x - current.x
        dy = next_cell.y - current.y

        if dx == 1 and dy == 0:
            directions.append("E")
        elif dx == -1 and dy == 0:
            directions.append("W")
        elif dx == 0 and dy == 1:
            directions.append("S")
        elif dx == 0 and dy == -1:
            directions.append("N")

    return "".join(directions)
