FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies first to leverage Docker caching
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set Flask environment variables directly in the Dockerfile
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expose the port Flask runs on (optional but helpful for container networking)
EXPOSE 5000

# Use CMD for running the application
CMD ["python", "app.py"]