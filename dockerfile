# 1. Use the official lightweight Python base Image
FROM python:3.11-slim

# 2. Setting the working directory in the container
WORKDIR /app

# 3. Copy the requirements file into the container
COPY requirements.txt .

# 4. Install the python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 5. Copy the rest of the application code into the container
COPY . .