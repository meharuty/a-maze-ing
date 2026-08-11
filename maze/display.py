from maze.cell import Cell
from maze.solution import bfs
import time
import os


class MazeDisplay:
    COLORS = {1: "\033[37m",  # White
              2: "\033[32m",  # Green
              3: "\033[33m",  # Yellow
              4: "\033[34m",  # Blue
              5: "\033[35m",  # Magenta
              6: "\033[31m"  # red
              }

    RESET = "\033[0m"

    @staticmethod
    def ascii(maze, entry: Cell, exit: Cell, show_path, color=1, col2=1, custom_path=None) -> str:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Maze generated successfully!")
        path_cells = []
        if custom_path is not None:
            path_cells = custom_path
        elif show_path and entry and exit:
            path_cells = bfs(maze, entry, exit)
            path_cells = [(cell.x, cell.y) for cell in path_cells]
        entry = (entry.x, entry.y)
        exit = (exit.x, exit.y)

        color_code = MazeDisplay.COLORS.get(color, MazeDisplay.COLORS[1])
        col_code2 = MazeDisplay.COLORS.get(col2, MazeDisplay.COLORS[1])

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
                    row += col_code2 + " █ "
                elif entry and (x, y) == entry:
                    row += " 🚪"
                elif exit and (x, y) == exit:
                    row += " 🏁"
                elif (x, y) in path_cells:
                    row += color_code + " ■ "
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
    def print_ascii(maze, entry: Cell,
                    exit: Cell, show_path=False, color=1, col2=1, custom_path=None) -> None:
        print(MazeDisplay.ascii(maze, entry, exit, show_path, color, col2, custom_path))

    @staticmethod
    def preview(maze, entry: Cell, exit: Cell,
                show_path=False, color=1, col2=1, custom_path=None) -> None:
        print("\n" + "="*50)
        print("MAZE PREVIEW")
        print("="*50)
        MazeDisplay.print_ascii(maze, entry, exit, show_path, color, col2, custom_path)
        print("="*50 + "\n")

    @staticmethod
    def animate_path(maze, entry: Cell, exit: Cell, delay=0.1, color=1, col2=1) -> None:
        path = bfs(maze, entry, exit)
        if not path:
            print("No path found!")
            return
        path_cells = [(cell.x, cell.y) for cell in path]
        for i in range(len(path_cells) + 1):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Maze generated successfully!")
            MazeDisplay.preview(maze, entry, exit, False, color, col2, path_cells[:i])
            time.sleep(delay)
