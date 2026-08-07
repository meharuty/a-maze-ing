from maze.cell import Cell
from maze.solution import bfs


class MazeDisplay:
    @staticmethod
    def ascii(maze, entry: Cell, exit: Cell, show_path) -> str:
        path_cells = []
        if show_path and entry and exit:
            path_cells = bfs(maze, entry, exit)
            path_cells = [(cell.x, cell.y) for cell in path_cells]
        entry = (entry.x, entry.y)
        exit = (exit.x, exit.y)
        result = []
        result.append("+" + "---+" * maze.width)
        for y in range(maze.height):
            row = "|"
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
            result.append(row)
            bottom = "+"
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if cell.south:
                    bottom += "---+"
                else:
                    bottom += "   +"
            result.append(bottom)
        return "\n".join(result)

    @staticmethod
    def print_ascii(maze, entry: Cell,
                    exit: Cell, show_path=False) -> None:
        print(MazeDisplay.ascii(maze, entry, exit, show_path))

    @staticmethod
    def preview(maze, entry: Cell, exit: Cell, show_path=False) -> None:
        print("\n" + "="*50)
        print("MAZE PREVIEW")
        print("="*50)
        MazeDisplay.print_ascii(maze, entry, exit, show_path)
        print("="*50 + "\n")
