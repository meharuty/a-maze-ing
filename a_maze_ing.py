import sys

from maze.parser import ConfigParser
from maze.maze import Maze
from maze.generator import MazeGenerator
from maze.display import MazeDisplay


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return

    parser = ConfigParser(sys.argv[1])
    config = parser.parse()

    maze = Maze(config["WIDTH"], config["HEIGHT"])

    generator = MazeGenerator(maze, config["SEED"])
    start_cell = maze.get_cell(config["ENTRY"][0], config["ENTRY"][1])
    generator.generate(start_cell)

    if generator.validate_dfs():
        print("Maze generated successfully!")
    else:
        print("Generation failed.")
        return
    MazeDisplay.preview(
        maze,
        entry=(config["ENTRY"][0], config["ENTRY"][1]),
        exit=(config["EXIT"][0], config["EXIT"][1]),
        show_path=True
    )


if __name__ == "__main__":
    main()
