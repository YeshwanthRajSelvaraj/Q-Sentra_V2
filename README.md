# Q-Sentra 🛡️

**Quantum-Safe Cryptographic Asset Management Platform**

Q-Sentra is a specialized cybersecurity platform built for enterprise environments (developed initially for Punjab National Bank operations out of a Hackathon scope). It is designed to proactively discover, analyze, and remediate systemic cryptographic vulnerabilities. It specifically focuses on managing the transition to **Post-Quantum Cryptography** (PQC) alongside core compliance monitoring frameworks.

---

## 🌟 Key Features

1. **AI-Powered PQC Posture Scoring**
   - Incorporates XGBoost Machine Learning and SHAP explanations to dynamically assess the quantum resilience score of endpoints.
   - Extracts key features recursively from TLS handshakes, certificate signatures (RSA/ECDSA distributions vs. KEM migrations).
   
2. **Dynamic Cyber Rating Engine**
   - Renders a multi-weighted Consolidated Enterprise Cyber Rating up to 1000 points.
   - Evaluates categories ranging from Protocol Versions and Certificate Expiries to Network Exposure.

3. **OSINT-Based Asset Discovery**
   - Multi-vectored asset ingestion utilizing Reverse DNS, DNS Enumeration, and Certificate Transparency log polling.
   - Streamed into an interactive queue for SOC Analysts to Ignore or Confirm into the central inventory seamlessly.

4. **Cryptographic Bill of Materials (CBOM)**
   - Automatically builds CycloneDX-aligned CBOM payloads indexing deep PKI topology per asset.

5. **Advanced Geographical & Interactive Visualizations**
   - Real-time heatmaps built with Leaflet for global cryptographic footprinting.
   - Responsive Dashboard interfaces and Network Graph Topologies displaying blast radiuses and active threat domains.

---

## 🛠️ Technology Stack

- **Frontend**: React (Vite-optimized), Tailwind-styled UI conventions, Recharts (Responsive Dataviz), Leaflet (Maps).
- **Backend Core**: Python 3, FastAPI, SQLAlchemy (Async), Uvicorn.
- **AI/ML Layer**: XGBoost, SHAP, Joblib, Pandas.
- **Database Architecture**: PostgreSQL (Relational states), MongoDB (NoSQL logs, pending configs), Redis (Messaging).

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed on your machine:
- Node.js (v18+)
- Python (v3.10+) 
- PostgreSQL
- MongoDB (Optional depending on backend configurations)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YeshwanthRajSelvaraj/Q-Sentra.git
   cd Q-Sentra
   ```

2. **Frontend Initialization:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   *The React interface will boot on `http://localhost:5173`.*

3. **Backend Initialization:**
   ```bash
   cd backend
   python -m venv venv
   source venv/Scripts/activate # Windows
   # source venv/bin/activate # Unix/macOS
   
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```
   *The FastAPI server will boot on `http://localhost:8000`. Test Swagger Docs at `/docs`.*

---

## 📦 Deployment & Containerization
Deeper integration is supported via Docker and Celery. Verify the root-level `docker-compose.yml` for unified orchestration pipelines once deployment properties are stabilized.

---

## 🤝 Contributing
For internal collaborations or general PR submissions, ensure your feature paths adhere to standard GitHub workflows. Branch out logically, maintain component granularity, and document Python hooks accordingly.

*Powered by Advanced Cryptographic AI Integrations.*
