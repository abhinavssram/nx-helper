from typing import List


class NXEntity:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type
        
    @classmethod
    def from_dict(cls, d: dict):
        return cls(name=d["name"], type=d["type"])


class NXDependency:
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target

    @classmethod
    def from_dict(cls, d: dict):
        return cls(source=d["source"], target=d["target"])


class NXGraph:
    def __init__(self, nodes: List[NXEntity], dependencies: List[NXDependency]):
        self.nodes = nodes
        self.dependencies = dependencies


# Example data
# node1 = NXEntity(name="A", type="Process")
# node2 = NXEntity(name="B", type="Database")

# dep = NXDependency(source="A", target="B")

# graph = NXGraph(nodes=[node1, node2], dependencies=[dep])

# print(graph.nodes[0].name)  # Output: A