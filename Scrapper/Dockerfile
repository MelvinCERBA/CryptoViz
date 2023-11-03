# Start from a Python 3.9 base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies for Chrome and wget
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg2 \
    ca-certificates \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Install Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Copy the Python requirements file into the container at /usr/src/app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY src/ .
CMD ["faust", "-A", "main", "worker", "-l", "info"]