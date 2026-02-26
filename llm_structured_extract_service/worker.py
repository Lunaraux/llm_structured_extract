import logging
from celery import Celery
from llm_structured_extract.config.settings import settings
from llm_structured_extract import extract
from llm_structured_extract.core.schema_registry import list_available_schemas
from .task_models import ExtractTask


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s %(filename)s:%(lineno)d %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = Celery(
    "llm_structured_extract_service",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)
# 从统一配置获取任务队列名称
app.conf.task_default_queue = settings.service_config.task_queue

# 预热 Schema Registry
logger = logging.getLogger(__name__)
schemas = list_available_schemas()
logger.info(f"✅ Worker schema registry warmed up ({len(schemas)} schemas loaded)")


@app.task
def submit_extract(payload: dict) -> str:
    task = ExtractTask(**payload)
    output = extract(task.text, task.schema)
    return output


if __name__ == "__main__":
    import sys
    app.worker_main(sys.argv[1:])
