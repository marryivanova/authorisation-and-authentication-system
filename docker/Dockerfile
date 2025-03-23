FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install -r /app/requirements.txt


CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]