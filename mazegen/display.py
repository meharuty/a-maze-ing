from mazegen.cell import Cell
from mazegen.solution import bfs
from mazegen.maze import Maze


class MazeDisplay:
    """Provide methods for displaying a maze in the terminal."""

    COLORS = {1: "\033[37m",  # White
              2: "\033[32m",  # Green
              3: "\033[33m",  # Yellow
              4: "\033[34m",  # Blue
              5: "\033[35m"  # Magenta
              }

    RESET = "\033[0m"

    @staticmethod
    def ascii(maze: Maze, ent: Cell, ex: Cell,
              show_path: bool, color: int = 1, col2: int = 1) -> str:
        """
        Build and return the ASCII representation of a maze.

        Args:
            maze: The maze to display.
            ent: The entrance cell.
            ex: The exit cell.
            show_path: Whether to display the shortest path.
            color: The color number used for the maze walls and path.
        Returns:
            A string containing the ASCII representation of the maze.
        """

        path_cells = []
        if show_path and ent and ex:
            path = bfs(maze, ent, ex)
            path_cells = [(cell.x, cell.y) for cell in path]
        entry = (ent.x, ent.y)
        exit = (ex.x, ex.y)

        color_code = MazeDisplay.COLORS.get(color, MazeDisplay.COLORS[1])
        col2_code = MazeDisplay.COLORS.get(col2, MazeDisplay.COLORS[1])

        pattern_cells = MazeDisplay._get_42_pattern_cells(maze)
        result = []
        result.append(
            color_code + "+" + "---+" * maze.width + MazeDisplay.RESET
            )
        for y in range(maze.height):
            row = color_code + "|"
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if (x, y) in pattern_cells:
                    if entry in pattern_cells:
                        raise ValueError("Error entry in 42 pattern")
                    if exit in pattern_cells:
                        raise ValueError("Error exit in 42 pattern")
                    row += col2_code + " \u2588 "
                elif entry and (x, y) == entry:
                    row += " S "
                elif exit and (x, y) == exit:
                    row += " E "
                elif (x, y) in path_cells:
                    row += color_code + " * "
                else:
                    row += "   "
                row += color_code + "|" if cell.east else " "
            result.append(row)
            bottom = color_code + "+"
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if cell.south:
                    bottom += color_code + "---+"
                else:
                    bottom += color_code + "   +"
            result.append(bottom)
        return "\n".join(result)

    @staticmethod
    def _get_42_pattern_cells(maze: Maze) -> set[tuple[int, int]]:
        """Return the coordinates of cells forming the '42' pattern.
        Args:
            maze: The maze used to determine the pattern position.

            Returns:
                A set of (x, y) coordinates belonging to the '42' pattern.
                An empty set is returned if the maze is too small.
        """

        width = maze.width
        height = maze.height

        if width < 14 or height < 10:
            return set()

        center_x = width // 2
        center_y = height // 2

        pattern_cells = set()

        four_pattern = [
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
        ]

        two_pattern = [
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
        ]

        start_x_4 = center_x - 5
        start_y_4 = center_y - 3

        start_x_2 = center_x + 1
        start_y_2 = center_y - 3

        for dy in range(7):
            for dx in range(5):
                if four_pattern[dy][dx] == 1:
                    x = start_x_4 + dx
                    y = start_y_4 + dy
                    if maze.in_bounds(x, y):
                        pattern_cells.add((x, y))
        for dy in range(7):
            for dx in range(5):
                if two_pattern[dy][dx] == 1:
                    x = start_x_2 + dx
                    y = start_y_2 + dy
                    if maze.in_bounds(x, y):
                        pattern_cells.add((x, y))

        return pattern_cells

    @staticmethod
    def print_ascii(maze: Maze, entry: Cell,
                    exit: Cell, show_path: bool = False, color: int = 1,
                    col2: int = 1
                    ) -> None:
        """Print the ASCII representation of a maze to the terminal.

        Args:
            maze: The maze to display.
            entry: The entrance cell.
            exit: The exit cell.
            show_path: Whether to display the shortest path.
            color: The color number used for the maze display.
        """
        print(MazeDisplay.ascii(maze, entry, exit, show_path, color, col2))

    @staticmethod
    def preview(maze: Maze, entry: Cell, exit: Cell,
                show_path: bool = False, color: int = 1,
                col2: int = 1) -> None:
        """Display a preview of the maze in the terminal.

        Args:
            maze: The maze to display.
            entry: The entrance cell.
            exit: The exit cell.
            show_path: Whether to display the shortest path.
            color: The color number used for the maze display.
        """
        MazeDisplay.print_ascii(maze, entry, exit, show_path, color, col2)
