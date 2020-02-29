FROM python:3.7

RUN pip install pipenv
WORKDIR /home/app
COPY . .
WORKDIR /home/app/zmanim_api
RUN pipenv install
ENV PYTHONPATH=/home/app
EXPOSE 8000
CMD ["pipenv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
