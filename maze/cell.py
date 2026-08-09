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
