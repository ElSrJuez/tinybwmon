# Dockerfile for tinybwmon
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the Flask port
EXPOSE 42042

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=42042
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
