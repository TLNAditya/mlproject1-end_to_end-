FROM python:3.12-slim-trixie

WORKDIR /app

# Copy everything (so setup.py is inside /app)
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]
