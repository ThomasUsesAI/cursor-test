from typing import List, Optional, Tuple
from src.map.game_map import GameMap
from src.map.tile import Tile
from src.procedural.room import Room
import random

class DungeonGenerator:
    """Generates dungeon layouts using a room-based approach.
    
    This generator creates rooms and connects them with corridors to create
    a complete dungeon level.
    
    Attributes:
        map_width (int): Width of the game map
        map_height (int): Height of the game map
        min_rooms (int): Minimum number of rooms to generate
        max_rooms (int): Maximum number of rooms to generate
        min_room_size (int): Minimum dimension for rooms
        max_room_size (int): Maximum dimension for rooms
    """
    
    def __init__(self, map_width: int, map_height: int,
                 min_rooms: int = 5, max_rooms: int = 10,
                 min_room_size: int = 6, max_room_size: int = 10):
        """Initialize the dungeon generator.
        
        Args:
            map_width (int): Width of the game map
            map_height (int): Height of the game map
            min_rooms (int): Minimum number of rooms
            max_rooms (int): Maximum number of rooms
            min_room_size (int): Minimum room dimension
            max_room_size (int): Maximum room dimension
        """
        self.map_width = map_width
        self.map_height = map_height
        self.min_rooms = min_rooms
        self.max_rooms = max_rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
    
    def generate(self) -> Tuple[GameMap, List[Room]]:
        """Generate a new dungeon level.
        
        Returns:
            Tuple[GameMap, List[Room]]: The generated map and list of rooms
        """
        game_map = GameMap(self.map_width, self.map_height)
        rooms: List[Room] = []
        
        # Determine number of rooms to create
        num_rooms = random.randint(self.min_rooms, self.max_rooms)
        
        # Try to place rooms
        attempts = 0
        max_attempts = 100  # Prevent infinite loops
        
        while len(rooms) < num_rooms and attempts < max_attempts:
            room = Room.create_random(
                self.map_width,
                self.map_height,
                self.min_room_size,
                self.max_room_size
            )
            
            if room is None:
                attempts += 1
                continue
            
            # Check if room intersects with any existing rooms
            intersects = False
            for other_room in rooms:
                if room.intersects(other_room):
                    intersects = True
                    break
            
            if not intersects:
                room.place_in_map(game_map)
                if rooms:  # Connect to previous room
                    self._create_corridor(game_map,
                                        rooms[-1].center,
                                        room.center)
                rooms.append(room)
            
            attempts += 1
        
        return game_map, rooms
    
    def _create_corridor(self, game_map: GameMap,
                        start: Tuple[int, int],
                        end: Tuple[int, int]) -> None:
        """Create a corridor between two points.
        
        Args:
            game_map (GameMap): The game map to modify
            start (Tuple[int, int]): Starting coordinates (x, y)
            end (Tuple[int, int]): Ending coordinates (x, y)
        """
        x1, y1 = start
        x2, y2 = end
        
        # Randomly choose which direction to go first
        if random.random() < 0.5:
            # First horizontal, then vertical
            self._create_h_tunnel(game_map, x1, x2, y1)
            self._create_v_tunnel(game_map, y1, y2, x2)
        else:
            # First vertical, then horizontal
            self._create_v_tunnel(game_map, y1, y2, x1)
            self._create_h_tunnel(game_map, x1, x2, y2)
    
    def _create_h_tunnel(self, game_map: GameMap,
                        x1: int, x2: int, y: int) -> None:
        """Create a horizontal tunnel.
        
        Args:
            game_map (GameMap): The game map to modify
            x1 (int): Starting x coordinate
            x2 (int): Ending x coordinate
            y (int): Y coordinate of the tunnel
        """
        for x in range(min(x1, x2), max(x1, x2) + 1):
            game_map.set_tile(x, y, Tile.floor())
    
    def _create_v_tunnel(self, game_map: GameMap,
                        y1: int, y2: int, x: int) -> None:
        """Create a vertical tunnel.
        
        Args:
            game_map (GameMap): The game map to modify
            y1 (int): Starting y coordinate
            y2 (int): Ending y coordinate
            x (int): X coordinate of the tunnel
        """
        for y in range(min(y1, y2), max(y1, y2) + 1):
            game_map.set_tile(x, y, Tile.floor())