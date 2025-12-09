# --------------------------
# 1. Base Image
# --------------------------
FROM python:3.10-slim

# Avoid Python buffering issues
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# --------------------------
# 2. Install Python packages
# --------------------------
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --------------------------
# 3. Copy project code
# --------------------------
COPY . .

# --------------------------
# 4. Expose API port
# --------------------------
EXPOSE 8000

# --------------------------
# 5. Command to run FastAPI
# --------------------------
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
