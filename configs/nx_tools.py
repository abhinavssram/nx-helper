# configs/direct_tools.py
from langchain_core.tools import tool
from src.nx_graph_helper import NXGraphHelper

def create_nx_tools(nx_helper: NXGraphHelper):
    """Create tools directly from nx_helper"""
    
    @tool
    def get_all_dependencies(entity: str) -> str:
        """Get all dependencies of an entity
        Args:
            entity: The entity string to get the dependencies of.
        Returns:
            A string representation of the dependencies which is grouped by type in dict.
        """
        return str(nx_helper.all_dependencies(entity))
    
    @tool
    def get_dependencies_by_type(entity: str, target_type: str) -> str:
        """Get dependencies of a specific type for an entity
        Args:
            entity: The entity string to get the dependencies of.
            target_type: The type string of the dependencies to get.
        Returns:
            A string representation of the dependencies which is grouped by type in list.
        """
        return str(nx_helper.dependency_by_type(entity, target_type))
    
    @tool
    def list_all_entities() -> str:
        """List all entities in the graph grouped by type
        Returns:
            A string representation of the entities which is Dict[str, List[str]].
        """
        return str(nx_helper.get_all_entities())
    
    @tool
    def get_dependents_by_type(target_entity: str) -> str:
        """Get all entities that depend on a target entity, grouped by type
        Args:
            target_entity: The entity string to get the dependents of.
        Returns:
            A string representation of the dependents which is Dict[str, List[str]].
        """
        return str(nx_helper.group_dependents_by_type(target_entity))
    
    @tool
    def check_dependency_relationship(source: str, target: str) -> str:
        """Check if source entity depends on target entity
        Args:
            source: The source entity string.
            target: The target entity string.
        Returns:
            A string representation of the dependency relationship.
        """
        result = nx_helper.check_if_dependent(source, target)
        return f"{source} {'depends on' if result else 'does NOT depend on'} {target}"
    
    @tool
    def find_all_paths_between_source_and_target(source: str, target: str) -> str:
        """Find all paths from source to target entity and create a CSV file
        Args:
            source: The source entity string to start the path search from.
            target: The target entity string to find paths to.
        Returns:
            A string representation of all paths found and CSV file creation status.
        """
        paths = nx_helper.find_all_paths_to_csv(source, target)
        if not paths:
            return f"No paths found from '{source}' to '{target}'. No CSV file created."
        
        # Format the response with path information
        path_strings = []
        for i, path in enumerate(paths, 1):
            path_strings.append(f"Path {i}: {' -> '.join(path)}")
        
        csv_filename = f"path_{source}_{target}.csv"
        
        response = [
            f"Found {len(paths)} path(s) from '{source}' to '{target}':",
            "",
            *path_strings,
            "",
            f"CSV file created: {csv_filename}"
        ]
        
        return "\n".join(response)
    return [
        get_all_dependencies,
        get_dependencies_by_type,
        list_all_entities,
        get_dependents_by_type,
        check_dependency_relationship,
        find_all_paths_between_source_and_target
    ]