FROM python:3
ENV PYTHONUNBUFFERED=1
ENV DEBUG_MODE=True
ENV DB_ENGINE=postgre
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
