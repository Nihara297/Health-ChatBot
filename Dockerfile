FROM python:3.10-slim-buster

WORKDIR /app

# copy requirements from repo root
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy rest of repo into /app
COPY . .

CMD ["python3", "app.py"]
