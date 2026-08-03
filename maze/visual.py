from maze.maze import Maze
from maze.cell import Cell


class MazeVisualizer:
    def __init__(self, maze: Maze):
        self.maze = maze

    def print_north(self, cell: Cell) -> None:
        if cell.north:
            print("\u2588", end="")
        else:
            print(" ", end="")

    def print_south(self, cell: Cell) -> None:
        if cell.south:
            print("\u2588", end="")
        else:
            print(" ", end="")

    def print_west(self, cell: Cell) -> None:
        if cell.west:
            print("\u2588", end="")
        else:
            print(" ", end="")

    def print_east(self, cell: Cell) -> None:
        if cell.east:
            print("\u2588", end="")
        else:
            print(" ", end="")

    def maze_visualizer(self) -> None:
        for row in self.maze.grid:
            for cell in row:
                self.print_north(cell)
                self.print_west(cell)
                print(" ", end="")
                self.print_east(cell)
                self.print_south(cell)
