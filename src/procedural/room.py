from typing import Tuple, Optional
from src.map.game_map import GameMap
from src.map.tile import Tile
import random

class Room:
    """Represents a rectangular room in the dungeon.
    
    A room is defined by its position (top-left corner) and dimensions.
    The room can be placed in a game map and provides methods for checking
    intersections with other rooms.
    
    Attributes:
        x (int): X coordinate of top-left corner
        y (int): Y coordinate of top-left corner
        width (int): Width of the room
        height (int): Height of the room
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """Initialize a new room.
        
        Args:
            x (int): X coordinate of top-left corner
            y (int): Y coordinate of top-left corner
            width (int): Width of the room
            height (int): Height of the room
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    @property
    def center(self) -> Tuple[int, int]:
        """Get the center coordinates of the room.
        
        Returns:
            Tuple[int, int]: (x, y) coordinates of room center
        """
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        return (center_x, center_y)
    
    def intersects(self, other: 'Room', buffer: int = 1) -> bool:
        """Check if this room intersects with another room.
        
        Args:
            other (Room): The other room to check against
            buffer (int): Extra space to maintain between rooms
            
        Returns:
            bool: True if rooms intersect (including buffer), False otherwise
        """
        return (self.x - buffer <= other.x + other.width and
                self.x + self.width + buffer >= other.x and
                self.y - buffer <= other.y + other.height and
                self.y + self.height + buffer >= other.y)
    
    def place_in_map(self, game_map: GameMap) -> None:
        """Place this room in the game map.
        
        Creates floor tiles for the room interior and wall tiles around
        the perimeter.
        
        Args:
            game_map (GameMap): The game map to place the room in
        """
        # Create floor tiles for room interior
        for x in range(self.x, self.x + self.width):
            for y in range(self.y, self.y + self.height):
                game_map.set_tile(x, y, Tile.floor())
        
        # Create walls around the room
        for x in range(self.x - 1, self.x + self.width + 1):
            if game_map.get_tile(x, self.y - 1).type == TileType.VOID:
                game_map.set_tile(x, self.y - 1, Tile.wall())
            if game_map.get_tile(x, self.y + self.height).type == TileType.VOID:
                game_map.set_tile(x, self.y + self.height, Tile.wall())
        
        for y in range(self.y - 1, self.y + self.height + 1):
            if game_map.get_tile(self.x - 1, y).type == TileType.VOID:
                game_map.set_tile(self.x - 1, y, Tile.wall())
            if game_map.get_tile(self.x + self.width, y).type == TileType.VOID:
                game_map.set_tile(self.x + self.width, y, Tile.wall())
    
    @staticmethod
    def create_random(map_width: int, map_height: int,
                     min_size: int, max_size: int) -> Optional['Room']:
        """Create a random room within the given constraints.
        
        Args:
            map_width (int): Width of the game map
            map_height (int): Height of the game map
            min_size (int): Minimum room dimension
            max_size (int): Maximum room dimension
            
        Returns:
            Optional[Room]: A new room if one could be created, None otherwise
        """
        width = random.randint(min_size, max_size)
        height = random.randint(min_size, max_size)
        
        # Account for walls
        max_x = map_width - width - 2
        max_y = map_height - height - 2
        
        if max_x <= 2 or max_y <= 2:
            return None
        
        x = random.randint(2, max_x)
        y = random.randint(2, max_y)
        
        return Room(x, y, width, height)
    
    def __eq__(self, other: object) -> bool:
        """Check if two rooms are equal.
        
        Args:
            other (object): The other room to compare with
            
        Returns:
            bool: True if rooms have same position and dimensions
        """
        if not isinstance(other, Room):
            return NotImplemented
        return (self.x == other.x and self.y == other.y and
                self.width == other.width and self.height == other.height)
    
    def __hash__(self) -> int:
        """Generate a hash value for the room.
        
        Returns:
            int: Hash value based on room position and dimensions
        """
        return hash((self.x, self.y, self.width, self.height))