from typing import Optional, Tuple
import time
from src.game.crystal import CrystalType

class Ability:
    """Base class for all abilities.
    
    Attributes:
        cooldown (float): Time in seconds between uses
        last_use (float): Timestamp of last use
        is_unlocked (bool): Whether this ability is available
    """
    
    def __init__(self, cooldown: float = 1.0):
        """Initialize a new ability.
        
        Args:
            cooldown (float): Cooldown time in seconds
        """
        self.cooldown = cooldown
        self.last_use = 0.0
        self.is_unlocked = False
    
    def can_use(self) -> bool:
        """Check if the ability can be used.
        
        Returns:
            bool: True if enough time has passed since last use
        """
        return time.time() - self.last_use >= self.cooldown
    
    def use(self) -> None:
        """Use the ability and start its cooldown."""
        self.last_use = time.time()

class Dash(Ability):
    """Heat Crystal ability - Quick dash in movement direction.
    
    Attributes:
        distance (int): Number of tiles to dash
        crystal_type (CrystalType): Associated crystal type
    """
    
    def __init__(self):
        """Initialize the dash ability."""
        super().__init__(cooldown=0.5)  # 0.5 second cooldown
        self.distance = 3  # Dash 3 tiles
        self.crystal_type = CrystalType.RED  # Heat crystal
    
    def get_dash_target(self, dx: int, dy: int, x: int, y: int) -> Tuple[int, int]:
        """Calculate the target position for the dash.
        
        Args:
            dx (int): Movement direction X
            dy (int): Movement direction Y
            x (int): Current position X
            y (int): Current position Y
            
        Returns:
            Tuple[int, int]: Target position (x, y)
        """
        # Scale the movement by dash distance
        target_x = x + (dx * self.distance)
        target_y = y + (dy * self.distance)
        return target_x, target_y

class AbilityManager:
    """Manages all player abilities.
    
    Attributes:
        abilities (dict): Map of crystal types to abilities
    """
    
    def __init__(self):
        """Initialize the ability manager."""
        self.abilities = {
            CrystalType.RED: Dash(),  # Heat crystal dash
            # More abilities will be added in future chunks
        }
    
    def unlock_ability(self, crystal_type: CrystalType) -> None:
        """Unlock the ability for a crystal type.
        
        Args:
            crystal_type (CrystalType): Type of crystal completed
        """
        if crystal_type in self.abilities:
            self.abilities[crystal_type].is_unlocked = True
    
    def get_ability(self, crystal_type: CrystalType) -> Optional[Ability]:
        """Get the ability associated with a crystal type.
        
        Args:
            crystal_type (CrystalType): Type of crystal
            
        Returns:
            Optional[Ability]: The ability or None if not found
        """
        return self.abilities.get(crystal_type)