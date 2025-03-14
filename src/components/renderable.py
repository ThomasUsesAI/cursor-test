from dataclasses import dataclass
from typing import Tuple

@dataclass
class Renderable:
    """Component for entities that can be rendered on screen.
    
    Attributes:
        char (str): Character representation of the entity
        color (Tuple[int, int, int]): RGB color tuple
    """
    char: str
    color: Tuple[int, int, int] = (255, 255, 255)  # Default to white