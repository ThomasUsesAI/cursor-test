from typing import List, Optional, Tuple
import time
from src.map.game_map import GameMap
from src.procedural.dungeon_generator import DungeonGenerator
from src.game.crystal import Crystal, CrystalType
from src.game.sequence import CrystalSequence
from src.game.abilities import AbilityManager

class Entity:
    """Base class for all game entities.
    
    Attributes:
        x (int): X position on map
        y (int): Y position on map
        char (str): Character used to represent entity
        color (tuple): RGB color tuple
    """
    
    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

class Player(Entity):
    """Player entity with movement and abilities.
    
    Attributes:
        last_move (float): Timestamp of last movement
        move_cooldown (float): Time between movements
        abilities (AbilityManager): Player's unlocked abilities
    """
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, '@', (0, 255, 255))  # Cyan color
        self.last_move = 0.0
        self.move_cooldown = 0.1  # 0.1 second between moves
        self.abilities = AbilityManager()

class GameState:
    """Manages the game state including map, entities, and game logic.
    
    Attributes:
        game_map (GameMap): Current game map
        entities (List[Entity]): List of all entities
        player (Player): The player entity
        sequence (CrystalSequence): Crystal activation sequence tracker
    """
    
    def __init__(self, map_width: int, map_height: int):
        """Initialize a new game state.
        
        Args:
            map_width (int): Width of the game map
            map_height (int): Height of the game map
        """
        # Generate initial dungeon
        generator = DungeonGenerator(map_width, map_height)
        self.game_map, self.rooms = generator.generate()
        
        self.entities: List[Entity] = []
        self.player: Optional[Player] = None
        self.sequence = CrystalSequence()
        
        # Create player in first room center
        self._create_player()
    
    def _create_player(self) -> None:
        """Create the player entity in the center of the first room."""
        if self.rooms:
            room = self.rooms[0]
            x = room.x + room.width // 2
            y = room.y + room.height // 2
        else:
            # Fallback to map center if no rooms
            x = self.game_map.width // 2
            y = self.game_map.height // 2
        
        self.player = Player(x, y)
        self.entities.append(self.player)
    
    def move_player(self, dx: int, dy: int) -> bool:
        """Move the player if the movement is valid.
        
        Args:
            dx (int): X direction (-1, 0, 1)
            dy (int): Y direction (-1, 0, 1)
            
        Returns:
            bool: True if movement was successful
        """
        if not self.player:
            return False
        
        # Check movement cooldown
        current_time = time.time()
        if current_time - self.player.last_move < self.player.move_cooldown:
            return False
        
        # Get target position
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        # Check if movement is valid
        if not self.game_map.in_bounds(new_x, new_y):
            return False
        
        tile = self.game_map.get_tile(new_x, new_y)
        if not tile.walkable:
            return False
        
        # Move player
        self.player.x = new_x
        self.player.y = new_y
        self.player.last_move = current_time
        return True
    
    def use_ability(self, crystal_type: CrystalType, dx: int, dy: int) -> bool:
        """Use the ability associated with a crystal type.
        
        Args:
            crystal_type (CrystalType): Type of crystal ability to use
            dx (int): X direction (-1, 0, 1)
            dy (int): Y direction (-1, 0, 1)
            
        Returns:
            bool: True if ability was used successfully
        """
        if not self.player:
            return False
        
        ability = self.player.abilities.get_ability(crystal_type)
        if not ability or not ability.is_unlocked or not ability.can_use():
            return False
        
        # Handle dash ability
        if crystal_type == CrystalType.RED:  # Heat crystal
            target_x, target_y = ability.get_dash_target(dx, dy, self.player.x, self.player.y)
            
            # Check if path is clear
            for i in range(1, ability.distance + 1):
                check_x = self.player.x + (dx * i)
                check_y = self.player.y + (dy * i)
                
                if not self.game_map.in_bounds(check_x, check_y):
                    target_x = check_x - dx
                    target_y = check_y - dy
                    break
                
                tile = self.game_map.get_tile(check_x, check_y)
                if not tile.walkable:
                    target_x = check_x - dx
                    target_y = check_y - dy
                    break
            
            # Move player to final position
            self.player.x = target_x
            self.player.y = target_y
            ability.use()
            return True
        
        return False
    
    def activate_crystal(self, crystal: Crystal) -> bool:
        """Activate a crystal and check sequence.
        
        Args:
            crystal (Crystal): Crystal being activated
            
        Returns:
            bool: True if activation was valid
        """
        if not crystal.is_active:
            crystal.activate()
            
            # Check sequence and unlock ability if completed
            if self.sequence.add_crystal(crystal):
                if crystal.crystal_type in self.sequence.completed_types:
                    self.player.abilities.unlock_ability(crystal.crystal_type)
                return True
        
        return False
    
    def update(self) -> None:
        """Update game state."""
        # Update sequence
        self.sequence.update()