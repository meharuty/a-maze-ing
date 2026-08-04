import sys

from maze.parser import ConfigParser
from maze.maze import Maze
from maze.generator import MazeGenerator
from maze.visual import MazeVisualizer
from maze.maze_hexadecimal import HexRepr
from maze.solution import bfs
from maze.cell import Cell


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return

    parser = ConfigParser(sys.argv[1])
    config = parser.parse()

    maze = Maze(config["WIDTH"], config["HEIGHT"])

    generator = MazeGenerator(maze, config["SEED"])
    generator.generate()

    if not (config["PERFECT"]):
        generator.for_non_perfect()

    if generator.validate_dfs():
        print("Maze generated successfully!")
        vis_repr = MazeVisualizer(maze)
        vis_repr.visualize()
    else:
        print("Generation failed.")

    repr = HexRepr(maze)
    repr.write("output.txt")

    bfs(maze=maze, root=Cell(0, 0))


if __name__ == "__main__":
    main()
