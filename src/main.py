from src.engine.game_engine import GameEngine

def main():
    """Start the game."""
    engine = GameEngine(800, 600, "The Resonance Maze")
    engine.start()

if __name__ == "__main__":
    main()