# -*- coding: utf-8 -*-
import os
import sys
import argparse
import re

# 将项目根目录添加到 pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm_structured_extract.utils.generator import ModelGenerator

def preprocess_md_for_model(md_content):
    """
    预处理Markdown内容，适配LLM提取规则（对齐手动编写模型的格式）
    1. 剥离标题前的序号（如「1. 创始人背景」→「创始人背景」）
    2. 将H4层级降级为H3（减少深嵌套，避免Prompt规则跳过上层标题）
    """
    lines = md_content.split("\n")
    processed_lines = []
    # 匹配标题前的序号：支持「1.」「（1）」「二、」「3、」等格式
    seq_pattern = r"^[一二三四五六七八九十\d]{1,2}[.、）\s)]*"
    
    for line in lines:
        stripped_line = line.strip()
        # 处理标题行（#/##/###/#### 开头）
        if stripped_line.startswith(("# ", "## ", "### ", "#### ")):
            # 提取标题层级和内容
            level = len(re.match(r'^#+', stripped_line).group())
            title_content = stripped_line.lstrip("# ").strip()
            # 剥离序号
            title_content = re.sub(seq_pattern, "", title_content).strip()
            # 简化层级：H4→H3（避免过深嵌套）
            if level == 4:
                level = 3
            # 重构标题行
            new_title = f"{'#'*level} {title_content}"
            processed_lines.append(new_title)
        else:
            # 非标题行原样保留
            processed_lines.append(line)
    
    return "\n".join(processed_lines)

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
    
    # 新增：预处理Markdown，对齐手动编写的格式
    md_content = preprocess_md_for_model(md_content)
        
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
