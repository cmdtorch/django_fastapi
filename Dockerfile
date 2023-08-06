FROM python:3.11

WORKDIR /django_fastapi
COPY ./requirements.txt /django_fastapi/

RUN pip install -r requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /django_fastapi

CMD ["uvicorn", "django_fastapi.app:fastapp", "--host", "0.0.0.0", "--port", "80"]