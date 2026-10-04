from collections import deque
from mazegen.maze import Maze
from mazegen.cell import Cell


def bfs(maze: Maze, root: Cell, target: Cell) -> list[Cell]:
    """Find the shortest path between two cells using breadth-first search.

    Args:
        maze: The maze in which to search for a path.
        root: The starting cell.
        target: The destination cell.

    Returns:
        A list of cells representing the shortest path from root to target.
        Returns an empty list if the target is unreachable.
    """

    visited = set()
    queue = deque([root])
    parents = {}

    visited.add((root.x, root.y))

    while queue:
        vertex = queue.popleft()

        if vertex.x == target.x and vertex.y == target.y:
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

    while (current.x, current.y) != (root.x, root.y):
        path.append(current)
        current = parents[(current.x, current.y)]

    path.append(root)
    path.reverse()

    return path


def path_to_directions(path: list[Cell]) -> str:
    """Convert a cell path into movement directions.

    Args:
        path: A list of consecutive cells representing a maze path.

    Returns:
        A string containing movement directions using E, W, S, and N
        for east, west, south, and north respectively.
    """
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
