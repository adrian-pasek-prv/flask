# Base image
FROM python:latest
# Expose a port
EXPOSE 5000
# Move to an /app folder inside container
WORKDIR /app
# Install necessary packages
RUN pip install flask
# Copy necessary files like Python scripts to WORKDIR .
COPY app.py .
# What command should run when you start container
# 0.0.0.0 allows external clients to make a request
CMD ["flask", "run", "--host", "0.0.0.0"]
