import pygame
from typing import Tuple
from src.engine.game_state import GameState
from src.components.position import Position
from src.components.renderable import Renderable

class GameEngine:
    """Main game engine class responsible for managing the game loop and core systems."""
    
    def __init__(self, width: int = 800, height: int = 600, title: str = "Quantum Rogue"):
        """Initialize the game engine.
        
        Args:
            width (int): Screen width in pixels
            height (int): Screen height in pixels
            title (str): Window title
        """
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.is_running = False
        
        # Calculate tile size based on screen dimensions and desired map size
        self.tile_size = min(width // 80, height // 60)
        
        # Initialize game state
        self.state = GameState()
        
        # Initialize font
        self.font = pygame.font.Font(None, self.tile_size)
    
    def start(self) -> None:
        """Start the game loop."""
        self.is_running = True
        while self.is_running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(60)
        
        pygame.quit()
    
    def _handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
    
    def _handle_keydown(self, key: int) -> None:
        """Handle keyboard input.
        
        Args:
            key (int): The pygame key constant that was pressed
        """
        if key == pygame.K_ESCAPE:
            self.is_running = False
        elif key == pygame.K_UP:
            self.state.move_player(0, -1)
        elif key == pygame.K_DOWN:
            self.state.move_player(0, 1)
        elif key == pygame.K_LEFT:
            self.state.move_player(-1, 0)
        elif key == pygame.K_RIGHT:
            self.state.move_player(1, 0)
    
    def _update(self) -> None:
        """Update game state."""
        self.state.update()
    
    def _render(self) -> None:
        """Render the game."""
        self.screen.fill((0, 0, 0))  # Clear screen with black
        
        # Render all entities
        for entity_id, components in self.state.entities.items():
            if Position in components and Renderable in components:
                pos = components[Position]
                renderable = components[Renderable]
                self._render_entity(pos, renderable)
        
        pygame.display.flip()
    
    def _render_entity(self, pos: Position, renderable: Renderable) -> None:
        """Render a single entity.
        
        Args:
            pos (Position): Position component of the entity
            renderable (Renderable): Renderable component of the entity
        """
        # Create a surface with the character
        text_surface = self.font.render(renderable.char, True, renderable.color)
        
        # Calculate screen position
        screen_x = pos.x * self.tile_size
        screen_y = pos.y * self.tile_size
        
        # Center the character in its tile
        text_rect = text_surface.get_rect(center=(screen_x + self.tile_size // 2,
                                                screen_y + self.tile_size // 2))
        
        # Draw to screen
        self.screen.blit(text_surface, text_rect)