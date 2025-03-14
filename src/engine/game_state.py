from typing import Dict, Type, Optional
from src.components.position import Position
from src.components.renderable import Renderable
from src.components.player import Player
from src.systems.movement_system import MovementSystem

class GameState:
    """Manages the current state of the game, including entities and systems."""
    
    def __init__(self, map_width: int = 80, map_height: int = 60):
        """Initialize the game state.
        
        Args:
            map_width (int): Width of the game map
            map_height (int): Height of the game map
        """
        self.map_width = map_width
        self.map_height = map_height
        self.entities: Dict[int, Dict[Type, object]] = {}
        self.player_id: Optional[int] = None
        
        # Initialize systems
        self.movement_system = MovementSystem(map_width, map_height)
        
        # Create player
        self._create_player()
    
    def _create_player(self) -> None:
        """Create the player entity with necessary components."""
        player_components = {
            Position: Position(self.map_width // 2, self.map_height // 2),
            Renderable: Renderable('@', (0, 255, 255)),  # Cyan color
            Player: Player()
        }
        
        # Generate a unique entity ID
        entity_id = len(self.entities)
        self.entities[entity_id] = player_components
        self.player_id = entity_id
    
    def move_player(self, dx: int, dy: int) -> bool:
        """Attempt to move the player by the given delta.
        
        Args:
            dx (int): Change in x-coordinate
            dy (int): Change in y-coordinate
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        if self.player_id is None:
            return False
            
        player_pos = self.entities[self.player_id][Position]
        new_x = player_pos.x + dx
        new_y = player_pos.y + dy
        
        if self.movement_system.is_valid_move(new_x, new_y):
            player_pos.move(dx, dy)
            return True
        
        return False
    
    def update(self) -> None:
        """Update game state for the current frame."""
        self.movement_system.update(self.entities)