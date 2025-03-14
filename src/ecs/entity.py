class Entity:
    """Base entity class for the ECS system."""
    
    _next_id = 0
    
    def __init__(self):
        """Initialize a new entity with a unique ID."""
        self.id = Entity._next_id
        Entity._next_id += 1
        self.components = {}
    
    def add_component(self, component):
        """Add a component to the entity.
        
        Args:
            component: The component instance to add
        """
        self.components[type(component)] = component
    
    def remove_component(self, component_type):
        """Remove a component from the entity.
        
        Args:
            component_type: The type of component to remove
        """
        if component_type in self.components:
            del self.components[component_type]
    
    def get_component(self, component_type):
        """Get a component of the specified type.
        
        Args:
            component_type: The type of component to get
            
        Returns:
            The component instance if found, None otherwise
        """
        return self.components.get(component_type)