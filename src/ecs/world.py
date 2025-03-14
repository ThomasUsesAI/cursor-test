class World:
    """Container for all entities and systems in the game."""
    
    def __init__(self):
        """Initialize an empty world."""
        self.entities = {}
        self.systems = []
    
    def add_entity(self, entity):
        """Add an entity to the world.
        
        Args:
            entity: The entity to add
        """
        self.entities[entity.id] = entity
    
    def remove_entity(self, entity_id):
        """Remove an entity from the world.
        
        Args:
            entity_id: The ID of the entity to remove
        """
        if entity_id in self.entities:
            del self.entities[entity_id]
    
    def add_system(self, system):
        """Add a system to the world.
        
        Args:
            system: The system to add
        """
        self.systems.append(system)
    
    def update(self):
        """Update all systems in the world."""
        for system in self.systems:
            system.update(self.entities)