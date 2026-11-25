FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements-app.lock ./requirements-app.lock
RUN python -m pip install --no-cache-dir --require-hashes -r requirements-app.lock \
    && useradd --create-home --uid 10001 hsmart
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic
COPY src ./src
ENV PYTHONPATH=/app/src
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/v1/health', timeout=3)" || exit 1
CMD ["uvicorn", "hsmart_platform.app:app", "--host", "0.0.0.0", "--port", "8000"]
