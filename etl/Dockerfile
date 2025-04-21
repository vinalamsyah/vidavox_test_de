
FROM python:3.12-bookworm


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN apt-get update && apt-get install -y libpq-dev poppler-utils tesseract-ocr ffmpeg libsm6 libxext6


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app


WORKDIR /code/app


CMD ["python", "-u", "watcher.py"]