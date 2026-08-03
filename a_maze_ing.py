import sys

from maze.parser import ConfigParser
from maze.maze import Maze
from maze.generator import MazeGenerator
from maze.visual import MazeVisualizer


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return

    parser = ConfigParser(sys.argv[1])
    config = parser.parse()

    maze = Maze(config["WIDTH"], config["HEIGHT"])

    generator = MazeGenerator(maze, config["SEED"])
    generator.generate()

    if generator.validate_dfs():
        print("Maze generated successfully!")
        vis_repr = MazeVisualizer(maze)
        vis_repr.maze_visualizer()
    else:
        print("Generation failed.")


if __name__ == "__main__":
    main()
