# Base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y git

# Install synthguard
RUN pip install git+https://github.com/SynthGuard/synthguard-library.git

# Copy the rest of your application code
COPY . /app
