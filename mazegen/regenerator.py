from mazegen.generator import MazeGenerator
import random
from mazegen.maze import Maze
from typing import Any


def regenerate_maze(config: dict[str, Any]) -> Maze:
    """Generate a new maze using the provided configuration.
    A new seed is derived from the configured seed when one is provided.

    Args:
        config: Validated maze configuration containing the maze dimensions,
        entry point, generation mode, and optional seed.

    Returns:
        A newly generated maze.
    """
    maze = Maze(
        config["WIDTH"],
        config["HEIGHT"]
    )
    new_seed = None
    if config["SEED"]:
        new_seed = config["SEED"] * random.randint(2, 10)

    generator = MazeGenerator(maze, new_seed)
    generator.generate(config["PERFECT"], config["ENTRY"])

    return maze
