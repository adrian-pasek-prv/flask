# Base image
FROM python:latest
# Move to an /app folder inside container
WORKDIR /app
# Copy requirements.txt to WORKDIR for pip to use 
COPY requirements.txt .
# Install necessary packages
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# Copy necessary files like Python scripts to WORKDIR .
COPY . .
# What command should run when you start container
# Run bash script called docker-entrypoint.sh
# It has specification of what chain of commands it should use
CMD ["/bin/bash", "docker-entrypoint.sh"]
