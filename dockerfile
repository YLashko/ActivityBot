FROM python:3.11.0-alpine3.17

WORKDIR /app

COPY . .

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers \
    && apk add libffi-dev
RUN pip install poetry
RUN poetry install

WORKDIR /app

CMD ["poetry", "run", "python", "activitybot/main.py"]
