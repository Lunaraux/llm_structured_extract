# -*- coding: utf-8 -*-
import os
import sys
import asyncio
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List

# 将项目根目录添加到 pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm_structured_extract import async_extract_to_model
from llm_structured_extract.core.extract import _get_adapter
from llm_structured_extract.utils.logger import get_logger

logger = get_logger(__name__)

# 默认要提取的 8 个核心模型
CORE_SCHEMAS = [
    "company_basic_view",
    "company_core_business_view",
    "company_core_strategy_and_management_view",
    "company_financial_analysis_view",
    "company_founder_and_team_view",
    "company_funding_plan_view",
    "company_industry_view",
    "company_performance_and_valuation_view"
]

async def process_schema(text: str, schema: str, output_dir: Path, cache_id: str = None):
    """处理单个 Schema 的提取任务"""
    logger.info(f"🚀 开始提取 Schema: {schema}")
    
    # 准备输出文件路径
    raw_md_path = output_dir / "raw_markdown" / f"{schema}.md"
    json_path = output_dir / "parsed_json" / f"{schema}.json"
    
    try:
        # 执行异步提取
        result_obj = await async_extract_to_model(
            text, 
            schema, 
            save_raw_to=str(raw_md_path),
            context_cache_id=cache_id
        )
        
        # 保存解析后的 JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(
                result_obj.model_dump(mode='json'),
                f,
                ensure_ascii=False,
                indent=2
            )
        
        logger.info(f"✅ Schema {schema} 提取完成")
        return True
    except Exception as e:
        logger.error(f"❌ Schema {schema} 提取失败: {str(e)}")
        return False

async def main():
    parser = argparse.ArgumentParser(description="Batch extraction for multiple schemas from a single input file.")
    parser.add_argument("input", help="Path to the input Markdown file.")
    parser.add_argument("--output-root", default="outputs", help="Root directory for outputs.")
    parser.add_argument("--use-cache", action="store_true", help="Enable context caching to save tokens.")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)
        
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
    # 创建本次提取的专用文件夹
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"extract_{input_path.stem}_{timestamp}"
    output_dir = Path(args.output_root) / folder_name
    
    (output_dir / "raw_markdown").mkdir(parents=True, exist_ok=True)
    (output_dir / "parsed_json").mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*80}")
    print(f"📂 任务启动: {input_path.name}")
    print(f"📁 输出目录: {output_dir}")
    print(f"{'='*80}\n")

    # 1. 如果启用了缓存，先创建 Context Cache
    cache_id = None
    if args.use_cache:
        try:
            adapter = _get_adapter()
            print("⏳ 正在创建 Context Cache (可能需要几十秒)...")
            cache_id = adapter.create_context_cache(text)
            if cache_id:
                print(f"✨ Cache 创建成功: {cache_id}")
            else:
                print("⚠️ 该适配器不支持 Context Cache，将按普通模式继续。")
        except Exception as e:
            print(f"⚠️ Cache 创建失败: {e}")

    # 2. 并行执行 8 个模型的提取
    tasks = [
        process_schema(text, schema, output_dir, cache_id) 
        for schema in CORE_SCHEMAS
    ]
    
    results = await asyncio.gather(*tasks)
    
    # 统计结果
    success_count = sum(1 for r in results if r)
    print(f"\n{'='*80}")
    print(f"📊 任务总结:")
    print(f"✅ 成功: {success_count} / {len(CORE_SCHEMAS)}")
    print(f"📂 所有结果已保存至: {output_dir}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    asyncio.run(main())
