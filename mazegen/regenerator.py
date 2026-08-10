from mazegen.generator import MazeGenerator
import random
from mazegen.maze import Maze
from typing import Any


def regenerate_maze(config: dict[str, Any]) -> Maze:
    maze = Maze(
        config["WIDTH"],
        config["HEIGHT"],
    )

    new_seed = random.SystemRandom().randint(0, 2**32 - 1)

    print("NEW SEED:", new_seed)

    generator = MazeGenerator(maze, new_seed)
    generator.generate(
        config["PERFECT"],
        config["ENTRY"],
    )

    return maze
