import pygame

class GameEngine:
    """Main game engine class responsible for managing the game loop and core systems."""
    
    def __init__(self, width=800, height=600, title="Quantum Rogue"):
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
        
    def start(self):
        """Start the game loop."""
        self.is_running = True
        while self.is_running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(60)
        
        pygame.quit()
    
    def _handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
    
    def _update(self):
        """Update game state."""
        pass
    
    def _render(self):
        """Render the game."""
        self.screen.fill((0, 0, 0))  # Clear screen with black
        pygame.display.flip()