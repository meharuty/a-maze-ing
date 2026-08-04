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
        value = 0

        if cell.north:
            value |= 1

        if cell.east:
            value |= 2

        if cell.south:
            value |= 4

        if cell.west:
            value |= 8

        return format(value, "X")
