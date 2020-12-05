FROM python:alpine3.7

RUN apk update && \
    apk add build-base=0.5-r0 \
    linux-headers=4.4.6-r2 \
    python3-dev

WORKDIR /app/weather
COPY requirements.txt /app/weather
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
