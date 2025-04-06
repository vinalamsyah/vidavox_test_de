
FROM python:3.12-alpine


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN apk add postgresql-dev


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app


WORKDIR /code/app


CMD ["uvicorn", "endpoints:app", "--host", "0.0.0.0", "--port", "80"]