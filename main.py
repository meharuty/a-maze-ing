from maze.maze import Maze

maze = Maze(4, 3)

cell = maze.get_cell(1, 1)

print(cell)

print("Neighbors:")
for neighbor in maze.neighbors(cell):
    print(neighbor)

east = maze.get_cell(2, 1)

maze.remove_wall(cell, east)

print("\nAfter removing wall:\n")

print(cell)
print(east)
