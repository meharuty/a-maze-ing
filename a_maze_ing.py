import sys

from maze.parser import ConfigParser
from maze.maze import Maze
from maze.generator import MazeGenerator
# from maze.visual import MazeVisualizer
from maze.maze_hexadecimal import HexRepr
from maze.solution import bfs, path_to_directions
from maze.display import MazeDisplay


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return

    parser = ConfigParser(sys.argv[1])
    config = parser.parse()

    maze = Maze(config["WIDTH"], config["HEIGHT"])
    generator = MazeGenerator(maze, config["SEED"])
    generator.generate()

    if not config["PERFECT"]:
        generator.for_non_perfect()

    if not generator.validate_dfs():
        print("Generation failed.")
        return

    print("Maze generated successfully!")

    # vis_repr = MazeVisualizer(maze)
    # vis_repr.visualize()

    entry_x, entry_y = config["ENTRY"]
    exit_x, exit_y = config["EXIT"]

    entry = maze.grid[entry_x][entry_y]
    exit = maze.grid[exit_x][exit_y]

    path = bfs(
        maze=maze,
        root=entry,
        target=exit
    )

    solution = path_to_directions(path)

    hex_repr = HexRepr(maze)
    hex_repr.write(config["OUTPUT_FILE"])

    with open(config["OUTPUT_FILE"], "a") as file:
        file.write("\n\n")
        file.write(f"{entry_x},{entry_y}\n")
        file.write(f"{exit_x},{exit_y}\n")
        file.write(solution + "\n")

    print("Shortest path:", solution)
    """for current, next_cell in zip(path, path[1:]):
        print(
            f"({current.x}, {current.y})"
            f" -> "
            f"({next_cell.x}, {next_cell.y})"
        )"""
    MazeDisplay.preview(
        maze,
        entry,
        exit
    )


if __name__ == "__main__":
    main()
