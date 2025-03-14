from enum import Enum
from typing import Tuple, Optional
import time

class CrystalType(Enum):
    """Types of Resonance Crystals with their corresponding colors."""
    RED = ('R', (255, 50, 50))     # Heat
    BLUE = ('B', (50, 50, 255))    # Frost
    GREEN = ('G', (50, 255, 50))   # Growth
    PURPLE = ('P', (255, 50, 255)) # Void
    YELLOW = ('Y', (255, 255, 50)) # Lightning

class Crystal:
    """A Resonance Crystal that can be activated in sequence.
    
    Attributes:
        crystal_type (CrystalType): The type of crystal
        position (Tuple[int, int]): Position in the game map
        is_active (bool): Whether the crystal is currently activated
        activation_time (float): When the crystal was last activated
        duration (float): How long the crystal stays active
    """
    
    def __init__(self, crystal_type: CrystalType, position: Tuple[int, int],
                 duration: float = 30.0):
        """Initialize a new crystal.
        
        Args:
            crystal_type (CrystalType): Type of the crystal
            position (Tuple[int, int]): Position in the game map
            duration (float): How long the crystal stays active in seconds
        """
        self.crystal_type = crystal_type
        self.position = position
        self.is_active = False
        self.activation_time: Optional[float] = None
        self.duration = duration
    
    def activate(self) -> None:
        """Activate the crystal, starting its effect timer."""
        self.is_active = True
        self.activation_time = time.time()
    
    def deactivate(self) -> None:
        """Deactivate the crystal, ending its effects."""
        self.is_active = False
        self.activation_time = None
    
    def update(self) -> None:
        """Update the crystal's state based on time.
        
        Deactivates the crystal if its duration has expired.
        """
        if (self.is_active and self.activation_time and 
            time.time() - self.activation_time > self.duration):
            self.deactivate()
    
    @property
    def time_remaining(self) -> Optional[float]:
        """Get the remaining active time in seconds.
        
        Returns:
            Optional[float]: Seconds remaining or None if inactive
        """
        if not self.is_active or not self.activation_time:
            return None
        
        remaining = self.duration - (time.time() - self.activation_time)
        return max(0.0, remaining)
    
    @property
    def symbol(self) -> str:
        """Get the display symbol for this crystal.
        
        Returns:
            str: The crystal's symbol
        """
        return self.crystal_type.value[0]
    
    @property
    def color(self) -> Tuple[int, int, int]:
        """Get the display color for this crystal.
        
        Returns:
            Tuple[int, int, int]: RGB color values
        """
        return self.crystal_type.value[1]