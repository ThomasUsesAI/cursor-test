from typing import List, Optional, Tuple
from src.map.tile import Tile, TileType

class GameMap:
    """Represents the game map grid and provides map manipulation methods.
    
    The map is a 2D grid of tiles that can be modified and queried. It handles
    the storage and basic operations on the map tiles.
    
    Attributes:
        width (int): Width of the map in tiles
        height (int): Height of the map in tiles
        tiles (List[List[Tile]]): 2D grid of tiles
    """
    
    def __init__(self, width: int, height: int):
        """Initialize a new map filled with void tiles.
        
        Args:
            width (int): Width of the map in tiles
            height (int): Height of the map in tiles
        """
        self.width = width
        self.height = height
        self.tiles = [[Tile.void() for y in range(height)] for x in range(width)]
    
    def in_bounds(self, x: int, y: int) -> bool:
        """Check if the given coordinates are within the map bounds.
        
        Args:
            x (int): X coordinate to check
            y (int): Y coordinate to check
            
        Returns:
            bool: True if the coordinates are within bounds
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """Get the tile at the specified coordinates.
        
        Args:
            x (int): X coordinate of the tile
            y (int): Y coordinate of the tile
            
        Returns:
            Optional[Tile]: The tile at the coordinates, or None if out of bounds
        """
        if self.in_bounds(x, y):
            return self.tiles[x][y]
        return None
    
    def set_tile(self, x: int, y: int, tile: Tile) -> bool:
        """Set the tile at the specified coordinates.
        
        Args:
            x (int): X coordinate to set
            y (int): Y coordinate to set
            tile (Tile): The tile to place
            
        Returns:
            bool: True if the tile was set successfully
        """
        if self.in_bounds(x, y):
            self.tiles[x][y] = tile
            return True
        return False
    
    def clear_map(self) -> None:
        """Reset the map to all void tiles."""
        for x in range(self.width):
            for y in range(self.height):
                self.tiles[x][y] = Tile.void()
    
    def count_neighbors(self, x: int, y: int, tile_type: TileType) -> int:
        """Count neighboring tiles of a specific type.
        
        Args:
            x (int): X coordinate of the center tile
            y (int): Y coordinate of the center tile
            tile_type (TileType): Type of tile to count
            
        Returns:
            int: Number of neighboring tiles of the specified type
        """
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                new_x, new_y = x + dx, y + dy
                tile = self.get_tile(new_x, new_y)
                if tile and tile.type == tile_type:
                    count += 1
        return count