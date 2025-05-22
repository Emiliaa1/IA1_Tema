FROM python:3.11-alpine

RUN apk add --no-cache gcc musl-dev libffi-dev

# Set working directory
WORKDIR /app

COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables for Flask
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

EXPOSE 5000

# Run the Flask app
CMD ["flask", "run"]