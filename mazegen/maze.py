from mazegen.cell import Cell


class Maze:
    """Represent a rectangular maze as a grid of cells."""

    def __init__(self, width: int, height: int):
        """Initialize a maze with the given dimensions.

        Args:
            width: The number of cells along the horizontal axis.
            height: The number of cells along the vertical axis.

        Raises:
            ValueError: If width or height is not positive.
        """

        if width <= 0 or height <= 0:
            raise ValueError("Maze dimensions must be positive.")

        self.width = width
        self.height = height

        self.grid = [
            [Cell(x, y) for y in range(height)]
            for x in range(width)
        ]

    def get_cell(self, x: int, y: int) -> Cell:
        """Return the cell at the specified coordinates.

        Args:
            x: The horizontal coordinate of the cell.
            y: The vertical coordinate of the cell.

        Returns: The cell at the given coordinates.
        """
        return self.grid[x][y]

    def in_bounds(self, x: int, y: int) -> bool:
        """Check whether the given coordinates are inside the maze.

        Args:
            x: The horizontal coordinate to check.
            y: The vertical coordinate to check.

        Returns:
            True if the coordinates are inside the maze, otherwise False.
        """
        return (
            0 <= x < self.width
            and
            0 <= y < self.height
        )

    def neighbors(self, cell: Cell) -> list[Cell]:
        """Return all cells directly adjacent to a given cell.

        Args:
            cell: The cell whose neighbors should be found.

        Returns:
            A list of adjacent cells that are within the maze boundaries.
        """

        neighbors = []

        directions = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0)
        ]

        for dx, dy in directions:
            nx = cell.x + dx
            ny = cell.y + dy

            if self.in_bounds(nx, ny):
                neighbors.append(self.get_cell(nx, ny))

        return neighbors

    def get_neighbors_open(self, cell: Cell) -> list[Cell]:
        """Return neighboring cells connected by an open passage.

        Args:
            cell: The cell whose open neighbors should be found.

        Returns:
            A list of neighboring cells that
            can be reached without crossing a wall.
        """

        valid = []

        for neighbor in self.neighbors(cell):
            dx = neighbor.x - cell.x
            dy = neighbor.y - cell.y

            if dx == 1 and not cell.east:
                valid.append(neighbor)

            elif dx == -1 and not cell.west:
                valid.append(neighbor)

            elif dy == 1 and not cell.south:
                valid.append(neighbor)

            elif dy == -1 and not cell.north:
                valid.append(neighbor)

        return valid

    def remove_wall(self, first: Cell, second: Cell) -> None:
        """Remove the wall between two adjacent cells.

        Args:
            first: The first cell.
            second: The second cell.

        Raises:
            ValueError: If the cells are not directly adjacent.
        """

        dx = second.x - first.x
        dy = second.y - first.y

        if dx == 1:
            first.east = False
            second.west = False

        elif dx == -1:
            first.west = False
            second.east = False

        elif dy == 1:
            first.south = False
            second.north = False

        elif dy == -1:
            first.north = False
            second.south = False

        else:
            raise ValueError("Cells are not adjacent.")

    def add_wall(self, first: Cell, second: Cell) -> None:
        """Add a wall between two adjacent cells.

        Args:
            first: The first cell.
            second: The second cell.

        Raises:
            ValueError: If the cells are not directly adjacent.
        """

        dx = second.x - first.x
        dy = second.y - first.y

        if dx == 1:
            first.east = True
            second.west = True

        elif dx == -1:
            first.west = True
            second.east = True

        elif dy == 1:
            first.south = True
            second.north = True

        elif dy == -1:
            first.north = True
            second.south = True

        else:
            raise ValueError("Cells are not adjacent.")
