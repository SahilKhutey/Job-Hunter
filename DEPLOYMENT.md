# HunterOS: Development & Deployment Guide

## 🛠️ Development Workflow

HunterOS is a multi-platform ecosystem. Follow these instructions to run the full stack locally.

### 1. Backend (Python/FastAPI)
The brain of the operation.
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
python run_backend.py
```
*   **API**: `http://localhost:8000`
*   **Docs**: `http://localhost:8000/docs`

### 2. Web Frontend (Next.js)
The primary interface.
```bash
cd frontend
npm install
npm run dev
```
*   **URL**: `http://localhost:3000`

### 3. Desktop App (Electron)
The high-privacy automation shell.
```bash
cd desktop
npm install
npm start
```

### 4. Mobile App (Expo/React Native)
The Mission Control companion.
```bash
cd mobile
npm install
npx expo start
```

---

## 🚀 Deployment Strategy

HunterOS uses a containerized architecture for reliable production deployment.

### 1. Production Stack (Docker Compose)
Deploy the full intelligence pipeline including Nginx Gateway, Redis, and Postgres.
```bash
docker-compose up -d --build
```

### 2. Services Overview
*   **Gateway (Nginx)**: Handles SSL termination and routes traffic between the frontend and API.
*   **API**: Scalable FastAPI instances.
*   **Worker**: Dedicated container for background browser automation (Playwright).
*   **Redis**: Used for task queuing and real-time WebSocket state.
*   **Postgres**: Persistent storage for profiles, jobs, and audit logs.

### 3. CI/CD Pipeline
Automated deployments are handled via GitHub Actions (`.github/workflows/deploy.yml`).
*   **Triggers**: On push to `main`.
*   **Actions**: 
    1.  Linting & Security Scan.
    2.  Build Docker Images.
    3.  Push to Registry.
    4.  Deploy to Production Cluster.

---

## 🔐 Security & Hardening
*   **JWT Authentication**: All inter-service communication is secured via signed tokens.
*   **Environment Variables**: Use `.env` files (ignored by git) for sensitive keys.
*   **Playwright Isolation**: Automation runs in isolated browser contexts within the `worker` container.
