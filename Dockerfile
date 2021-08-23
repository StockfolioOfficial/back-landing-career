FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk update && apk upgrade && \
    apk --update add python3-dev gcc g++ libffi-dev mariadb-dev tzdata

RUN pip install -r requirements.txt

RUN cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN echo "Asia/Seoul" > /etc/timezone
RUN apk del tzdata

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "stockers.wsgi:application"]