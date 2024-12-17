FROM python:3.12-slim

EXPOSE 8501

# install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && apt-get install -y ghostscript \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy app files to the container
COPY . /app

# Install dependencies
RUN uv sync --frozen

# Set the environment variable for Python unbuffered mode (this will allow you to see logs in real-time)
ENV PYTHONUNBUFFERED=1

# Expose port 80
EXPOSE 80

# Define the command to run the bot
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

# ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false", "--server.maxUploadSize=300" ]