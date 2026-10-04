from dataclasses import dataclass


@dataclass
class Cell:
    """Represent a single cell in the maze."""

    x: int
    y: int

    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True

    visited: bool = False

    def get_bitmask(self) -> int:
        """
        Return the bitmask representing the cell's walls.

        Each wall is represented by one bit:
        north=1, east=2, south=4, west=8.

        Returns:
            int: The bitmask of the cell's walls.
        """

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
