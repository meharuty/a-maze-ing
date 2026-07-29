from dataclasses import dataclass


@dataclass
class Cell:
    x: int
    y: int

    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True

    visited: bool = False

    def __repr__(self) -> str:
        return (
            f"Cell({self.x}, {self.y}, "
            f"N={self.north}, "
            f"E={self.east}, "
            f"S={self.south}, "
            f"W={self.west})"
        )
