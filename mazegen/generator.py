import random
from typing import Any
from mazegen.maze import Maze
from mazegen.cell import Cell
from mazegen.display import MazeDisplay


class MazeGenerator:
    """Generate and modify mazes using randomized maze algorithms."""
    def __init__(self, maze: Maze, seed: Any) -> None:
        """Initialize the maze generator.

        Args:
            maze: The maze to generate and modify.
            seed: Seed used to initialize the random number generator.
        """

        self.maze = maze
        self.random = random.Random(seed)

    def generate(self, perfect: bool, entry: tuple[int, int]) -> None:
        """Generate a maze starting from the given entry cell.

        Args:
            perfect: Whether to generate a perfect maze without loops.
            entry: Coordinates of the cell where generation starts.
        """

        x, y = entry
        start = self.maze.grid[x][y]
        self._visit(start)

        self.carve_42_pattern()
        if not perfect:
            self.for_non_perfect()

    def _visit(self, cell: Cell) -> None:
        """Generate maze passages using an iterative DFS algorithm.

        Args:
            cell: The cell from which maze generation starts.
        """

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

    def regenerate_maze(self, config: dict[str, Any]) -> Maze:
        """Generate a new maze using the provided configuration.
        A new seed is derived from the configured seed when one is provided.

        Args:
            config: Validated maze configuration containing
            the maze dimensions,
            entry point, generation mode, and optional seed.

        Returns:
            A newly generated maze.
        """
        width = self.maze.width
        height = self.maze.height
        self.maze = Maze(width, height)
        new_seed = None
        if config["SEED"]:
            new_seed = config["SEED"] * random.randint(2, 1000)

        self.random = random.Random(new_seed)
        self.generate(config["PERFECT"], config["ENTRY"])

        return self.maze

    def unvisited_neighbors(self, cell: Cell) -> list[Cell]:
        """Return neighboring cells that have not been visited.

        Args:
            cell: The cell whose neighbors are checked.

        Returns:
            A list of unvisited neighboring cells.
        """

        return [
            neighbor
            for neighbor in self.maze.neighbors(cell)
            if not neighbor.visited
        ]

    def validate_dfs(self) -> bool:
        """Check whether every cell in the maze was visited.

        Returns:
            True if all cells were visited, otherwise False.
        """

        for row in self.maze.grid:
            for cell in row:
                if not (cell.visited):
                    return False
        return True

    def for_non_perfect(self) -> None:
        """Modify a perfect maze to create a non-perfect maze."""

        self.open_corners()
        self.open_center()
        self.add_loops()
        self.reduce_dead_ends()

    def open_corners(self) -> None:
        """Open passages around the four corners of the maze."""

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
                if self.can_remove_wall(corner, neighbor):
                    self.maze.remove_wall(corner, neighbor)

    def add_loops(self, count: int = 2) -> None:
        """Add passages to create additional routes in the maze.

        Args:
            count: Maximum number of additional passages to create.
        """

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

            if self.can_remove_wall(cell, neighbor):
                self.maze.remove_wall(cell, neighbor)
                added += 1

            if added >= count:
                return

    def dead_ends(self) -> list[Cell]:
        """Find all cells that are dead ends.

        Returns:
            A list of cells having exactly one open passage.
        """

        result = []

        for row in self.maze.grid:
            for cell in row:
                if self.degree(cell) == 1:
                    result.append(cell)

        return result

    def reduce_dead_ends(self) -> None:
        """Reduce the number of dead ends by opening additional passages."""

        while True:
            dead_ends = self.dead_ends()
            if len(dead_ends) == 0:
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

                    if self.can_remove_wall(cell, neighbor):
                        self.maze.remove_wall(cell, neighbor)
                        opened = True
                        break

                if opened:
                    break

            if not opened:
                return

    def open_center(self) -> None:
        """Open a passage from the center cell to a neighboring cell."""

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
            if self.can_remove_wall(center, neighbor):
                self.maze.remove_wall(center, neighbor)

    def degree(self, cell: Cell) -> int:
        """Return the number of open passages connected to a cell.

        Args:
            cell: The cell whose open passages are counted.

        Returns:
            The number of open sides of the cell.
        """

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
        """Check whether two neighboring cells have an open passage.

        Args:
            first: The first cell.
            second: The neighboring cell to check.

        Returns:
            True if the passage between the cells is open, otherwise False.
        """

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
        """Check whether opening a wall creates a 3x3 open area.

        Args:
            first: The first cell of the potential passage.
            second: The neighboring cell of the potential passage.

        Returns:
            True if opening the wall creates a 3x3 open area, otherwise False.
        """

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
        """Check whether a 3x3 area is completely open.

        Args:
            start_x: The x-coordinate of the area's top-left cell.
            start_y: The y-coordinate of the area's top-left cell.

        Returns:
            True if the 3x3 area is fully open, otherwise False.
        """

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
        """Close the cells required to create the '42' pattern."""

        pattern_cells = MazeDisplay._get_42_pattern_cells(self.maze)
        if not pattern_cells:
            print("Warning: Maze too small for '42' pattern - skipping")
            return
        for x, y in pattern_cells:
            cell = self.maze.get_cell(x, y)
            self._make_cell_closed(cell)

    def _make_cell_closed(self, cell: Cell) -> None:
        """Close all four walls of a cell and its neighboring walls.

        Args:
            cell: The cell to close completely.
        """

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

    def protected_cells(self, cell: Cell) -> bool:
        """Check whether a cell belongs to the '42' pattern.

        Args:
            cell: The cell to check.

        Returns:
            True if the cell belongs to the protected '42' pattern,
            otherwise False.
        """

        protected_cells = []
        pattern_cells = MazeDisplay._get_42_pattern_cells(self.maze)
        for x, y in pattern_cells:
            c = self.maze.get_cell(x, y)
            protected_cells.append(c)
        if cell in protected_cells:
            return True
        return False

    def can_remove_wall(self, first: Cell, second: Cell) -> bool:
        """Check whether a wall can safely be removed.

        Args:
            first: The first cell.
            second: The neighboring cell.
        """

        return (
            not self.protected_cells(first)
            and not self.protected_cells(second)
        )
