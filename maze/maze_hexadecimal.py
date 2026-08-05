from maze.maze import Maze
from maze.cell import Cell


class HexRepr:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def write(self, filename: str) -> None:
        with open(filename, "w") as file:
            for row in self.maze.grid:
                for cell in row:
                    file.write(self.cell_to_hex(cell))
                file.write("\n")

    def cell_to_hex(self, cell: Cell) -> str:
        return format(cell.get_bitmask(), "X")
