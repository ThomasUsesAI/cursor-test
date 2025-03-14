from typing import List, Optional, Set
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
        used_crystals (Set[Crystal]): Crystals that have been used in sequence
        completed_types (Set[CrystalType]): Crystal types that have been permanently unlocked
    """
    
    def __init__(self, sequence_length: int = 3):
        """Initialize a new crystal sequence tracker.
        
        Args:
            sequence_length (int): Length of the sequence to generate
        """
        self.max_sequence_length = sequence_length
        self.target_sequence: List[CrystalType] = []
        self.current_sequence: List[Crystal] = []
        self.used_crystals: Set[Crystal] = set()
        self.completed_types: Set[CrystalType] = set()
        self._generate_sequence()
    
    def _generate_sequence(self) -> None:
        """Generate a new random target sequence."""
        self.target_sequence = []
        available_types = [t for t in CrystalType if t not in self.completed_types]
        
        if not available_types:
            return  # All sequences completed
            
        crystal_type = random.choice(available_types)
        self.target_sequence = [crystal_type]  # Only one type at a time now
    
    def add_crystal(self, crystal: Crystal) -> bool:
        """Add a crystal to the current sequence.
        
        Args:
            crystal (Crystal): The crystal being activated
            
        Returns:
            bool: True if the crystal matches the next in sequence
        """
        # If this type is already completed, ignore it
        if crystal.crystal_type in self.completed_types:
            return False
        
        # Remove any inactive crystals from the current sequence and used set
        self.current_sequence = [c for c in self.current_sequence if c.is_active]
        self.used_crystals = {c for c in self.used_crystals if c.is_active}
        
        # Ignore if this crystal was already used
        if crystal in self.used_crystals:
            return False
        
        # Check if this activation matches the sequence
        current_pos = len(self.current_sequence)
        if current_pos >= len(self.target_sequence):
            return False
        
        if crystal.crystal_type == self.target_sequence[current_pos]:
            self.current_sequence.append(crystal)
            self.used_crystals.add(crystal)
            
            # If sequence is complete, permanently unlock this type
            if self.is_complete:
                self.completed_types.add(crystal.crystal_type)
                self._generate_sequence()  # Generate new sequence for next type
            
            return True
        
        # Wrong crystal - reset sequence
        self.current_sequence = []
        self.used_crystals.clear()
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
    def all_completed(self) -> bool:
        """Check if all crystal types have been completed.
        
        Returns:
            bool: True if all crystal types are unlocked
        """
        return len(self.completed_types) == len(CrystalType)
    
    @property
    def progress(self) -> float:
        """Get the current sequence completion progress.
        
        Returns:
            float: Progress from 0.0 to 1.0
        """
        if not self.target_sequence:
            return 1.0
        return len(self.current_sequence) / len(self.target_sequence)
    
    def get_next_crystal_type(self) -> Optional[CrystalType]:
        """Get the next crystal type needed in the sequence.
        
        Returns:
            Optional[CrystalType]: Next crystal type or None if complete
        """
        current_pos = len(self.current_sequence)
        if current_pos >= len(self.target_sequence):
            return None
        return self.target_sequence[current_pos]
    
    def update(self) -> None:
        """Update the sequence state.
        
        Removes inactive crystals from the current sequence and used set.
        """
        # Update all crystals in the sequence
        for crystal in self.current_sequence:
            crystal.update()
        
        # Remove inactive crystals
        self.current_sequence = [c for c in self.current_sequence if c.is_active]
        self.used_crystals = {c for c in self.used_crystals if c.is_active}
        
        # If any crystal became inactive and we haven't completed this type,
        # reset the sequence
        if (len(self.current_sequence) < len(self.used_crystals) and
            not self.target_sequence[0] in self.completed_types):
            self.current_sequence = []
            self.used_crystals.clear()