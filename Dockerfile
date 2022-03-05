FROM python:3.7.12-slim
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY requirements.txt .

RUN apt update \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0"]