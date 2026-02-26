# -*- coding: utf-8 -*-
import os
import sys
import importlib

# 将项目根目录添加到 pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm_structured_extract.core.schema_registry import get_all_schemas
from llm_structured_extract.utils.model_visualizer import visualize_model

def main():
    schemas = get_all_schemas()
    
    if not schemas:
        print("No schemas found in registry. Make sure models are in the models/ directory.")
        return

    print(f"Found {len(schemas)} registered schemas.\n")
    
    import argparse
    parser = argparse.ArgumentParser(description="Verify model structures against business architecture.")
    parser.add_argument("schema", nargs="?", help="Specific schema name to verify.")
    parser.add_argument("--meta", action="store_true", help="Show field names and types in output.")
    args = parser.parse_args()

    schemas = get_all_schemas()
    
    if not schemas:
        print("No schemas found in registry. Make sure models are in the models/ directory.")
        return

    print(f"Found {len(schemas)} registered schemas.\n")
    
    if args.schema:
        if args.schema in schemas:
            visualize_model(schemas[args.schema], show_meta=args.meta)
        else:
            print(f"Schema '{args.schema}' not found.")
    else:
        for name in sorted(schemas.keys()):
            visualize_model(schemas[name], show_meta=args.meta)

if __name__ == "__main__":
    main()
