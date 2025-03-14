from typing import List, Optional
from src.game.crystal import Crystal, CrystalType
import random

class CrystalSequence:
    """Tracks and validates crystal activation sequences.
    
    This class manages the target sequence of crystals that need to be
    activated and tracks the player's progress towards completing it.
    
    Attributes:
        target_sequence (List[CrystalType]): The sequence to match
        current_sequence (List[Crystal]): Currently activated crystals
        max_sequence_length (int): Maximum length of the sequence
    """
    
    def __init__(self, sequence_length: int = 3):
        """Initialize a new crystal sequence tracker.
        
        Args:
            sequence_length (int): Length of the sequence to generate
        """
        self.max_sequence_length = sequence_length
        self.target_sequence: List[CrystalType] = []
        self.current_sequence: List[Crystal] = []
        self._generate_sequence()
    
    def _generate_sequence(self) -> None:
        """Generate a new random target sequence."""
        self.target_sequence = []
        crystal_types = list(CrystalType)
        
        for _ in range(self.max_sequence_length):
            crystal_type = random.choice(crystal_types)
            self.target_sequence.append(crystal_type)
    
    def add_crystal(self, crystal: Crystal) -> bool:
        """Add a crystal to the current sequence.
        
        Args:
            crystal (Crystal): The crystal being activated
            
        Returns:
            bool: True if the crystal matches the next in sequence
        """
        # Remove any inactive crystals from the current sequence
        self.current_sequence = [c for c in self.current_sequence if c.is_active]
        
        # Check if this activation matches the sequence
        current_pos = len(self.current_sequence)
        if current_pos >= len(self.target_sequence):
            return False
        
        if crystal.crystal_type == self.target_sequence[current_pos]:
            self.current_sequence.append(crystal)
            return True
        
        # Wrong crystal - reset sequence
        self.current_sequence = []
        return False
    
    @property
    def is_complete(self) -> bool:
        """Check if the current sequence matches the target.
        
        Returns:
            bool: True if the sequence is complete
        """
        if len(self.current_sequence) != len(self.target_sequence):
            return False
        
        # Check that all crystals are still active
        if not all(crystal.is_active for crystal in self.current_sequence):
            return False
        
        return True
    
    @property
    def progress(self) -> float:
        """Get the current sequence completion progress.
        
        Returns:
            float: Progress from 0.0 to 1.0
        """
        return len(self.current_sequence) / len(self.target_sequence)
    
    def get_next_crystal_type(self) -> Optional[CrystalType]:
        """Get the next crystal type needed in the sequence.
        
        Returns:
            Optional[CrystalType]: The next crystal type or None if complete
        """
        current_pos = len(self.current_sequence)
        if current_pos >= len(self.target_sequence):
            return None
        return self.target_sequence[current_pos]
    
    def update(self) -> None:
        """Update the sequence state.
        
        Removes inactive crystals from the current sequence.
        """
        # Update all crystals in the sequence
        for crystal in self.current_sequence:
            crystal.update()
        
        # Remove inactive crystals
        self.current_sequence = [c for c in self.current_sequence if c.is_active]