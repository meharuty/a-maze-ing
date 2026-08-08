import random
from maze.maze import Maze
from maze.cell import Cell
from maze.display import MazeDisplay


class MazeGenerator:
    def __init__(self, maze: Maze, seed: int) -> None:
        self.maze = maze
        self.random = random.Random(seed)

    def generate(self, perfect: bool) -> None:
        start = self.maze.grid[0][0]
        self._visit(start)

        self.carve_42_pattern()
        if not perfect:
            self.for_non_perfect()

    def _visit(self, cell: Cell):
        pattern_cells = MazeDisplay._get_42_pattern_cells(self.maze)
        for x, y in pattern_cells:
            pattern_cell = self.maze.get_cell(x, y)
            pattern_cell.visited = True
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
        self.open_center()
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

    def add_loops(self, count=0) -> None:
        candidates = []

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.get_cell(x, y)

                if x + 1 < self.maze.width:
                    neighbor = self.maze.get_cell(x + 1, y)

                    if not self.is_open(cell, neighbor):
                        candidates.append((cell, neighbor))

                if y + 1 < self.maze.height:
                    neighbor = self.maze.get_cell(x, y + 1)

                    if not self.is_open(cell, neighbor):
                        candidates.append((cell, neighbor))

        self.random.shuffle(candidates)

        added = 0

        for cell, neighbor in candidates:
            if self.creates_large_open_area(cell, neighbor):
                continue

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
        protected_cells = []
        pattern_cells = MazeDisplay._get_42_pattern_cells(self.maze)
        for x, y in pattern_cells:
            c = self.maze.get_cell(x, y)
            protected_cells.append(c)
        while True:
            dead_ends = self.dead_ends()
            if len(dead_ends) <= 0:
                return

            self.random.shuffle(dead_ends)

            opened = False

            for cell in dead_ends:
                candidates = [
                    neighbor
                    for neighbor in self.maze.neighbors(cell)
                    if not self.is_open(cell, neighbor)
                ]

                self.random.shuffle(candidates)

                for neighbor in candidates:
                    large_area = self.creates_large_open_area(
                        cell,
                        neighbor
                    )
                    if large_area:
                        continue

                    if neighbor not in protected_cells:
                        self.maze.remove_wall(cell, neighbor)
                        opened = True
                        break

                if opened:
                    break

            if not opened:
                return

    def open_center(self) -> None:
        protected_cells = []
        pattern_cells = MazeDisplay._get_42_pattern_cells(self.maze)
        for x, y in pattern_cells:
            c = self.maze.get_cell(x, y)
            protected_cells.append(c)

        center_x = self.maze.width // 2
        center_y = self.maze.height // 2

        center = self.maze.get_cell(center_x, center_y)

        neighbors = [
            neighbor
            for neighbor in self.maze.neighbors(center)
            if not self.is_open(center, neighbor)
        ]

        if neighbors:
            neighbor = self.random.choice(neighbors)
            if neighbor not in protected_cells:
                self.maze.remove_wall(center, neighbor)

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

    def is_open(self, first: Cell, second: Cell) -> bool:
        dx = second.x - first.x
        dy = second.y - first.y

        if dx == 1:
            return not first.east

        if dx == -1:
            return not first.west

        if dy == 1:
            return not first.south

        if dy == -1:
            return not first.north

        return False

    def creates_large_open_area(
        self,
        first: Cell,
        second: Cell
    ) -> bool:
        self.maze.remove_wall(first, second)

        result = False

        for y in range(self.maze.height - 2):
            for x in range(self.maze.width - 2):

                if self.is_open_area_3x3(x, y):
                    result = True
                    break

            if result:
                break

        self.maze.add_wall(first, second)

        return result

    def is_open_area_3x3(self, start_x: int, start_y: int) -> bool:
        for y in range(start_y, start_y + 3):
            for x in range(start_x, start_x + 2):
                first = self.maze.get_cell(x, y)
                second = self.maze.get_cell(x + 1, y)

                if not self.is_open(first, second):
                    return False

        for y in range(start_y, start_y + 2):
            for x in range(start_x, start_x + 3):
                first = self.maze.get_cell(x, y)
                second = self.maze.get_cell(x, y + 1)

                if not self.is_open(first, second):
                    return False

        return True

    def carve_42_pattern(self) -> None:
        pattern_cells = MazeDisplay._get_42_pattern_cells(self.maze)
        if not pattern_cells:
            print("Warning: Maze too small for '42' pattern - skipping")
            return
        for x, y in pattern_cells:
            cell = self.maze.get_cell(x, y)
            self._make_cell_closed(cell)

    def _make_cell_closed(self, cell: Cell) -> None:
        cell.north = True
        cell.east = True
        cell.south = True
        cell.west = True
        if cell.x > 0:
            west = self.maze.get_cell(cell.x - 1, cell.y)
            west.east = True
        if cell.x + 1 < self.maze.width:
            east = self.maze.get_cell(cell.x + 1, cell.y)
            east.west = True
        if cell.y > 0:
            north = self.maze.get_cell(cell.x, cell.y - 1)
            north.south = True
        if cell.y + 1 < self.maze.height:
            south = self.maze.get_cell(cell.x, cell.y + 1)
            south.north = True
