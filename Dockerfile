FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .
CMD ["python", "-c", "from llm_structured_extract import __version__; print(__version__)"]
