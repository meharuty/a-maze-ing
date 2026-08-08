import sys

from maze.parser import ConfigParser
from maze.maze import Maze
from maze.generator import MazeGenerator
from maze.maze_hexadecimal import HexRepr
from maze.solution import bfs, path_to_directions
from maze.display import MazeDisplay
from maze.regenerator import regenerate_maze


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return

    parser = ConfigParser(sys.argv[1])
    try:
        config = parser.parse()
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return
    except ValueError as error:
        print(f"Error: {error}")
        return
    except FileExistsError as error:
        print(f"Error: {error}")
        return

    maze = Maze(config["WIDTH"], config["HEIGHT"])
    generator = MazeGenerator(maze, config["SEED"])
    generator.generate(config["PERFECT"])

    if not generator.validate_dfs():
        print("Generation failed.")
        return

    print("Maze generated successfully!")

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

    try:
        MazeDisplay.preview(
            maze,
            entry,
            exit
        )
    except ValueError as e:
        print(e)
        return

    show_path = False
    choice = ""

    while (choice != 'q'):
        print("""Choose an action:
r - Regenerate maze
p - Show/Hide path
c - Change wall colour
q - Quit""")

        choice = input('\n')
        if choice not in ['r', 'p', 'c', 'q']:
            print("YOUR CHOICE IS WRONG!")
            return

        if choice == 'r':
            maze = regenerate_maze(config)
            MazeDisplay.preview(maze, entry, exit)

        if choice == 'p':
            show_path = not show_path
            MazeDisplay.preview(maze, entry, exit, show_path)

        if choice == 'c':
            col = int(input("Choose color (1-5)"))
            if col not in [1, 2, 3, 4, 5]:
                print("error")
                return
            MazeDisplay.preview(maze, entry, exit, show_path, col)


if __name__ == "__main__":
    main()
