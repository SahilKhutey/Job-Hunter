# 🚀 HunterOS

> **The Autonomous Career Execution Engine.**  

> Don't just apply. Optimize, simulate, and win.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2015-black.svg?style=flat&logo=next.js)](https://nextjs.org/)
[![OpenAI](https://img.shields.io/badge/Intelligence-GPT--4o-412991.svg?style=flat&logo=openai)](https://openai.com/)

---

## 🧠 What is HunterOS?


**HunterOS** is a production-grade, multi-agent platform designed to automate the most grueling parts of the job search. Unlike traditional job boards, this system acts as your **Personal Talent Agent**, handling everything from identity management and resume tailoring to real-time ATS simulation.


### ✨ Key Features

- **🔐 Trust Layer**: Production-ready JWT authentication with Google & LinkedIn OAuth integration.
- **📄 Tailoring Engine**: AI-powered per-job resume optimization. Every application gets a unique, high-impact PDF.
- **📊 ATS Simulation**: A sophisticated scoring loop using semantic embeddings and structural rules to predict how recruiters see your resume.
- **⚡ Auto-Fix Loop**: Don't just find gaps—automatically bridge them. HunterOS suggests and implements improvements to increase your match score.
- **📱 Multi-Platform Ecosystem**: Integrated Mobile (Expo) for monitoring and Desktop (Electron) for high-performance automation execution.

- **🕵️ Multi-Agent Orchestration**: A backend architecture designed for parallel job scraping, analysis, and execution.


---

## 🛠️ Tech Stack

- **Frontend**: Next.js 15, Zustand (State Management), Tailwind CSS, Framer Motion (Animations).
- **Backend**: FastAPI (Python), PostgreSQL (via SQLAlchemy), Authlib (OAuth).
- **Intelligence**: OpenAI GPT-4o, Text Embeddings (3-Small).
- **Automation**: Playwright (Browser Execution), Celery/Redis (Task Queueing).
- **PDF Engine**: ReportLab (High-Fidelity Document Generation).

---

## 📂 Project Structure

```text
Job-Hunter/
├── backend/                # FastAPI Application
├── frontend/               # Next.js Web Dashboard
├── desktop/                # Electron App (Execution Engine)
├── mobile/                 # Expo App (Mission Control)
├── docker-compose.yml      # Container Orchestration
└── ROADMAP.md              # Future Vision & Goals

```

---

## 🚦 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL
- OpenAI API Key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SahilKhutey/Job-Hunter.git
   cd Job-Hunter
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   # Setup .env (see .env.example)
   python main.py
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

---

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get started.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ by [Sahil Khutey](https://github.com/SahilKhutey)**
