from collections import deque


class MazeDisplay:
    @staticmethod
    def ascii(maze, entry=None, exit=None, show_path=False) -> str:
        path_cells =set()
        if show_path and entry and exit:
            path_cells = MazeDisplay.find_path(maze, entry, exit)
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
    def find_path(maze, start, end) -> set:
        start_cell = maze.get_cell(start[0], start[1])
        end_cell = maze.get_cell(end[0], end[1])
        queue = deque([(start_cell, [])])
        visited = set()
        visited.add((start_cell.x, start_cell.y))
        while queue:
            current, path = queue.popleft()
            if current.x == end_cell.x and current.y == end_cell.y:
                return set(path + [(current.x, current.y)])
            for dx, dy in [(0, -1), (1, 0), (0,1), (-1, 0)]:
                nx, ny = current.x + dx, current.y + dy
                if maze.in_bounds(nx, ny) and (nx, ny) not in visited:
                    neighbor = maze.get_cell(nx, ny)
                    can_move = False
                    if dx == 1 and not current.east:
                        can_move = True
                    elif dx == -1 and not current.west:
                        can_move = True
                    elif dy == 1 and not current.south:
                        can_move = True
                    elif dy == -1 and not current.north:
                        can_move = True
                    if can_move:
                        visited.add((nx, ny))
                        queue.append((neighbor, path + [(current.x, current.y)]))
        return set()

    @staticmethod
    def print_ascii(maze, entry=None, exit=None, show_path=False) -> None:
        print(MazeDisplay.ascii(maze, entry, exit, show_path))

    @staticmethod
    def preview(maze, entry=None, exit=None, show_path=True) -> None:
        print("\n" + "="*50)
        print("🧩  MAZE PREVIEW")
        print("="*50)
        MazeDisplay.print_ascii(maze, entry, exit, show_path)
        print("="*50 + "\n")
