# Development Guidelines

## Project Chunks & Development Phases

### Phase 1: Core Engine & Basic Gameplay
1. **Basic Game Engine** (1-2 iterations)
   - Game loop
   - Input handling
   - Basic rendering
   - Entity Component System foundation

2. **Map Generation** (2-3 iterations)
   - Basic grid system
   - Room generation
   - Corridor connection
   - Obstacle placement

3. **Player Mechanics** (2-3 iterations)
   - Movement system
   - Collision detection
   - Field of view
   - Basic UI elements

### Phase 2: Quantum Mechanics
1. **Time Manipulation** (2-3 iterations)
   - Action recording
   - Timeline management
   - Temporal echo creation
   - Paradox resolution

2. **Quantum Energy System** (1-2 iterations)
   - Energy management
   - Recharge mechanics
   - Visual feedback
   - Balance tuning

3. **Quantum Effects** (2-3 iterations)
   - Probability fields
   - Quantum tunneling
   - Entanglement mechanics
   - Superposition states

### Phase 3: Content & Progression
1. **Enemy System** (2-3 iterations)
   - Basic AI behavior
   - Enemy types
   - Combat mechanics
   - Pathfinding

2. **Items & Equipment** (2-3 iterations)
   - Inventory system
   - Item effects
   - Equipment slots
   - Quantum modifications

3. **Progression System** (2-3 iterations)
   - Experience/leveling
   - Skill unlocks
   - Achievement tracking
   - Meta-progression

### Phase 4: Polish & Enhancement
1. **Visual Enhancement** (1-2 iterations)
   - Improved graphics
   - Animations
   - Particle effects
   - UI polish

2. **Audio Implementation** (1 iteration)
   - Sound effects
   - Background music
   - Audio management

3. **Performance Optimization** (1-2 iterations)
   - Code profiling
   - Memory optimization
   - Loading improvements

## Iteration Guidelines

### Iteration Size
Each iteration should be:
- **Completable in 1-2 hours** of focused development
- **Self-contained** with clear start/end points
- **Testable** with defined success criteria
- **Documented** with updated design docs

### Iteration Structure
1. **Planning** (10-15 minutes)
   - Review requirements
   - Define success criteria
   - Outline implementation steps

2. **Implementation** (30-60 minutes)
   - Write code in small, testable chunks
   - Follow clean code principles
   - Add necessary documentation

3. **Testing** (15-20 minutes)
   - Run unit tests
   - Manual testing
   - Performance checks

4. **Review & Documentation** (10-15 minutes)
   - Code cleanup
   - Update documentation
   - Commit changes

### Code Change Size
- **Maximum 300 lines** of new code per iteration
- **Maximum 3 files** modified significantly
- **Maximum 1 major system** changed per iteration
- Each commit should be atomic and reversible

## Core Development Principles

### 1. Structured Development Process
- Break each feature into logical, manageable steps
- Plan implementation before coding
- Document architectural decisions
- Use version control effectively with meaningful commits

### 2. Code Architecture
- Follow clean architecture principles
- Use Entity Component System (ECS) for game objects
- Maintain separation of concerns
- Keep code DRY (Don't Repeat Yourself)
- Write modular and reusable components

### 3. Game Design Focus
#### Strategic Depth
- Implement thoughtful decision-making mechanics
- Balance resource management systems
- Create adaptable gameplay scenarios
- Design meaningful player choices

#### Roguelike Elements
- Implement procedural generation for replayability
- Design permadeath mechanics with fair consequences
- Create turn-based systems that reward strategy
- Develop meaningful progression systems

#### Replayability
- Generate dynamic encounters
- Create randomized but balanced maps
- Design unlockable content that adds value
- Implement varied gameplay paths

### 4. Code Quality Standards
- Write clear, self-documenting code
- Add comprehensive docstrings to classes and functions
- Follow PEP 8 style guide for Python
- Keep functions focused and single-purpose
- Use type hints for better code clarity
- Write unit tests for critical components

### 5. Performance Considerations
- Profile code regularly
- Optimize resource-intensive operations
- Use appropriate data structures
- Consider memory management in procedural generation
- Cache frequently accessed data

### 6. Documentation Requirements
- Maintain up-to-date API documentation
- Document complex algorithms
- Keep README current with setup instructions
- Document game mechanics and systems
- Track technical debt and future improvements

## Development Workflow

### 1. Feature Implementation
1. Design the feature (document in GAME_DESIGN.md)
2. Break down into tasks
3. Implement core functionality
4. Write tests
5. Document the feature
6. Review and refactor
7. Commit with clear message

### 2. Code Review Guidelines
- Check for adherence to architecture
- Verify documentation completeness
- Ensure test coverage
- Review performance implications
- Validate game design principles

### 3. Testing Strategy
- Unit tests for core systems
- Integration tests for feature interactions
- Playtesting for game mechanics
- Performance testing for critical systems

## Project Structure
```
quantum-rogue/
├── docs/                 # Documentation
├── src/                  # Source code
│   ├── engine/          # Game engine components
│   ├── ecs/             # Entity Component System
│   ├── quantum/         # Quantum mechanics systems
│   ├── procedural/      # Procedural generation
│   ├── ui/              # User interface components
│   └── utils/           # Utility functions
├── tests/               # Test suite
├── assets/              # Game assets
└── requirements.txt     # Dependencies
```

## Commit Message Guidelines
Format:
```
[type]: Brief description

Detailed description of changes and reasoning
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Test changes
- chore: Build/maintenance changes