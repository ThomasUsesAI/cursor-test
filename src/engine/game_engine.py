import pygame
import time
from typing import Optional, Tuple
from src.engine.game_state import GameState
from src.game.crystal import CrystalType

class GameEngine:
    """Main game engine handling rendering and input.
    
    Attributes:
        screen_width (int): Window width in pixels
        screen_height (int): Window height in pixels
        tile_size (int): Size of each tile in pixels
        game_state (GameState): Current game state
        screen (pygame.Surface): Pygame display surface
        running (bool): Whether game is running
        last_movement (Tuple[int, int]): Last movement direction
    """
    
    def __init__(self, screen_width: int, screen_height: int, title: str = "Roguelike"):
        """Initialize the game engine.
        
        Args:
            screen_width (int): Window width in pixels
            screen_height (int): Window height in pixels
            title (str): Window title
        """
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_size = 20
        
        # Calculate map size based on screen dimensions
        map_width = screen_width // self.tile_size
        map_height = screen_height // self.tile_size
        
        self.game_state = GameState(map_width, map_height)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(title)
        
        self.running = True
        self.last_movement = (0, 0)  # Track last movement for ability use
        
        # Initialize font for UI
        self.font = pygame.font.Font(None, 24)
    
    def handle_input(self) -> None:
        """Handle keyboard input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # Ability hotkeys
                elif event.key == pygame.K_SPACE:
                    # Use Heat Crystal dash ability if unlocked
                    if self.last_movement != (0, 0):
                        self.game_state.use_ability(
                            CrystalType.RED,  # Heat crystal
                            self.last_movement[0],
                            self.last_movement[1]
                        )
        
        # Handle held movement keys
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_h]:
            dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_l]:
            dx = 1
        
        if keys[pygame.K_UP] or keys[pygame.K_k]:
            dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_j]:
            dy = 1
        
        if dx != 0 or dy != 0:
            if self.game_state.move_player(dx, dy):
                self.last_movement = (dx, dy)
    
    def render(self) -> None:
        """Render the game state."""
        self.screen.fill((0, 0, 0))  # Clear screen
        
        # Render map tiles
        for y in range(self.game_state.game_map.height):
            for x in range(self.game_state.game_map.width):
                tile = self.game_state.game_map.get_tile(x, y)
                color = (100, 100, 100) if tile.walkable else (50, 50, 50)
                
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                )
                
                # Draw tile character
                text = self.font.render(tile.char, True, (200, 200, 200))
                text_rect = text.get_rect(
                    center=(
                        x * self.tile_size + self.tile_size // 2,
                        y * self.tile_size + self.tile_size // 2
                    )
                )
                self.screen.blit(text, text_rect)
        
        # Render entities
        for entity in self.game_state.entities:
            text = self.font.render(entity.char, True, entity.color)
            text_rect = text.get_rect(
                center=(
                    entity.x * self.tile_size + self.tile_size // 2,
                    entity.y * self.tile_size + self.tile_size // 2
                )
            )
            self.screen.blit(text, text_rect)
        
        # Render UI
        self._render_ui()
        
        pygame.display.flip()
    
    def _render_ui(self) -> None:
        """Render game UI elements."""
        # Render sequence progress
        progress = self.game_state.sequence.progress
        next_crystal = self.game_state.sequence.get_next_crystal_type()
        
        if next_crystal:
            # Show next crystal needed
            text = f"Next: {next_crystal.name}"
            color = (255, 255, 255)
            if next_crystal in self.game_state.sequence.completed_types:
                text = f"{next_crystal.name} UNLOCKED!"
                color = (0, 255, 0)
            
            text_surface = self.font.render(text, True, color)
            self.screen.blit(text_surface, (10, 10))
            
            # Show progress bar
            bar_width = 200
            bar_height = 20
            pygame.draw.rect(
                self.screen,
                (50, 50, 50),
                (10, 40, bar_width, bar_height)
            )
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                (10, 40, int(bar_width * progress), bar_height)
            )
        
        # Show ability cooldowns
        y_offset = 70
        for crystal_type, ability in self.game_state.player.abilities.abilities.items():
            if ability.is_unlocked:
                cooldown_left = max(0, ability.cooldown - (time.time() - ability.last_use))
                ready = cooldown_left == 0
                
                text = f"{crystal_type.name}: {'READY' if ready else f'{cooldown_left:.1f}s'}"
                color = (0, 255, 0) if ready else (200, 200, 200)
                
                text_surface = self.font.render(text, True, color)
                self.screen.blit(text_surface, (10, y_offset))
                y_offset += 30
    
    def start(self) -> None:
        """Start the game loop."""
        while self.running:
            self.handle_input()
            self.game_state.update()
            self.render()
            pygame.time.Clock().tick(60)  # 60 FPS
        
        pygame.quit()