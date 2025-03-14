from dataclasses import dataclass
from typing import Tuple
from enum import Enum, auto

class TileType(Enum):
    """Enumeration of possible tile types in the game.
    
    Each tile type has different properties and interactions:
    - FLOOR: Can be walked on
    - WALL: Blocks movement and sight
    - DOOR: Can be opened/closed
    - VOID: Out of bounds/not generated
    """
    FLOOR = auto()
    WALL = auto()
    DOOR = auto()
    VOID = auto()

@dataclass
class Tile:
    """Represents a single tile in the game map.
    
    Attributes:
        type (TileType): The type of tile
        blocks_movement (bool): Whether entities can move through this tile
        blocks_sight (bool): Whether this tile blocks line of sight
        explored (bool): Whether the player has seen this tile
        visible (bool): Whether the tile is currently visible
        char (str): Character representation of the tile
        color (Tuple[int, int, int]): RGB color of the tile
    """
    type: TileType
    blocks_movement: bool = False
    blocks_sight: bool = False
    explored: bool = False
    visible: bool = False
    char: str = '.'
    color: Tuple[int, int, int] = (255, 255, 255)  # White
    
    @classmethod
    def floor(cls) -> 'Tile':
        """Create a floor tile."""
        return cls(
            type=TileType.FLOOR,
            blocks_movement=False,
            blocks_sight=False,
            char='.',
            color=(64, 64, 64)  # Dark gray
        )
    
    @classmethod
    def wall(cls) -> 'Tile':
        """Create a wall tile."""
        return cls(
            type=TileType.WALL,
            blocks_movement=True,
            blocks_sight=True,
            char='#',
            color=(128, 128, 128)  # Gray
        )
    
    @classmethod
    def door(cls) -> 'Tile':
        """Create a door tile."""
        return cls(
            type=TileType.DOOR,
            blocks_movement=True,
            blocks_sight=True,
            char='+',
            color=(139, 69, 19)  # Brown
        )
    
    @classmethod
    def void(cls) -> 'Tile':
        """Create a void tile."""
        return cls(
            type=TileType.VOID,
            blocks_movement=True,
            blocks_sight=True,
            char=' ',
            color=(0, 0, 0)  # Black
        )