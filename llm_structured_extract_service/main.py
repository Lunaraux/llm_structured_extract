import argparse
import logging
from .worker import submit_extract
from llm_structured_extract.config.settings import settings
from llm_structured_extract.core.schema_registry import list_available_schemas

# 获取日志对象
log = logging.getLogger("llm_structured_extract_service.cli")

def warmup():
    """应用启动预热（消除 get_model 风险）"""
    schemas = list_available_schemas()
    log.info(f"✅ Schema registry warmed up ({len(schemas)} schemas loaded)")

def cli():
    # 1. 初始化日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s %(filename)s:%(lineno)d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # 2. 预热
    warmup()
    
    # 3. 从统一配置获取服务参数
    service_config = settings.service_config
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=True)
    parser.add_argument("--schema", type=str, default=service_config.default_schema)
    parser.add_argument("--timeout", type=int, default=service_config.default_timeout)
    args = parser.parse_args()
    
    res = submit_extract.delay({"text": args.text, "schema": args.schema})
    output = res.get(timeout=args.timeout)
    log.info(output)


if __name__ == "__main__":
    cli()
