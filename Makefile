.PHONY: install run debug clean lint lint-strict

install:
	poetry install

run:
	poetry run python3 a_maze_ing.py config_right.txt

debug:
	poetry run python3 -m pdb a_maze_ing.py config_right.txt

clean:
	rm -rf maze/__pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache

lint:
	flake8 .
	mypy . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
