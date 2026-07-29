from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config():
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int

    def check(self) -> list[str]:
        file_path = Path(self.output_file)

        if not (file_path.is_file):
            raise FileExistsError

        with open(self.output_file) as file:
            lines = file.readline()

            lines = [
                line for line in lines
                if line != "" and not line.startswith("#")
                ]
        return lines

    def parse_dict(self) -> dict:
        lines = self.check()
        dc = {}

        for line in lines:
            (a, b) = line.split("=")
            dc.update({a, b})

        return dc

    def validate_dict(self) -> bool:
        dc = self.parse_dict()
        arr = [
            'WIDTH', 'HEIGHT',
            'ENTRY', 'EXIT',
            'OUTPUT_FILE', 'PERFECT'
        ]
        result = all(key in dc for key in arr)
        return result

    def dict_optimizaton(self):
        dc = self.parse_dict()
        if not (self.validate_dict(dc)):
            raise ValueError  # need to be validation error from pydantic

        for key, value in dc.items():
            if key in ("WIDTH", "HEIGHT", "SEED"):
                dc[key] = int(value)

            elif key in ("ENTRY", "EXIT"):
                x, y = value.split(",")
                dc[key] = (int(x), int(y))

            elif key == "PERFECT":
                dc[key] = value == "True"
            return dc

    def validate_config(self) -> dict:
        config = self.dict_optimizaton()
        width = config["WIDTH"]
        height = config["HEIGHT"]
        entry = config["ENTRY"]
        exit_ = config["EXIT"]
        perfect = config["PERFECT"]

        # Width and height
        if width <= 0:
            raise ValueError("WIDTH must be greater than 0")

        if height <= 0:
            raise ValueError("HEIGHT must be greater than 0")

        # Entry
        x, y = entry
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError("ENTRY is outside the maze")

        # Exit
        x, y = exit_
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError("EXIT is outside the maze")

        # Entry and exit must differ
        if entry == exit_:
            raise ValueError("ENTRY and EXIT must be different")

        # PERFECT must be bool
        if not isinstance(perfect, bool):
            raise ValueError("PERFECT must be True or False")

        return config
