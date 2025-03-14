import pygame
from typing import Tuple, Optional
from src.engine.game_state import GameState
from src.map.tile import TileType
from src.game.crystal import Crystal

class GameEngine:
    """Game engine handling rendering and input.
    
    This class is responsible for:
    - Initializing the game window
    - Handling the game loop
    - Processing input
    - Rendering the game state
    
    Attributes:
        screen (pygame.Surface): The game window surface
        state (GameState): Current game state
        cell_size (int): Size of each tile in pixels
        running (bool): Whether the game is running
    """
    
    def __init__(self, screen_width: int = 800, screen_height: int = 600,
                 title: str = "Resonance Maze"):
        """Initialize the game engine.
        
        Args:
            screen_width (int): Window width in pixels
            screen_height (int): Window height in pixels
            title (str): Window title
        """
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(title)
        
        self.cell_size = 12
        self.state = GameState()
        self.running = True
        
        # Colors
        self.colors = {
            TileType.WALL: (128, 128, 128),  # Gray
            TileType.FLOOR: (64, 64, 64),    # Dark gray
            TileType.VOID: (0, 0, 0),        # Black
            'player': (0, 255, 255),         # Cyan
            'ui_bg': (32, 32, 32),           # Dark gray
            'ui_text': (255, 255, 255),      # White
            'ui_highlight': (255, 255, 0),    # Yellow
        }
        
        # Font
        self.font = pygame.font.Font(None, 24)
    
    def start(self) -> None:
        """Start the game loop."""
        clock = pygame.time.Clock()
        
        while self.running:
            self._handle_events()
            self.state.update()
            self._render()
            clock.tick(60)
        
        pygame.quit()
    
    def _handle_events(self) -> None:
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.state.move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.state.move_player(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.state.move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.state.move_player(1, 0)
    
    def _render(self) -> None:
        """Render the current game state."""
        self.screen.fill(self.colors[TileType.VOID])
        
        # Calculate viewport
        player_x, player_y = self.state.player_pos
        viewport_width = self.screen.get_width() // self.cell_size
        viewport_height = (self.screen.get_height() - 100) // self.cell_size
        
        viewport_x = max(0, min(player_x - viewport_width // 2,
                              self.state.game_map.width - viewport_width))
        viewport_y = max(0, min(player_y - viewport_height // 2,
                              self.state.game_map.height - viewport_height))
        
        # Render map
        for y in range(viewport_height):
            for x in range(viewport_width):
                map_x = viewport_x + x
                map_y = viewport_y + y
                
                if not self.state.game_map.in_bounds(map_x, map_y):
                    continue
                
                tile = self.state.game_map.get_tile(map_x, map_y)
                color = self.colors[tile.type]
                
                screen_x = x * self.cell_size
                screen_y = y * self.cell_size
                
                pygame.draw.rect(
                    self.screen,
                    color,
                    (screen_x, screen_y, self.cell_size, self.cell_size)
                )
        
        # Render crystals
        for room in self.state.rooms:
            if not room.crystal:
                continue
            
            crystal_x, crystal_y = room.crystal.position
            screen_x = (crystal_x - viewport_x) * self.cell_size
            screen_y = (crystal_y - viewport_y) * self.cell_size
            
            if (0 <= screen_x < self.screen.get_width() and
                0 <= screen_y < self.screen.get_height()):
                color = room.crystal.color
                if not room.crystal.is_active:
                    color = tuple(c // 2 for c in color)  # Darker when inactive
                
                pygame.draw.rect(
                    self.screen,
                    color,
                    (screen_x, screen_y, self.cell_size, self.cell_size)
                )
        
        # Render player
        player_screen_x = (player_x - viewport_x) * self.cell_size
        player_screen_y = (player_y - viewport_y) * self.cell_size
        
        pygame.draw.rect(
            self.screen,
            self.colors['player'],
            (player_screen_x, player_screen_y, self.cell_size, self.cell_size)
        )
        
        # Render UI
        self._render_ui()
        
        pygame.display.flip()
    
    def _render_ui(self) -> None:
        """Render the game UI."""
        # UI background
        ui_height = 100
        ui_rect = pygame.Rect(0, self.screen.get_height() - ui_height,
                            self.screen.get_width(), ui_height)
        pygame.draw.rect(self.screen, self.colors['ui_bg'], ui_rect)
        
        # Sequence progress
        progress = self.state.sequence_progress
        progress_width = self.screen.get_width() - 40
        progress_height = 20
        progress_x = 20
        progress_y = self.screen.get_height() - 80
        
        # Background bar
        pygame.draw.rect(
            self.screen,
            (64, 64, 64),
            (progress_x, progress_y, progress_width, progress_height)
        )
        
        # Progress bar
        pygame.draw.rect(
            self.screen,
            (0, 255, 0),
            (progress_x, progress_y,
             int(progress_width * progress), progress_height)
        )
        
        # Next crystal info
        next_type = self.state.next_crystal_type
        if next_type:
            text = f"Next: {next_type.name}"
            color = next_type.value[1]
        else:
            text = "Sequence Complete!"
            color = (0, 255, 0)
        
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(
            centerx=self.screen.get_width() // 2,
            centery=self.screen.get_height() - 30
        )
        self.screen.blit(text_surface, text_rect)