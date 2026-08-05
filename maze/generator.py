import random
from maze.maze import Maze
from maze.cell import Cell


class MazeGenerator:
    def __init__(self, maze: Maze, seed: int) -> None:
        self.maze = maze
        self.random = random.Random(seed)

    def generate(self) -> None:
        start = self.maze.grid[0][0]
        self._visit(start)

    def _visit(self, cell: Cell):
        cell.visited = True
        stack = [cell]

        while stack:
            current = stack[-1]
            neighbors = self.unvisited_neighbors(current)
            if not neighbors:
                stack.pop()
            else:
                neighbor = self.random.choice(neighbors)
                neighbor.visited = True
                self.maze.remove_wall(current, neighbor)
                stack.append(neighbor)

    def unvisited_neighbors(self, cell):
        return [
            neighbor
            for neighbor in self.maze.neighbors(cell)
            if not neighbor.visited
        ]

    def validate_dfs(self) -> bool:
        for row in self.maze.grid:
            for cell in row:
                if not (cell.visited):
                    return False
        return True

    def for_non_perfect(self) -> None:
        for row in self.maze.grid:
            for cell in row:

                if cell.x + 1 < self.maze.width:
                    neighbor = self.maze.get_cell(cell.x + 1, cell.y)

                    if self.random.random() < 0.1:
                        self.maze.remove_wall(cell, neighbor)

                if cell.y + 1 < self.maze.height:
                    neighbor = self.maze.get_cell(cell.x, cell.y + 1)

                    if self.random.random() < 0.1:
                        self.maze.remove_wall(cell, neighbor)
