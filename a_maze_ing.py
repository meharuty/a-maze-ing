import sys
from parser import ConfigParser
from maze import Maze


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python a_maze_ing.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        # Read and validate configuration
        parser = ConfigParser(config_file)
        config = parser.parse()

        # Create maze
        maze = Maze(
            width=config["WIDTH"],
            height=config["HEIGHT"]
        )

        # Print success
        print("Maze created successfully!")
        print(f"Width: {maze.width}")
        print(f"Height: {maze.height}")
        print(f"Entry: {config['ENTRY']}")
        print(f"Exit: {config['EXIT']}")
        print(f"Perfect: {config['PERFECT']}")
        print(f"Seed: {config['SEED']}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
