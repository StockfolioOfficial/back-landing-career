FROM python:3.9-alpine

LABEL POPM=HellP
LABEL POPM=HellP
LABEL Maintainers=Yerang-Kim,junlegend
LABEL Maintainers_Mail=grondin0425@gmail.com,junlegend82@gmail.com

WORKDIR /app

COPY requirements.txt .

RUN apk update && apk upgrade && \
    apk --update add python3-dev gcc g++ libffi-dev mariadb-dev tzdata make

RUN pip install -r requirements.txt

RUN cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN echo "Asia/Seoul" > /etc/timezone
RUN apk del tzdata

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "stockers.wsgi:application"]
