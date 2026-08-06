from pathlib import Path


class ConfigParser:
    def __init__(self, filename):
        self.filename = filename

    def check(self) -> list[str]:
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
        lines = self.check()
        dc = {}

        for line in lines:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            dc[key] = value

        return dc

    def validate_dict(self, dc: dict[str, str]) -> bool:
        arr = [
            'WIDTH', 'HEIGHT',
            'ENTRY', 'EXIT',
            'OUTPUT_FILE', 'PERFECT'
        ]
        result = all(key in dc for key in arr)
        return result

    def dict_optimization(self) -> dict:
        dc = self.parse_dict()
        if not (self.validate_dict(dc)):
            raise ValueError  # need to be validation error from pydantic

        for key, value in dc.items():
            if key in ("WIDTH", "HEIGHT", "SEED"):
                try:
                    dc[key] = int(value)
                except ValueError:
                    raise ValueError(f"{key} must be an integer")

            elif key in ("ENTRY", "EXIT"):
                try:
                    x, y = value.split(",")
                    dc[key] = (int(x.strip()), int(y.strip()))
                except ValueError:
                    raise ValueError(f"{key} must be in the format x,y")
            elif key == "PERFECT":
                if value == "True":
                    dc[key] = True
                elif value == "False":
                    dc[key] = False
                else:
                    raise ValueError("PERFECT must be True or False")
        if "SEED" not in dc:
            dc["SEED"] = None
        return dc

    def validate_config(self) -> dict:
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

    def parse(self):
        return self.validate_config()
