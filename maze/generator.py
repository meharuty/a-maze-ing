import random
from maze.maze import Maze
from maze.cell import Cell


class MazeGenerator:
    def __init__(self, maze: Maze, seed: int) -> None:
        self.maze = maze
        self.random = random.Random(seed)

    def generate(self, perfect: bool) -> None:
        start = self.maze.grid[0][0]
        self._visit(start)

        if not perfect:
            self.for_non_perfect()

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
        self.open_corners()
        self.add_loops()
        self.reduce_dead_ends()

    def open_corners(self) -> None:
        corners = [
            self.maze.get_cell(0, 0),
            self.maze.get_cell(self.maze.width - 1, 0),
            self.maze.get_cell(0, self.maze.height - 1),
            self.maze.get_cell(
                self.maze.width - 1,
                self.maze.height - 1
            ),
        ]

        for corner in corners:
            neighbors = self.maze.neighbors(corner)

            for neighbor in neighbors:
                self.maze.remove_wall(corner, neighbor)

    def add_loops(self, count=2) -> None:
        added = 0

        for row in self.maze.grid:
            for cell in row:

                if cell.x + 1 < self.maze.width:
                    neighbor = self.maze.get_cell(cell.x + 1, cell.y)

                    if self.random.random() < 0.1:
                        self.maze.remove_wall(cell, neighbor)
                        added += 1

                if cell.y + 1 < self.maze.height:
                    neighbor = self.maze.get_cell(cell.x, cell.y + 1)

                    if self.random.random() < 0.1:
                        self.maze.remove_wall(cell, neighbor)
                        added += 1

                if added >= count:
                    return

    def dead_ends(self):
        result = []

        for row in self.maze.grid:
            for cell in row:
                if self.degree(cell) == 1:
                    result.append(cell)

        return result

    def reduce_dead_ends(self) -> None:
        while True:
            dead_ends = self.dead_ends()

            if len(dead_ends) <= 2:
                break

            cell = self.random.choice(dead_ends)

            neighbors = self.maze.neighbors(cell)

            if neighbors:
                neighbor = self.random.choice(neighbors)
                self.maze.remove_wall(cell, neighbor)

    def degree(self, cell: Cell) -> int:
        degree = 0

        if not cell.north:
            degree += 1

        if not cell.south:
            degree += 1

        if not cell.east:
            degree += 1

        if not cell.west:
            degree += 1

        return degree
