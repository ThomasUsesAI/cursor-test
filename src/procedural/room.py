from dataclasses import dataclass
from typing import List, Tuple, Optional
from src.map.game_map import GameMap
from src.map.tile import Tile
import random

@dataclass
class Room:
    """Represents a rectangular room in the game map.
    
    A room is defined by its position (top-left corner) and dimensions.
    It can be placed on the map and connected to other rooms.
    
    Attributes:
        x (int): X coordinate of the top-left corner
        y (int): Y coordinate of the top-left corner
        width (int): Width of the room
        height (int): Height of the room
    """
    x: int
    y: int
    width: int
    height: int
    
    @property
    def center(self) -> Tuple[int, int]:
        """Get the center coordinates of the room.
        
        Returns:
            Tuple[int, int]: (x, y) coordinates of the room's center
        """
        return (self.x + self.width // 2,
                self.y + self.height // 2)
    
    def intersects(self, other: 'Room') -> bool:
        """Check if this room intersects with another room.
        
        Args:
            other (Room): The other room to check against
            
        Returns:
            bool: True if the rooms intersect
        """
        return (self.x <= other.x + other.width and
                self.x + self.width >= other.x and
                self.y <= other.y + other.height and
                self.y + self.height >= other.y)
    
    def place_in_map(self, game_map: GameMap) -> None:
        """Place this room in the game map.
        
        Args:
            game_map (GameMap): The game map to place the room in
        """
        # Fill room interior with floor tiles
        for x in range(self.x + 1, self.x + self.width - 1):
            for y in range(self.y + 1, self.y + self.height - 1):
                game_map.set_tile(x, y, Tile.floor())
        
        # Place walls around the room
        for x in range(self.x, self.x + self.width):
            game_map.set_tile(x, self.y, Tile.wall())
            game_map.set_tile(x, self.y + self.height - 1, Tile.wall())
        
        for y in range(self.y, self.y + self.height):
            game_map.set_tile(self.x, y, Tile.wall())
            game_map.set_tile(self.x + self.width - 1, y, Tile.wall())

    @staticmethod
    def create_random(map_width: int, map_height: int,
                     min_size: int = 6, max_size: int = 10) -> Optional['Room']:
        """Create a random room within the given map dimensions.
        
        Args:
            map_width (int): Width of the game map
            map_height (int): Height of the game map
            min_size (int): Minimum room dimension
            max_size (int): Maximum room dimension
            
        Returns:
            Optional[Room]: A new room, or None if room couldn't be placed
        """
        width = random.randint(min_size, max_size)
        height = random.randint(min_size, max_size)
        
        # Make sure the room fits in the map with a 1-tile border
        if width >= map_width - 2 or height >= map_height - 2:
            return None
        
        x = random.randint(1, map_width - width - 1)
        y = random.randint(1, map_height - height - 1)
        
        return Room(x, y, width, height)