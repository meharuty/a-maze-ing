from generator import MazeGenerator
import random
from maze.maze import Maze


def regenerate_maze(config: dict, seed: int) -> tuple[Maze, MazeGenerator]:
    maze = Maze(
        config["WIDTH"],
        config["HEIGHT"]
    )

    seed = seed * random.randint(2, 10)

    generator = MazeGenerator(maze, seed)
    generator.generate()

    if not config["PERFECT"]:
        generator.for_non_perfect()

    return maze, generator
