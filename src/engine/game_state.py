from typing import List, Tuple, Optional, Dict
from src.map.game_map import GameMap
from src.map.tile import Tile, TileType
from src.procedural.dungeon_generator import DungeonGenerator
from src.procedural.room import Room
from src.game.crystal import Crystal, CrystalType
from src.game.sequence import CrystalSequence
import random

class GameState:
    """Manages the game state including map, entities, and game logic.
    
    This class is responsible for:
    - Initializing and managing the game map
    - Managing entities (player, crystals)
    - Handling game logic (crystal sequences, win conditions)
    - Processing player input
    
    Attributes:
        game_map (GameMap): The current game map
        rooms (List[Room]): List of rooms in the dungeon
        player_pos (Tuple[int, int]): Current player position
        crystal_sequence (CrystalSequence): Current crystal sequence to solve
    """
    
    def __init__(self, map_width: int = 80, map_height: int = 50):
        """Initialize a new game state.
        
        Args:
            map_width (int): Width of the game map
            map_height (int): Height of the game map
        """
        # Create the dungeon
        generator = DungeonGenerator(
            map_width=map_width,
            map_height=map_height,
            min_rooms=5,
            max_rooms=8
        )
        self.game_map, self.rooms = generator.generate()
        
        # Initialize crystal sequence
        self.crystal_sequence = CrystalSequence(sequence_length=3)
        
        # Place crystals in rooms
        self._place_crystals()
        
        # Place player in first room
        self.player_pos = self._get_player_start()
    
    def _place_crystals(self) -> None:
        """Place crystals in rooms according to the sequence."""
        # Get the required crystal types from the sequence
        required_types = self.crystal_sequence.target_sequence
        
        # Randomly select rooms for the required crystals
        selected_rooms = random.sample(self.rooms, len(required_types))
        
        # Place required crystals
        for room, crystal_type in zip(selected_rooms, required_types):
            room.add_crystal(crystal_type)
        
        # Add some random crystals to remaining rooms
        remaining_rooms = [r for r in self.rooms if r not in selected_rooms]
        for room in remaining_rooms:
            if random.random() < 0.5:  # 50% chance to add a crystal
                room.add_crystal()
    
    def _get_player_start(self) -> Tuple[int, int]:
        """Get the starting position for the player.
        
        Returns:
            Tuple[int, int]: Starting coordinates (x, y)
        """
        if self.rooms:
            return self.rooms[0].center
        return (self.game_map.width // 2, self.game_map.height // 2)
    
    def move_player(self, dx: int, dy: int) -> bool:
        """Move the player by the given amount.
        
        Args:
            dx (int): Change in x position
            dy (int): Change in y position
            
        Returns:
            bool: True if the move was successful
        """
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        # Check if the move is valid
        if not self.game_map.in_bounds(new_x, new_y):
            return False
        
        tile = self.game_map.get_tile(new_x, new_y)
        if not tile.walkable:
            return False
        
        self.player_pos = (new_x, new_y)
        
        # Check for crystal activation
        self._check_crystal_activation()
        
        return True
    
    def _check_crystal_activation(self) -> None:
        """Check if the player is on a crystal and activate it."""
        # Check each room's crystal
        for room in self.rooms:
            if not room.crystal:
                continue
            
            if room.crystal.position == self.player_pos:
                room.crystal.activate()
                self.crystal_sequence.add_crystal(room.crystal)
    
    def update(self) -> None:
        """Update the game state.
        
        Updates crystal states and sequence progress.
        """
        # Update crystal sequence
        self.crystal_sequence.update()
    
    @property
    def active_crystals(self) -> List[Crystal]:
        """Get list of currently active crystals.
        
        Returns:
            List[Crystal]: Active crystals
        """
        active = []
        for room in self.rooms:
            if room.crystal and room.crystal.is_active:
                active.append(room.crystal)
        return active
    
    @property
    def sequence_progress(self) -> float:
        """Get current sequence completion progress.
        
        Returns:
            float: Progress from 0.0 to 1.0
        """
        return self.crystal_sequence.progress
    
    @property
    def next_crystal_type(self) -> Optional[CrystalType]:
        """Get the next crystal type needed in the sequence.
        
        Returns:
            Optional[CrystalType]: Next crystal type or None if complete
        """
        return self.crystal_sequence.get_next_crystal_type()
    
    @property
    def is_level_complete(self) -> bool:
        """Check if the current level is complete.
        
        Returns:
            bool: True if the crystal sequence is complete
        """
        return self.crystal_sequence.is_complete