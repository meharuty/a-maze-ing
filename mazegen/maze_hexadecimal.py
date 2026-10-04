from mazegen.maze import Maze
from mazegen.cell import Cell


class HexRepr:
    """Represent a maze using hexadecimal wall encoding."""

    def __init__(self, maze: Maze) -> None:
        """Initialize the hexadecimal maze representation.

        Args:
            maze: The maze to represent.
        """

        self.maze = maze

    def write(self, filename: str) -> None:
        """Write the maze to a file using hexadecimal encoding.

        Args:
            filename: The path of the output file.
        """

        with open(filename, "w") as file:
            for y in range(self.maze.height):
                for x in range(self.maze.width):
                    cell = self.maze.get_cell(x, y)
                    file.write(self.cell_to_hex(cell))
                file.write("\n")

    def cell_to_hex(self, cell: Cell) -> str:
        """Convert a cell's wall bitmask to a hexadecimal character.

        Args:
            cell: The cell to convert.

        Returns:
            The hexadecimal representation of the cell's wall bitmask.
        """
        return format(cell.get_bitmask(), "X")
