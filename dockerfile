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

# Explicitly copy model (in case .dockerignore excluded mlruns)
# NOTE: destination changed to /app/src/serving/model to match inference.py's path
COPY src/serving/model /app/src/serving/model

# Copy MLflow run (artifacts + metadata) to the flat /app/model convenience path
COPY src/serving/model/3c04b71d025f4e1a89cacce06357bb0c/artifacts/model /app/model
COPY src/serving/model/3c04b71d025f4e1a89cacce06357bb0c/artifacts/feature_columns.txt /app/model/feature_columns.txt
COPY src/serving/model/3c04b71d025f4e1a89cacce06357bb0c/artifacts/preprocessing.pkl /app/model/preprocessing.pkl

# make "serving" and "app" importable without the "src." prefix
# ensures logs are shown in real-time (no buffering).
# lets you import modules using from app... instead of from src.app....
ENV PYTHONUNBUFFERED=1 \ 
    PYTHONPATH=/app/src

# 6. Expose the Port
EXPOSE 8080

# 7. Run the fastapi app using uvicorn
CMD [ "python","-m","uvicorn","src.app.main:app","--host","0.0.0.0","--port","8080" ]

   