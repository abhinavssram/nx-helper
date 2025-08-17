from collections import defaultdict, deque
from typing import Dict, List, Set
from src.model import NXGraph
from src.utility import load_nx_graph_from_json, write_console_outputs, write_csv_output

class NXGraphHelper:
    def __init__(self, graph: NXGraph):
        self.graph = graph
        self.entity_type_map = {node.name: node.type for node in graph.nodes}
        self.reverse_map = self._build_reverse_map()
    
    def _build_reverse_map(self) -> Dict[str, List[str]]:
        reverse_map = defaultdict(list)
        for dep in self.graph.dependencies:
            reverse_map[dep.target].append(dep.source)
        return reverse_map

    def dfs_dependencies(self, entity: str, visited=None, result=None):
        if visited is None:
            visited = set()
        if result is None:
            result = []

        if entity in visited:
            return result

        visited.add(entity)

        for dep in self.graph.dependencies:
            if dep.source == entity and dep.target not in visited:
                result.append(dep.target)
                self.dfs_dependencies(dep.target, visited, result)

        return result

    def all_dependencies(self, entity: str):
        '''
        DFS Traverse through the graph to get all the dependencies of given entity.
        Output grouped by type
        '''
        all_deps = self.dfs_dependencies(entity)
        type_map = defaultdict(list)

        for dep in all_deps:
            type_ = self.entity_type_map.get(dep, "unknown")
            type_map[type_].append(dep)

        output = [f"All Dependencies for '{entity}':"]
        for type_, deps in type_map.items():
            output.append(f"{type_} ({len(deps)}): {deps}")

        write_console_outputs("all_dependencies.txt", "\n".join(output))
        return dict(type_map)

    def dependency_by_type(self, entity: str, target_type: str):
        '''
        Get dependencies of a given type for an entity
        '''
        all_deps = self.dfs_dependencies(entity)
        filtered = [dep for dep in all_deps if self.entity_type_map.get(dep) == target_type]

        output = [
            f"Dependencies of '{entity}' with type '{target_type}' ({len(filtered)}):",
            str(filtered)
        ]
        write_console_outputs("dependencies_by_type.txt", "\n".join(output))
        return filtered

    def level_wise_dependencies(self, entity: str) -> Dict[int, List[str]]:
        '''
        BFS Traverse through the graph to get dependencies organized by levels.
        Level 0: direct dependencies, Level 1: dependencies of dependencies, etc.
        '''
        visited = set()
        queue = deque([(entity, -1)])  # Start with level -1 so direct deps are level 0
        level_map = defaultdict(list)
        entity_levels = {}  # Track the level of each entity
        
        visited.add(entity)
        
        while queue:
            current_entity, current_level = queue.popleft()
            
            # Find all direct dependencies of current entity
            for dep in self.graph.dependencies:
                if dep.source == current_entity and dep.target not in visited:
                    new_level = current_level + 1
                    visited.add(dep.target)
                    level_map[new_level].append(dep.target)
                    entity_levels[dep.target] = new_level
                    queue.append((dep.target, new_level))
        
        # Prepare output for text file
        output = [f"Level-wise Dependencies for '{entity}':"]
        output.append("=" * 50)
        
        total_deps = 0
        for level in sorted(level_map.keys()):
            deps = level_map[level]
            total_deps += len(deps)
            output.append(f"\nLevel {level} ({len(deps)} dependencies):")
            
            # Group by type at each level
            type_grouped = defaultdict(list)
            for dep in deps:
                dep_type = self.entity_type_map.get(dep, "unknown")
                type_grouped[dep_type].append(dep)
            
            for dep_type, type_deps in type_grouped.items():
                output.append(f"  {dep_type}: {type_deps}")
        
        output.append(f"\nSummary:")
        output.append(f"Total levels: {len(level_map)}")
        output.append(f"Total dependencies: {total_deps}")
        
        # Write to file
        filename = f"level_wise_dependencies_{entity.replace('/', '_').replace(':', '_')}.txt"
        write_console_outputs(filename, "\n".join(output))
        
        return dict(level_map)

    def level_wise_dependencies_with_types(self, entity: str) -> Dict[int, Dict[str, List[str]]]:
        '''
        BFS Traverse to get level-wise dependencies grouped by type at each level.
        Returns nested dict: {level: {type: [entities]}}
        '''
        visited = set()
        queue = deque([(entity, -1)])
        level_type_map = defaultdict(lambda: defaultdict(list))
        
        visited.add(entity)
        
        while queue:
            current_entity, current_level = queue.popleft()
            
            for dep in self.graph.dependencies:
                if dep.source == current_entity and dep.target not in visited:
                    new_level = current_level + 1
                    visited.add(dep.target)
                    dep_type = self.entity_type_map.get(dep.target, "unknown")
                    level_type_map[new_level][dep_type].append(dep.target)
                    queue.append((dep.target, new_level))
        
        # Prepare detailed output
        output = [f"Level-wise Dependencies with Types for '{entity}':"]
        output.append("=" * 60)
        
        for level in sorted(level_type_map.keys()):
            type_dict = level_type_map[level]
            total_at_level = sum(len(deps) for deps in type_dict.values())
            output.append(f"\nLevel {level} - Total: {total_at_level} dependencies")
            output.append("-" * 40)
            
            for dep_type in sorted(type_dict.keys()):
                deps = type_dict[dep_type]
                output.append(f"  {dep_type} ({len(deps)}):")
                for dep in sorted(deps):
                    output.append(f"    - {dep}")
        
        # Write to file
        filename = f"level_wise_dependencies_typed_{entity.replace('/', '_').replace(':', '_')}.txt"
        write_console_outputs(filename, "\n".join(output))
        
        # Convert defaultdict to regular dict for return
        result = {}
        for level, type_dict in level_type_map.items():
            result[level] = dict(type_dict)
        
        return result

    # def check_if_dependent(self, entity1: str, entity2: str):
    #     '''
    #     Return True if entity1 depends (directly or indirectly) on entity2
    #     '''
    #     all_deps = self.dfs_dependencies(entity1)
    #     result = entity2 in all_deps
    #     msg = f"{entity1} {'does' if result else 'does NOT'} depend on {entity2}"
    #     write_console_outputs("check_dependency.txt", msg)
    #     return result
    
    def get_all_entities(self) -> Dict[str, List[str]]:
        entity_map = defaultdict(list)
        for node in self.graph.nodes:
            entity_map[node.type].append(node.name)

        output = [f"All Entities:"]
        for type_, deps in entity_map.items():
            output.append(f"{type_} ({len(deps)}): {deps}")
        
        write_console_outputs("entities.txt", "\n".join(output))
        return dict(entity_map)
    
    def get_all_dependents(self, target_entity: str) -> List[str]:
        visited = set()
        queue = deque([target_entity])
        result = []

        while queue:
            curr = queue.popleft()
            for parent in self.reverse_map.get(curr, []):
                if parent not in visited:
                    visited.add(parent)
                    result.append(parent)
                    queue.append(parent)

        return result

    def group_dependents_by_type(self, target_entity: str) -> Dict[str, List[str]]:
        all_dependents = self.get_all_dependents(target_entity)
        grouped = defaultdict(list)

        for dep in all_dependents:
            type_ = self.entity_type_map.get(dep, "unknown")
            grouped[type_].append(dep)

        return dict(grouped)

    def check_if_dependent(self, source: str, target: str) -> bool:
        visited = set()
        return self._check_if_dependent_dfs(source, target, visited)

    def _check_if_dependent_dfs(self, current: str, target: str, visited: Set[str]) -> bool:
        if current == target:
            return True
        visited.add(current)
        for dep in self.graph.dependencies:
            if dep.source == current and dep.target not in visited:
                if self._check_if_dependent_dfs(dep.target, target, visited):
                    return True
        return False

    def find_common_dependencies(self, entity1: str, entity2: str) -> Dict[str, List[str]]:
        """Find common dependencies between two entities, grouped by type"""
        deps1 = set(self.dfs_dependencies(entity1))
        deps2 = set(self.dfs_dependencies(entity2))
        common_deps = deps1.intersection(deps2)
        
        grouped = defaultdict(list)
        for dep in common_deps:
            type_ = self.entity_type_map.get(dep, "unknown")
            grouped[type_].append(dep)
        
        output = [f"Common dependencies between '{entity1}' and '{entity2}':"]
        for type_, deps in grouped.items():
            output.append(f"{type_} ({len(deps)}): {deps}")
        
        write_console_outputs("common_dependencies.txt", "\n".join(output))
        return dict(grouped)
    
    def find_all_paths_to_csv(self, source: str, target: str):
        """
        Find all paths from source to target and save them to a CSV file
        """
        all_paths = self._find_all_paths(source, target, [], [])
        
        if not all_paths:
            print(f"No paths found from '{source}' to '{target}'")
            return []
        
        # Format paths for CSV (each path as a string with arrow notation)
        formatted_paths = []
        for path in all_paths:
            path_str = " -> ".join(path)
            formatted_paths.append([path_str])
        
        # Create CSV filename
        csv_filename = f"path_{source}_{target}.csv"
        
        # Write to CSV
        write_csv_output(csv_filename, formatted_paths, ["paths"])
        
        # Also write summary to console output for reference
        output_lines = [
            f"All paths from '{source}' to '{target}' ({len(all_paths)} paths found):",
            ""
        ]
        for i, path in enumerate(all_paths, 1):
            output_lines.append(f"Path {i}: {' -> '.join(path)}")
        
        write_console_outputs(f"paths_{source}_{target}.txt", "\n".join(output_lines))
        
        return all_paths

    def _find_all_paths(self, source: str, target: str, current_path: List[str], all_paths: List[List[str]]) -> List[List[str]]:
        """
        Recursive helper method to find all paths from source to target using DFS
        """
        # Add current node to the path
        current_path = current_path + [source]
        
        # If we reached the target, add this path to results
        if source == target:
            all_paths.append(current_path)
            return all_paths
        
        # Explore all dependencies of current source
        for dep in self.graph.dependencies:
            if dep.source == source:
                # Avoid cycles by checking if target is already in current path
                if dep.target not in current_path:
                    self._find_all_paths(dep.target, target, current_path, all_paths)
        
        return all_paths
