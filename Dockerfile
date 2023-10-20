FROM python:3.11-slim

RUN pip install pdm
WORKDIR /home/app
COPY . .
WORKDIR /home/app/zmanim_api
RUN pdm install
ENV PYTHONPATH=/home/app
ENV DOCKER_MODE=true
EXPOSE 8000
CMD ["pdm", "run", "python", "main.py"]
