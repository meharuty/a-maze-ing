from mazegen.generator import MazeGenerator
import random
from mazegen.maze import Maze
from typing import Any


def regenerate_maze(config: dict[str, Any]) -> Maze:
    maze = Maze(
        config["WIDTH"],
        config["HEIGHT"]
    )
    new_seed = None
    if config["SEED"]:
        new_seed = config["SEED"] * random.randint(2, 10)

    generator = MazeGenerator(maze, new_seed)
    generator.generate(config["PERFECT"])

    return maze
