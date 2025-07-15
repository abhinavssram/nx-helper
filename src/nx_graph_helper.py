from collections import defaultdict, deque
from typing import Dict, List, Set
from src.model import NXGraph
from src.utility import write_console_outputs

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