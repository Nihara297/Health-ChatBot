FROM python:3.10-slim-buster

WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install git+https://github.com/hwchase17/langchain-huggingface

# Copy the rest of the application
COPY . .

CMD ["python3", "app.py"]
