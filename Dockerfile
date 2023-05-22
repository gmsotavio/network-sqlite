FROM python:alpine

WORKDIR /app

# Install SQLite
RUN apk add --no-cache sqlite

# Copy the server code
COPY server.py /app/server.py
COPY abc.db /app/abc.db

# Expose the server port
EXPOSE 8888

# Run the server
CMD ["python3", "server.py"]
