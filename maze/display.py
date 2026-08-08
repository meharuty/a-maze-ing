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
        pattern_cells = MazeDisplay._get_42_pattern_cells(maze)
        result = []
        result.append("+" + "---+" * maze.width)
        for y in range(maze.height):
            row = "|"
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if (x, y) in pattern_cells:
                    row += " █ "
                elif entry and (x, y) == entry:
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
    def _get_42_pattern_cells(maze):
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
        
        start_x_4 = center_x - 7
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
