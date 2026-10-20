
FROM python:3.12-slim

WORKDIR /app

COPY http_identity_lab.py /app/http_identity_lab.py
COPY docker/service_settings.json /app/service_settings.json

EXPOSE 18080

CMD ["python", "-u", "http_identity_lab.py"]
