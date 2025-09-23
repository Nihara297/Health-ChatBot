FROM python:3.10-slim-buster

WORKDIR /app

# Install git and build tools before pip
RUN apt-get update && apt-get install -y git build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install git+https://github.com/hwchase17/langchain-huggingface

# Copy the rest of your application
COPY . .

CMD ["python3", "app.py"]
