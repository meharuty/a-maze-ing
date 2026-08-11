*This project has been created as part of the 42 curriculum by <meharuty>, <ggevorgy>.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python. The program reads a configuration file, generates a random maze, writes it to an output file in hexadecimal format, and displays it visually in the terminal. The maze can be perfect (exactly one path between entry and exit) or imperfect (multiple paths). A hidden "42" pattern is embedded in every maze as fully closed cells.

## Instructions

### Installation

```bash
make install
```

### Run

```bash
make run
# or directly:
python3 a_maze_ing.py config.txt
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint
```

### Clean

```bash
make clean
```

### Build the reusable package

```bash
pip install build
python -m build
```

This generates `mazegen-1.0.0-py3-none-any.whl` and `mazegen-1.0.0.tar.gz` at the root of the repository.

### Install the reusable package

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Configuration File

The configuration file must contain one `KEY=VALUE` pair per line. Lines starting with `#` are comments and are ignored.

### Mandatory keys

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width in number of cells | `WIDTH=20` |
| `HEIGHT` | Maze height in number of cells | `HEIGHT=15` |
| `ENTRY` | Entry coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether the maze is perfect | `PERFECT=True` |

### Optional keys

| Key | Description | Example |
|-----|-------------|---------|
| `SEED` | Random seed for reproducibility | `SEED=42` |

### Example config file

```
# A-Maze-ing configuration file
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Maze Generation Algorithm

We chose the **Recursive Backtracker** algorithm (also known as DFS maze generation).

### How it works

1. Start at the entry cell, mark it as visited
2. Pick a random unvisited neighbor
3. Remove the wall between the current cell and the chosen neighbor
4. Move to the neighbor and repeat
5. If no unvisited neighbors exist, backtrack to the previous cell
6. Continue until all cells have been visited

### Why we chose this algorithm

- Simple to implement and easy to understand
- Naturally produces a perfect maze (one unique path between any two points)
- Works directly on the grid structure without extra data structures
- Reproducible with a seed via `random.Random()`
- Creates long winding corridors that look visually interesting
- Easy to explain and justify during peer evaluation

## Reusable Module

The maze generation logic is packaged as a standalone pip-installable module called `mazegen`.

### What is reusable

The `MazeGenerator` class inside `generator.py` can be imported and used independently in any Python project.


## Team and Project Management

### Roles

| Member | Role |
|--------|------|
| `<meharuty>` | Maze structure, config parser, maze generation algorithm, pathfinding, output writer, reusable package |
| `<ggevorgy>` | Visual representation, user interactions, Makefile, README, testing, packaging setup |

### Anticipated planning and how it evolved

We initially planned to split the work cleanly between core logic and visualization. In practice, the maze structure and generation took longer than expected due to the corridor width restriction and the "42" pattern embedding. We adjusted by tackling those constraints incrementally after getting the basic generation working first.

### What worked well and what could be improved

**Worked well:**
- Using the 4-bit integer wall encoding — it made hex output trivial
- Adding BFS for solving the maze made it easy to verify that the entry and exit were connected
- The provided validation script caught coherence bugs early

**Could be improved:**
- The "42" pattern placement could be more flexible
- The maze generation and post-processing steps could be better separated to make the code easier to maintain
- More generation algorithms could be supported as bonuses

### Tools used

- Python 3.10+
- mypy and flake8 for static analysis and linting
- Claude (AI) — see Resources section

## Resources

GeeksforGeeks – BFS and DFS
Wikipedia - Poetry documentation



### AI usage

Claude (claude.ai) was used during this project for the following:
- Explaining concepts (bit manipulation, DFS vs BFS, maze generation theory)
- Clarifying project requirements from the subject PDF
- Reviewing code logic and catching bugs

All AI-generated explanations were reviewed, understood, and rewritten by the team before being included in the project. No code was copied directly from AI without full understanding.