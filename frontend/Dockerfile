
FROM python:3.12-bookworm


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./home.py /code/


CMD ["streamlit", "run", "home.py", "--server.port", "80"]