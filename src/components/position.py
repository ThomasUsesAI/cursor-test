from dataclasses import dataclass

@dataclass
class Position:
    """Component for storing an entity's position in the game world.
    
    Attributes:
        x (int): The x-coordinate in the game grid
        y (int): The y-coordinate in the game grid
    """
    x: int
    y: int
    
    def move(self, dx: int, dy: int) -> None:
        """Move the position by the given delta.
        
        Args:
            dx (int): Change in x-coordinate
            dy (int): Change in y-coordinate
        """
        self.x += dx
        self.y += dy