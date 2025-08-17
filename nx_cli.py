#!/usr/bin/env python3
"""
Non-AI CLI interface for nx-helper
Direct access to dependency graph analysis without LLM requirements
"""

import argparse
import json
import sys
from pathlib import Path
from src.nx_graph_helper import NXGraphHelper
from src.utility import load_nx_graph_from_json


def print_formatted_dict(data, title=None):
    """Helper to format dictionary output nicely"""
    if title:
        print(f"\n{title}:")
    for key, value in data.items():
        if isinstance(value, list):
            print(f"  {key} ({len(value)}): {', '.join(value)}")
        else:
            print(f"  {key}: {value}")


def print_formatted_list(data, title=None):
    """Helper to format list output nicely"""
    if title:
        print(f"\n{title}:")
    if data:
        print(f"  Found {len(data)} items: {', '.join(data)}")
    else:
        print("  No items found")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Nx dependency graphs without AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python nx_cli.py --list-entities
  python nx_cli.py --dependencies my-app
  python nx_cli.py --dependencies-by-type my-app lib
  python nx_cli.py --dependents core-lib
  python nx_cli.py --check-dependency my-app core-lib
  python nx_cli.py --common-dependencies app1 app2
  python nx_cli.py --level-wise-dependencies my-app
  python nx_cli.py --level-wise-typed my-app
  python nx_cli.py --find-paths my-app core-lib
  python nx_cli.py --graph-file /path/to/nx-output.json --list-entities
        """
    )
    
    parser.add_argument(
        "--graph-file", 
        default="nx-output.json",
        help="Path to nx-output.json file (default: nx-output.json)"
    )
    
    # Main operations (mutually exclusive)
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument(
        "--list-entities",
        action="store_true",
        help="List all entities grouped by type"
    )
    
    group.add_argument(
        "--dependencies",
        metavar="ENTITY",
        help="Get all dependencies of an entity"
    )
    
    group.add_argument(
        "--dependencies-by-type",
        nargs=2,
        metavar=("ENTITY", "TYPE"),
        help="Get dependencies of specific type for an entity"
    )
    
    group.add_argument(
        "--dependents",
        metavar="ENTITY", 
        help="Get all entities that depend on this entity"
    )
    
    group.add_argument(
        "--check-dependency",
        nargs=2,
        metavar=("SOURCE", "TARGET"),
        help="Check if source entity depends on target entity"
    )
    
    group.add_argument(
        "--common-dependencies",
        nargs=2,
        metavar=("ENTITY1", "ENTITY2"),
        help="Find common dependencies between two entities"
    )
    
    group.add_argument(
        "--level-wise-dependencies",
        metavar="ENTITY",
        help="Get dependencies organized by levels (BFS traversal)"
    )
    
    group.add_argument(
        "--level-wise-typed",
        metavar="ENTITY",
        help="Get level-wise dependencies grouped by type at each level"
    )
    
    group.add_argument(
        "--find-paths",
        nargs=2,
        metavar=("SOURCE", "TARGET"),
        help="Find all paths from source to target (creates CSV file)"
    )
    
    args = parser.parse_args()
    
    try:
        # Load the graph
        graph = load_nx_graph_from_json(args.graph_file)
        nx_helper = NXGraphHelper(graph)
        
        # Execute the requested operation
        if args.list_entities:
            entities = nx_helper.get_all_entities()
            print_formatted_dict(entities, "All Entities")
            
        elif args.dependencies:
            deps = nx_helper.all_dependencies(args.dependencies)
            print_formatted_dict(deps, f"All Dependencies for '{args.dependencies}'")
            
        elif args.dependencies_by_type:
            entity, dep_type = args.dependencies_by_type
            deps = nx_helper.dependency_by_type(entity, dep_type)
            print_formatted_list(deps, f"Dependencies of '{entity}' with type '{dep_type}'")
            
        elif args.dependents:
            dependents = nx_helper.group_dependents_by_type(args.dependents)
            print_formatted_dict(dependents, f"Entities that depend on '{args.dependents}'")
            
        elif args.check_dependency:
            source, target = args.check_dependency
            result = nx_helper.check_if_dependent(source, target)
            print(f"\n{source} {'depends on' if result else 'does NOT depend on'} {target}")
            
        elif args.common_dependencies:
            entity1, entity2 = args.common_dependencies
            common = nx_helper.find_common_dependencies(entity1, entity2)
            print_formatted_dict(common, f"Common dependencies between '{entity1}' and '{entity2}'")
            
        elif args.level_wise_dependencies:
            level_deps = nx_helper.level_wise_dependencies(args.level_wise_dependencies)
            print(f"\nLevel-wise Dependencies for '{args.level_wise_dependencies}':")
            for level, deps in level_deps.items():
                print(f"  Level {level} ({len(deps)}): {', '.join(deps)}")
                
        elif args.level_wise_typed:
            typed_deps = nx_helper.level_wise_dependencies_with_types(args.level_wise_typed)
            print(f"\nLevel-wise Dependencies with Types for '{args.level_wise_typed}':")
            for level, type_dict in typed_deps.items():
                print(f"  Level {level}:")
                for dep_type, deps in type_dict.items():
                    print(f"    {dep_type} ({len(deps)}): {', '.join(deps)}")
                    
        elif args.find_paths:
            source, target = args.find_paths
            paths = nx_helper.find_all_paths_to_csv(source, target)
            if paths:
                print(f"\nFound {len(paths)} path(s) from '{source}' to '{target}':")
                for i, path in enumerate(paths[:5], 1):  # Show first 5 paths
                    print(f"  Path {i}: {' -> '.join(path)}")
                if len(paths) > 5:
                    print(f"  ... and {len(paths) - 5} more paths")
                print(f"\nComplete results saved to CSV file: path_{source}_{target}.csv")
            else:
                print(f"\nNo paths found from '{source}' to '{target}'")
            
    except FileNotFoundError:
        print(f"Error: Graph file '{args.graph_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in graph file '{args.graph_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()