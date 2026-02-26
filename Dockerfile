FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .
CMD ["python", "-m", "llm_structured_extract_service.main", "--text", "张三，邮箱 zhang@example.com，电话 13800001234"]
