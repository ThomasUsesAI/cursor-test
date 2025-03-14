from typing import List, Optional, Tuple, Set, Dict
from src.map.game_map import GameMap
from src.map.tile import Tile, TileType
from src.procedural.room import Room
import random
import math

class DungeonGenerator:
    """Generates dungeon layouts using a room-based approach with guaranteed connectivity.
    
    This generator creates rooms and connects them with corridors to create
    a complete dungeon level. Uses Prim's algorithm to ensure all rooms are
    connected via a minimum spanning tree.
    
    Attributes:
        map_width (int): Width of the game map
        map_height (int): Height of the game map
        min_rooms (int): Minimum number of rooms to generate
        max_rooms (int): Maximum number of rooms to generate
        min_room_size (int): Minimum dimension for rooms
        max_room_size (int): Maximum dimension for rooms
        extra_connections (float): Percentage of extra connections to add (0.0 to 1.0)
    """
    
    def __init__(self, map_width: int, map_height: int,
                 min_rooms: int = 5, max_rooms: int = 10,
                 min_room_size: int = 6, max_room_size: int = 10,
                 extra_connections: float = 0.1):
        """Initialize the dungeon generator.
        
        Args:
            map_width (int): Width of the game map
            map_height (int): Height of the game map
            min_rooms (int): Minimum number of rooms
            max_rooms (int): Maximum number of rooms
            min_room_size (int): Minimum room dimension
            max_room_size (int): Maximum room dimension
            extra_connections (float): Percentage of extra connections (0.0 to 1.0)
        """
        self.map_width = map_width
        self.map_height = map_height
        self.min_rooms = min_rooms
        self.max_rooms = max_rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        self.extra_connections = extra_connections
    
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
                rooms.append(room)
            
            attempts += 1
        
        if rooms:
            # Connect all rooms using minimum spanning tree
            self._connect_rooms(game_map, rooms)
            
            # Add some extra connections for variety
            self._add_extra_connections(game_map, rooms)
        
        return game_map, rooms
    
    def _connect_rooms(self, game_map: GameMap, rooms: List[Room]) -> None:
        """Connect all rooms using Prim's minimum spanning tree algorithm.
        
        Args:
            game_map (GameMap): The game map to modify
            rooms (List[Room]): List of rooms to connect
        """
        if not rooms:
            return
            
        # Track connected rooms
        connected: Set[Room] = {rooms[0]}
        unconnected: Set[Room] = set(rooms[1:])
        
        # Connect all rooms
        while unconnected:
            best_distance = float('inf')
            best_connection = None
            
            # Find the closest unconnected room to any connected room
            for connected_room in connected:
                for unconnected_room in unconnected:
                    dist = self._distance_between(connected_room, unconnected_room)
                    if dist < best_distance:
                        best_distance = dist
                        best_connection = (connected_room, unconnected_room)
            
            if best_connection:
                room1, room2 = best_connection
                self._create_corridor(game_map, room1.center, room2.center)
                connected.add(room2)
                unconnected.remove(room2)
    
    def _add_extra_connections(self, game_map: GameMap,
                             rooms: List[Room]) -> None:
        """Add additional connections between rooms for variety.
        
        Args:
            game_map (GameMap): The game map to modify
            rooms (List[Room]): List of rooms
        """
        # Calculate number of extra connections
        num_extras = int(len(rooms) * self.extra_connections)
        
        # Create a list of all possible connections
        possible_connections = []
        for i, room1 in enumerate(rooms):
            for room2 in rooms[i + 1:]:
                dist = self._distance_between(room1, room2)
                possible_connections.append((dist, room1, room2))
        
        # Sort by distance and add some short connections
        possible_connections.sort()
        for _, room1, room2 in possible_connections[:num_extras]:
            self._create_corridor(game_map, room1.center, room2.center)
    
    def _distance_between(self, room1: Room, room2: Room) -> float:
        """Calculate the Manhattan distance between two rooms' centers.
        
        Args:
            room1 (Room): First room
            room2 (Room): Second room
            
        Returns:
            float: Manhattan distance between room centers
        """
        x1, y1 = room1.center
        x2, y2 = room2.center
        return abs(x2 - x1) + abs(y2 - y1)
    
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
            # Add walls above and below the corridor
            if game_map.get_tile(x, y - 1).type == TileType.VOID:
                game_map.set_tile(x, y - 1, Tile.wall())
            if game_map.get_tile(x, y + 1).type == TileType.VOID:
                game_map.set_tile(x, y + 1, Tile.wall())
    
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
            # Add walls to the sides of the corridor
            if game_map.get_tile(x - 1, y).type == TileType.VOID:
                game_map.set_tile(x - 1, y, Tile.wall())
            if game_map.get_tile(x + 1, y).type == TileType.VOID:
                game_map.set_tile(x + 1, y, Tile.wall())