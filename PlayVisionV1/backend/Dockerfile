FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update && apt install -y python3-dev postgresql-client && apt clean

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["sh", "entrypoint.sh"]