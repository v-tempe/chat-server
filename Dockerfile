FROM python:3.13-slim

LABEL authors="step"

RUN apt-get update && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && \
    rm /uv-installer.sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv export --frozen -o requirements.txt && \
    uv pip install --system --no-cache-dir -r requirements.txt

COPY app ./

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app.main:app"]

CMD ["--host", "0.0.0.0", "--port", "8000"]