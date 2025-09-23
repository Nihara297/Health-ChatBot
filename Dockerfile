FROM python:3.10-slim-bookworm

WORKDIR /app

# Install git and build tools plus common dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir git+https://github.com/hwchase17/langchain-huggingface

# Copy the rest of your application
COPY . .

# Expose the port your app runs on
EXPOSE 5001

# Run the application
CMD ["python3", "app.py"]
