FROM python:3.10-slim-buster

WORKDIR /app

# Copy requirements first to leverage caching
COPY ./app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY ./app .

CMD ["python3", "app.py"]
