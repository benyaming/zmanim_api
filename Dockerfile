FROM python:3.11-slim

RUN pip install poetry
WORKDIR /home/app
COPY . .
WORKDIR /home/app/zmanim_api
RUN poetry install
ENV PYTHONPATH=/home/app
ENV DOCKER_MODE=true
EXPOSE 8000
CMD ["poetry", "run", "python", "main.py"]
