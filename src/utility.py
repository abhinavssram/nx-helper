import csv
import json
from pathlib import Path
from typing import List
from src.model import NXDependency, NXEntity, NXGraph

def load_nx_graph_from_json(filepath: str) -> NXGraph:
    path = Path(__file__).parent / filepath
    with path.open("r") as f:
        data = json.load(f)

    graph_data = data["graph"]

    # Parse nodes
    nodes_raw = graph_data["nodes"]
    nodes = []
    for node_name, node_info in nodes_raw.items():
        nodes.append(NXEntity.from_dict(node_info))

    # Parse dependencies
    dependencies_raw = graph_data["dependencies"]
    dependencies = []
    for dep_list in dependencies_raw.values():
        for dep in dep_list:
            dependencies.append(NXDependency.from_dict(dep))

    return NXGraph(nodes=nodes, dependencies=dependencies)

def write_console_outputs(fileName: str, output_str: str):
    # Ensure the /outputs directory exists
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # File path inside /outputs
    file_path = output_dir / fileName

    # Append to file
    with open(file_path, "a") as f:
        f.write(output_str + "\n")    

def write_csv_output(fileName: str, data: List[List[str]], headers: List[str]):
    """
    Write data to CSV file in the outputs directory
    """
    # Ensure the /outputs directory exists
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # File path inside /outputs
    file_path = output_dir / fileName

    # Write to CSV file
    with open(file_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)  # Write headers
        writer.writerows(data)    # Write data rows
    
    print(f"CSV output written to {file_path}")
# Access the objects
# graph = load_nx_graph_from_json("../nx-output.json")

# txt = "Nodes:\n"
# for node in graph.nodes:
#     txt += (f"- {node.name} ({node.type})\n")

# write_console_outputs("nodes.txt", txt)


# print("Dependencies:")
# for dep in graph.dependencies:
#     print(f"- {dep.source} -> {dep.target}")
