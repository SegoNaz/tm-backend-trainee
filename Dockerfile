FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./test /code/test
COPY ./__init__.py /code/__init__.py

