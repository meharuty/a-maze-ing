from maze.maze import Maze
from maze.cell import Cell


class MazeVisualizer:
    def __init__(self, maze: Maze):
        self.maze = maze

    def print_top(self, cell: Cell) -> None:
        if cell.north:
            print("██", end="")
        else:
            print("  ", end="")

    def print_bottom(self, cell: Cell) -> None:
        if cell.south:
            print("██", end="")
        else:
            print("  ", end="")

    def print_left(self, cell: Cell) -> None:
        if cell.west:
            print("█", end="")
        else:
            print(" ", end="")

    def print_right(self, cell: Cell) -> None:
        if cell.east:
            print("█", end="")
        else:
            print(" ", end="")

    def visualize(self) -> None:
        for row in self.maze.grid:

            # Top walls
            for cell in row:
                self.print_top(cell)
            print()

            # Left/right walls
            for cell in row:
                self.print_left(cell)
                print(" ", end="")
                self.print_right(cell)
            print()

            # Bottom walls
            for cell in row:
                self.print_bottom(cell)
            print()
