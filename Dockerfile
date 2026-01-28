FROM ghcr.io/astral-sh/uv:python3.11-trixie-slim

WORKDIR /home/app
COPY . .
WORKDIR /home/app/zmanim_api
RUN uv sync --frozen --no-dev
ENV PATH="/home/app/zmanim_api/.venv/bin:$PATH"
ENV PYTHONPATH=/home/app
ENV DOCKER_MODE=true
EXPOSE 8000
CMD ["uv", "run", "python", "main.py"]
