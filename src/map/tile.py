from enum import Enum
from typing import Tuple

class TileType(Enum):
    """Types of tiles that can exist in the game map."""
    VOID = 0   # Empty space
    WALL = 1   # Wall
    FLOOR = 2  # Floor

class Tile:
    """A single tile in the game map.
    
    Attributes:
        type (TileType): The type of tile
        char (str): Character used to represent the tile
        color (Tuple[int, int, int]): RGB color values
    """
    
    def __init__(self, tile_type: TileType, char: str,
                 color: Tuple[int, int, int]):
        """Initialize a new tile.
        
        Args:
            tile_type (TileType): The type of tile
            char (str): Character used to represent the tile
            color (Tuple[int, int, int]): RGB color values
        """
        self.type = tile_type
        self.char = char
        self.color = color
    
    @property
    def walkable(self) -> bool:
        """Whether entities can walk on this tile.
        
        Returns:
            bool: True if walkable, False otherwise
        """
        return self.type == TileType.FLOOR
    
    @property
    def transparent(self) -> bool:
        """Whether light/sight can pass through this tile.
        
        Returns:
            bool: True if transparent, False otherwise
        """
        return self.type != TileType.WALL
    
    @staticmethod
    def wall() -> 'Tile':
        """Create a wall tile.
        
        Returns:
            Tile: A new wall tile
        """
        return Tile(TileType.WALL, '#', (128, 128, 128))
    
    @staticmethod
    def floor() -> 'Tile':
        """Create a floor tile.
        
        Returns:
            Tile: A new floor tile
        """
        return Tile(TileType.FLOOR, '.', (64, 64, 64))
    
    @staticmethod
    def void() -> 'Tile':
        """Create a void tile.
        
        Returns:
            Tile: A new void tile
        """
        return Tile(TileType.VOID, ' ', (0, 0, 0))