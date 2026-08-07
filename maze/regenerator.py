from generator import MazeGenerator
import random
from maze.maze import Maze


def regenerate_maze(config: dict, seed: int) -> tuple[Maze, MazeGenerator]:
    maze = Maze(
        config["WIDTH"],
        config["HEIGHT"]
    )

    new_seed = seed * random.randint(2, 10)

    generator = MazeGenerator(maze, new_seed)
    generator.generate(config["PERFECT"])

    return maze, generator
