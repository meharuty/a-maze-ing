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

    def get_bitmask(self) -> int:
        mask = 0

        if self.north:
            mask |= 1
        if self.east:
            mask |= 2
        if self.south:
            mask |= 4
        if self.west:
            mask |= 8

        return mask

    def __repr__(self) -> str:
        return (
            f"Cell({self.x}, {self.y}, "
            f"N={self.north}, "
            f"E={self.east}, "
            f"S={self.south}, "
            f"W={self.west})"
        )
