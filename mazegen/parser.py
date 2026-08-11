from pathlib import Path
from typing import Any


class ConfigParser:
    """Parse and validate maze configuration files."""

    def __init__(self, filename: str) -> None:
        """Initialize the configuration parser.

        Args:
            filename: Path to the configuration file.
        """
        self.filename = filename

    def check(self) -> list[str]:
        """Read and clean the configuration file.
        Empty lines and comments are removed from the file.

        Returns:
            A list of non-empty, non-comment configuration lines.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the configuration file is empty.
        """

        file_path = Path(self.filename)

        if not (file_path.is_file()):
            raise FileNotFoundError

        with open(self.filename) as file:
            lines = file.readlines()

            lines = [
                line.strip()
                for line in lines
                if line.strip() and not line.strip().startswith("#")
            ]
            if not lines:
                raise ValueError("Configuration file is empty.")

        return lines

    def parse_dict(self) -> dict[str, str]:
        """Parse configuration lines into a dictionary.

        Returns:
            A dictionary containing configuration keys and values.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the file is empty or contains duplicate keys.
            FileExistsError: If OUTPUT_FILE is empty.
        """

        lines = self.check()
        dc = {}

        for line in lines:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key in dc:
                raise ValueError("Duplicate key")
            dc[key] = value
        if not dc["OUTPUT_FILE"]:
            raise FileExistsError  # maybe I will find better erropr kind

        return dc

    def validate_dict(self, dc: dict[str, str]) -> bool:
        """Check that configuration keys are valid and complete.

        Args:
            dc: Configuration dictionary to validate.

        Returns:
            True if all mandatory keys are present.

        Raises:
            ValueError: If an unknown configuration key is found.
        """

        arr = [
            'WIDTH', 'HEIGHT',
            'ENTRY', 'EXIT',
            'OUTPUT_FILE', 'PERFECT'
        ]
        arr2 = [
            'WIDTH', 'HEIGHT',
            'ENTRY', 'EXIT',
            'OUTPUT_FILE', 'PERFECT', 'SEED'
        ]
        result = all(key in dc for key in arr)
        for key in dc:
            if key not in arr2:
                raise ValueError("Unknown key")
        return result

    def dict_optimization(self) -> dict[str, Any]:
        """Convert configuration values to their appropriate types.

        Integer values are converted to integers, coordinates to tuples,
        and the PERFECT value to a boolean. A missing SEED is set to None.

        Returns:
            A dictionary containing typed configuration values.

        Raises:
            ValueError: If a configuration value has an invalid format."""
        dc = self.parse_dict()
        if not (self.validate_dict(dc)):
            raise ValueError  # need to be validation error from pydantic

        for key, value in dc.items():
            if key in ("WIDTH", "HEIGHT", "SEED"):
                try:
                    dc[key] = int(value)   # type: ignore
                except ValueError:
                    raise ValueError(f"{key} must be an integer")

            elif key in ("ENTRY", "EXIT"):
                try:
                    x, y = value.split(",")
                    dc[key] = (int(x.strip()), int(y.strip()))  # type:ignore
                except ValueError:
                    raise ValueError(f"{key} must be in the format x,y")
            elif key == "PERFECT":
                if value == "True":
                    dc[key] = True   # type: ignore
                elif value == "False":
                    dc[key] = False   # type: ignore
                else:
                    raise ValueError("PERFECT must be True or False")
        if "SEED" not in dc:
            dc["SEED"] = None   # type: ignore
        return dc

    def validate_config(self) -> dict[str, Any]:
        """Validate maze dimensions and entry and exit coordinates.

        Returns:
            A validated configuration dictionary.

        Raises:
            ValueError: If dimensions are invalid,
            coordinates are outside the maze, or entry and exit are identical.
        """

        config = self.dict_optimization()
        width = config["WIDTH"]
        height = config["HEIGHT"]
        entry = config["ENTRY"]
        exit_ = config["EXIT"]

        if width <= 0:
            raise ValueError("WIDTH must be greater than 0")

        if height <= 0:
            raise ValueError("HEIGHT must be greater than 0")

        x, y = entry
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError("ENTRY is outside the maze")

        x, y = exit_
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError("EXIT is outside the maze")

        if entry == exit_:
            raise ValueError("ENTRY and EXIT must be different")

        return config

    def parse(self) -> dict[str, Any]:
        """Parse and fully validate the configuration file.

        Returns:
            A dictionary containing the validated maze configuration.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If any configuration value or setting is invalid.
        """
        return self.validate_config()
