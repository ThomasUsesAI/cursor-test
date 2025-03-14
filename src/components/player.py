from dataclasses import dataclass

@dataclass
class Player:
    """Component that marks an entity as the player character.
    
    Attributes:
        quantum_energy (int): Current quantum energy level
        max_quantum_energy (int): Maximum quantum energy capacity
    """
    quantum_energy: int = 100
    max_quantum_energy: int = 100
    
    def use_energy(self, amount: int) -> bool:
        """Attempt to use quantum energy.
        
        Args:
            amount (int): Amount of energy to use
            
        Returns:
            bool: True if energy was successfully used, False if insufficient
        """
        if self.quantum_energy >= amount:
            self.quantum_energy -= amount
            return True
        return False
    
    def restore_energy(self, amount: int) -> None:
        """Restore quantum energy.
        
        Args:
            amount (int): Amount of energy to restore
        """
        self.quantum_energy = min(self.quantum_energy + amount, self.max_quantum_energy)