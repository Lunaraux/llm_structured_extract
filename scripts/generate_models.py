# -*- coding: utf-8 -*-
import os
import sys
import argparse

# 将项目根目录添加到 pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm_structured_extract.utils.generator import ModelGenerator

def main():
    parser = argparse.ArgumentParser(description="Generate Pydantic models from Markdown skeleton with [id:xxx] annotations.")
    parser.add_argument("input", help="Path to the input Markdown file.")
    parser.add_argument("-o", "--output", help="Path to the output Python file. If not provided, prints to stdout.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)
        
    with open(args.input, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    gen = ModelGenerator()
    python_code = gen.generate_python_code(md_content)
    
    if args.output:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(python_code)
        print(f"Successfully generated model at: {args.output}")
    else:
        print(python_code)

if __name__ == "__main__":
    main()
