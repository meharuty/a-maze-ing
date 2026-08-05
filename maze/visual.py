from maze.maze import Maze


class MazeVisualizer:
    def __init__(self, maze: Maze):
        self.maze = maze

    def visualize(self) -> None:
        for y in range(self.maze.height):
            self.print_north_walls(y)
            self.print_side_walls(y)

        self.print_south_walls()

    def print_north_walls(self, y: int) -> None:
        for x in range(self.maze.width):
            cell = self.maze.grid[x][y]

            if x == 0:
                print("┌", end="")

            if cell.north:
                print("───", end="")
            else:
                print("   ", end="")

            if x == self.maze.width - 1:
                print("┐")
            else:
                next_cell = self.maze.grid[x + 1][y]

                if cell.north and next_cell.north:
                    print("┬", end="")
                else:
                    print(" ", end="")

    def print_side_walls(self, y: int) -> None:
        for x in range(self.maze.width):
            cell = self.maze.grid[x][y]

            if x == 0:
                print("│" if cell.west else " ", end="")

            print("   ", end="")

            if cell.east:
                print("│", end="")
            else:
                print(" ", end="")

        print()

    def print_south_walls(self) -> None:
        y = self.maze.height - 1

        for x in range(self.maze.width):
            cell = self.maze.grid[x][y]

            if x == 0:
                print("└", end="")

            if cell.south:
                print("───", end="")
            else:
                print("   ", end="")

            if x == self.maze.width - 1:
                print("┘")
            else:
                print("┴" if cell.south else " ", end="")
