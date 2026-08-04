from maze.cell import Cell


class Maze:
    def __init__(self, width: int, height: int):
        if width <= 0 or height <= 0:
            raise ValueError("Maze dimensions must be positive.")

        self.width = width
        self.height = height

        self.grid = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    def in_bounds(self, x: int, y: int) -> bool:
        return (
            0 <= x < self.width
            and
            0 <= y < self.height
        )

    def neighbors(self, cell: Cell) -> list[Cell]:
        neighbors = []

        directions = [
            (0, -1),   # North
            (1, 0),    # East
            (0, 1),    # South
            (-1, 0),   # West
        ]

        for dx, dy in directions:
            nx = cell.x + dx
            ny = cell.y + dy

            if self.in_bounds(nx, ny):
                neighbors.append(self.get_cell(nx, ny))

        return neighbors

    def get_neighbors_open(self, cell: Cell) -> list[Cell]:
        neighb = self.neighbors(cell)
        valid = []
        for neighbor in neighb:
            dx = neighbor.x - cell.x
            dy = neighbor.y - cell.y
        if dx == 1 and not cell.east:
            valid.append(neighbor)
        elif dx == -1 and not cell.west:
            valid.append(neighbor)
        elif dy == 1 and not cell.south:
            valid.append(neighbor)
        elif dy == -1 and not cell.north:
            valid.append(neighbor)
        return valid

    def remove_wall(self, first: Cell, second: Cell) -> None:
        dx = second.x - first.x
        dy = second.y - first.y

        if dx == 1:
            first.east = False
            second.west = False

        elif dx == -1:
            first.west = False
            second.east = False

        elif dy == 1:
            first.south = False
            second.north = False

        elif dy == -1:
            first.north = False
            second.south = False

        else:
            raise ValueError("Cells are not adjacent.")

    def add_wall(self, first: Cell, second: Cell) -> None:
        dx = second.x - first.x
        dy = second.y - first.y

        if dx == 1:
            first.east = True
            second.west = True

        elif dx == -1:
            first.west = True
            second.east = True

        elif dy == 1:
            first.south = True
            second.north = True

        elif dy == -1:
            first.north = True
            second.south = True

        else:
            raise ValueError("Cells are not adjacent.")

    def __repr__(self) -> str:
        return (
            f"Maze(width={self.width}, "
            f"height={self.height})"
        )
