# CI/CD Pipeline with GitHub Actions & Docker (No Cloud Needed)

## 1. Overview

This project implements a **complete CI/CD pipeline** that:

- Builds a Docker image for a simple Node.js web application  
- Runs tests on every change  
- Pushes the image to **Docker Hub**  
- Deploys the app locally using **Minikube** (Kubernetes)  

No cloud provider (AWS/GCP/Azure) is required — everything runs on your local machine.

---

## 2. Architecture

**Flow:**

1. Developer writes code and pushes to **GitHub** (`main` branch)  
2. **GitHub Actions** workflow runs:
   - Installs dependencies
   - Runs tests
   - Builds Docker image
   - Pushes image to **Docker Hub**
3. **Minikube** (local Kubernetes cluster) pulls the image from Docker Hub  
4. Kubernetes Deployment + Service expose the app locally  

High-level pipeline:

```text
Local Dev → GitHub → GitHub Actions → Docker Hub → Minikube → Browser
```

## 3. Tech Stack
1. Language: Node.js (Express)
2. Containerization: Docker
3. CI/CD: GitHub Actions
4. Image Registry: Docker Hub
5. Orchestration: Kubernetes (Minikube)
6. Local Dev Helper: docker-compose (for local testing only)

## 4. Project Structure
```
project-root/
│
├── app/
│   └── server.js              # Express application
│
├── tests/
│   └── sample.test.js         # Basic test
│
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Local Docker compose (optional dev)
├── deployment.yaml            # Kubernetes Deployment + Service
├── package.json               # Node.js project config
│
└── .github/
    └── workflows/
        └── ci-cd.yml          # GitHub Actions CI/CD workflow
```

## 5. Prerequisites
You should have the following installed:
1. Git
2. Node.js (v18+ recommended)
3. Docker Desktop
4. Docker Hub account
5. Minikube
6. kubectl
7. GitHub repository

## 6. Local Development (Without CI/CD)
1. Install Dependencies
--> npm install
2. Run Tests
--> npm test
3. Run App Locally (Node)
--> npm start
App will be available at -
```
http://localhost:3000
```
5. Run with Docker Locally (Optional)
with docker-compose: docker-compose up --build

## 7. Dockerfile
The Dockerfile uses a small Node.js base image and runs the app:
```
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

## 8. GitHub Actions CI/CD Workflow
Path: .github/workflows/ci-cd.yml
1. What the Pipeline Does
On every push or pull request to main:
Checks out code
Sets up Node.js
Installs dependencies
Runs tests
Sets up Docker Buildx
Logs in to Docker Hub
Builds and pushes the Docker image to Docker Hub

2. Workflow Definition
```
name: CI-CD Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build-test-push:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18

      - name: Install Dependencies
        run: npm install

      - name: Run Tests
        run: npm test

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and Push image
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/ci-cd-demo-app:latest
```

3. Required GitHub Secrets
In GitHub Repo → Settings → Secrets and variables → Actions:
DOCKER_USERNAME → your Docker Hub username
DOCKER_PASSWORD → your Docker Hub password or access token

## 9. Docker Image
The image is pushed to Docker Hub with the tag:
<DOCKER_USERNAME>/ci-cd-demo-app:latest

## 10. Deployment on Minikube (Local Kubernetes)
1. Start Minikube
minikube start --driver=docker
Verify node:
kubectl get nodes
You should see the minikube node in Ready state.

2. Kubernetes Manifest (deployment.yaml)
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ci-cd-demo-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ci-cd-demo-app
  template:
    metadata:
      labels:
        app: ci-cd-demo-app
    spec:
      containers:
      - name: ci-cd-demo-app
        image: <your-docker-username>/ci-cd-demo-app:latest
        ports:
        - containerPort: 3000
---
apiVersion: v1
kind: Service
metadata:
  name: ci-cd-demo-service
spec:
  type: NodePort
  selector:
    app: ci-cd-demo-app
  ports:
    - port: 3000
      targetPort: 3000
      nodePort: 30080
```

3. Apply Deployment
```
kubectl apply -f deployment.yaml
```
Check pods: kubectl get pods

4. Access the Application
minikube service ci-cd-demo-service
You’ll get a URL like: http://192.168.49.2:30080

## 11. Deliverables Checklist
You can use this section when submitting or demonstrating the project:
✅ GitHub Repository with:
App source code
Dockerfile
deployment.yaml
.github/workflows/ci-cd.yml

✅ Docker Image Link (Docker Hub), e.g.:
```
https://hub.docker.com/r/<your-docker-username>/ci-cd-demo-app
```

✅ GitHub Actions CI/CD Workflow Results
Screenshot/URL of successful workflow run

✅ Screenshots of Deployed App
Browser screenshot of minikube URL showing app running
Optional: kubectl get pods output

## 12. Troubleshooting (Quick)
Pod stuck in ImagePullBackOff<br/>
Check if image exists on Docker Hub<br/>
Ensure deployment.yaml uses correct image name and tag<br/>
Make repo public or configure registry credentials for Kubernetes<br/>
Service URL not working<br/>
Verify pod status: kubectl get pods<br/>
Re-check nodePort and service name<br/>

Redeploy:
```
kubectl delete -f deployment.yaml
kubectl apply -f deployment.yaml
```

## 13. Possible Improvements
Add real unit tests instead of dummy test<br/>
Add environment variables via Kubernetes Secrets/ConfigMaps<br/>
Add health checks (livenessProbe, readinessProbe)<br/>
Integrate logging/monitoring (Prometheus, Grafana, Loki, etc.)<br/>
Extend pipeline with linting, code coverage, or multi-stage Docker builds<br/>

## 14. End result:
This project demonstrates a fully working local CI/CD pipeline using GitHub Actions + Docker + Docker Hub + Minikube, with no cloud provider required.
<br>Workflow Process: Local Dev → GitHub → GitHub Actions → Docker Hub → Minikube → Browser</br>
