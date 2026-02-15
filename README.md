# 📉 Telco Churn Prediction – End-to-End MLOps Project

A production-ready machine learning system that predicts telecom customer churn and deploys it as a scalable API + interactive web application on AWS.

> 🌍 **Live Application:**  
> http://telco-fastapi-alb-835982802.eu-west-2.elb.amazonaws.com/

---

# 🚀 Project Overview

Customer churn directly impacts revenue in telecom businesses. This project delivers a complete, production-grade ML solution that:

- Predicts customers likely to churn  
- Exposes predictions via a REST API  
- Provides an interactive Streamlit frontend  
- Uses Docker + CI/CD for reproducible deployments  
- Runs serverlessly on AWS ECS Fargate  

This is not just a notebook model — it is a fully operational ML system deployed in the cloud.

---

# 🎯 Business Problem

Customer retention is significantly cheaper than acquisition. The objective is to:

- Identify high-risk customers early  
- Enable proactive retention strategies  
- Reduce churn rate  
- Increase customer lifetime value  

---

# 🏗️ Architecture Overview

```
GitHub → GitHub Actions → Docker Hub → AWS ECS Fargate
                                      ↓
                               Application Load Balancer
                                      ↓
                              FastAPI Inference Service
                                      ↓
                                Streamlit UI
```

---

# 🧠 Machine Learning Pipeline

## 1️⃣ Data Processing & Feature Engineering
- Data cleaning and preprocessing
- Categorical encoding
- Feature scaling
- Train/validation split
- Handling class imbalance

## 2️⃣ Model Training
- XGBoost Classifier
- Hyperparameter tuning
- Evaluation metrics:
  - Accuracy
  - Precision
  - Recall
  - ROC-AUC

## 3️⃣ Experiment Tracking (MLflow)
- Logged parameters
- Logged metrics
- Logged model artifacts
- Versioned runs under a named experiment
- Reproducible training pipeline

---

# 🔌 Model Serving – FastAPI

## Available Endpoints

| Method | Endpoint   | Description            |
|--------|------------|------------------------|
| GET    | `/`        | Health check           |
| POST   | `/predict` | Predict churn outcome  |

### Example Request

```json
POST /predict
{
  "tenure": 12,
  "MonthlyCharges": 70.5
}
```

---

# 🖥️ Frontend – Streamlit

- Interactive UI for manual testing
- Displays churn probability
- Business-friendly interface
- No need for API tools

Access via:

```
http://<ALB-DNS>/ui
```

---

# 🐳 Containerization

- Dockerized FastAPI + Streamlit app
- Uvicorn entrypoint: `src.app.main:app`
- Port exposed: `8000`
- PYTHONPATH configured to include `/app/src`
- Production-ready container image

---

# 🔁 CI/CD – GitHub Actions

On every push to `main`:

1. Build Docker image  
2. Push image to Docker Hub  
3. (Optional) Trigger ECS deployment  

Ensures:
- Automated builds  
- Reproducible deployments  
- Continuous integration  

---

# ☁️ AWS Infrastructure

## ECS Fargate
- Serverless container execution
- Managed compute
- Zero server maintenance

## Application Load Balancer
- Listener: HTTP :80
- Target Group: HTTP :8000
- Health check path: `/`

## Security Groups
- ALB:
  - Inbound 80 from `0.0.0.0/0`
- ECS Task:
  - Inbound 8000 from ALB SG
- Outbound: Open

## Observability
- CloudWatch Logs for:
  - Container stdout/stderr
  - ECS service events
- ALB health monitoring

---

# 🔄 Deployment Flow

1. Push code to `main`
2. GitHub Actions builds Docker image
3. Image pushed to Docker Hub
4. ECS service forces new deployment
5. ALB health checks `/`
6. Traffic routed to healthy task
7. Users access `/predict` or `/ui`

---

# 🛠️ Challenges & Solutions

## Unhealthy Targets Behind ALB
**Cause:** Health-check path mismatch  
**Solution:** Added `GET /` endpoint and aligned ports (80 → 8000)

---

## ModuleNotFoundError in Container
**Cause:** `src/` not in Python path  
**Solution:** Set:
```dockerfile
ENV PYTHONPATH=/app/src
```
Updated Uvicorn path:
```
src.app.main:app
```

---

## ALB DNS Timing Out
**Cause:** Incorrect security group configuration  
**Solution:**
- ALB inbound 80 from internet
- Task inbound 8000 from ALB SG

---

## ECS Not Using Latest Image
**Cause:** Old task definition running  
**Solution:** Forced new deployment after image push

---

## MLflow “No runs found”
**Cause:** Experiment name mismatch  
**Solution:** Standardized MLflow experiment naming and model loading

---

# 📂 Project Structure

```
├── src/
│   ├── app/
│   │   ├── main.py
│   │   ├── inference.py
│   ├── training/
│   ├── features/
│
├── Dockerfile
├── requirements.txt
├── .github/workflows/
└── README.md
```

---

# 🔐 Production Best Practices Implemented

- Stateless container architecture
- Health check endpoint
- Structured logging
- Scoped security groups
- Versioned ML artifacts
- CI/CD automation
- Infrastructure isolation

---

# 📌 Key Highlights

✔ End-to-End ML lifecycle  
✔ Cloud deployment on AWS  
✔ Containerized production app  
✔ Automated CI/CD pipeline  
✔ MLflow experiment tracking  
✔ API + Frontend integration  
✔ Real-world infrastructure debugging  

---

# 🔮 Future Improvements

- JWT authentication
- Model registry with MLflow
- Auto-scaling policies
- Canary deployments
- SHAP explainability
- Monitoring with Prometheus + Grafana
- Feature store integration

---

# 👨‍💻 Author

**Jay**  
Machine Learning Engineer | MLOps Enthusiast  

---

If this project helped you or inspired you, feel free to ⭐ the repository.
