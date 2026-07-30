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

        while True:
            neighbors = self.unvisited_neighbors(cell)
            if not neighbors:
                break
            neighbor = self.random.choice(neighbors)
            self.maze.remove_wall(cell, neighbor)
            self._visit(neighbor)

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
