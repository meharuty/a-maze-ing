from maze.cell import Cell
from maze.solution import bfs


class MazeDisplay:
    COLORS = {1: "\033[37m",  # White
              2: "\033[32m",  # Green
              3: "\033[33m",  # Yellow
              4: "\033[34m",  # Blue
              5: "\033[35m"  # Magenta
              }

    RESET = "\033[0m"

    @staticmethod
    def ascii(maze, entry: Cell, exit: Cell, show_path, color=1) -> str:
        path_cells = []
        if show_path and entry and exit:
            path_cells = bfs(maze, entry, exit)
            path_cells = [(cell.x, cell.y) for cell in path_cells]
        entry = (entry.x, entry.y)
        exit = (exit.x, exit.y)

        color_code = MazeDisplay.COLORS.get(color, MazeDisplay.COLORS[1])

        result = []
        result.append(
            color_code + "+" + "---+" * maze.width + MazeDisplay.RESET
            )
        for y in range(maze.height):
            row = color_code + "|"
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if entry and (x, y) == entry:
                    row += " S "
                elif exit and (x, y) == exit:
                    row += " E "
                elif (x, y) in path_cells:
                    row += " * "
                else:
                    row += "   "
                row += "|" if cell.east else " "
            row += MazeDisplay.RESET
            result.append(row)

            bottom = color_code + "+"
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
    def print_ascii(maze, entry: Cell,
                    exit: Cell, show_path=False, color=1) -> None:
        print(MazeDisplay.ascii(maze, entry, exit, show_path, color))

    @staticmethod
    def preview(maze, entry: Cell,
                exit: Cell,
                show_path=False, color=1
                ) -> None:
        print()
        print("Amazing Maze")
        MazeDisplay.print_ascii(maze, entry, exit, show_path, color)
        print()
