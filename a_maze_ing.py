import sys

from mazegen.parser import ConfigParser
from mazegen.maze import Maze
from mazegen.generator import MazeGenerator
from mazegen.maze_hexadecimal import HexRepr
from mazegen.solution import bfs, path_to_directions
from mazegen.display import MazeDisplay


def main() -> None:
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
    generator.generate(config["PERFECT"], config["ENTRY"])

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
    col = 1
    col2 = 1

    while (choice != '5'):
        print("""=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Rotate the 42 pattern colours
5. Quit""")

        choice = input('\n')
        if choice not in ['1', '2', '3', '4']:
            print("YOUR CHOICE IS WRONG!")
            continue

        if choice == '1':
            maze = generator.regenerate_maze(config)

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

            MazeDisplay.preview(
                maze=maze,
                entry=entry,
                exit=exit,
                show_path=show_path,
                color=col,
                col2=col2
            )

        if choice == '2':
            show_path = not show_path
            MazeDisplay.preview(maze, entry, exit, show_path, col, col2)

        if choice == '3':
            co = input("Choose color (1-5)")
            if co not in ['1', '2', '3', '4', '5']:
                print("error")
                return
            col = int(co)
            MazeDisplay.preview(maze, entry, exit, show_path, col, col2)

        if choice == '4':
            co2 = input("Choose color (1-5)")
            if co2 not in ['1', '2', '3', '4', '5']:
                print("error")
                return
            col2 = int(co2)
            MazeDisplay.preview(maze, entry, exit, show_path, col, col2)


if __name__ == "__main__":
    main()
