Sutradhara AI: Multi-Source Enterprise Banking Gateway
Sutradhara AI is a production-grade, highly scalable financial technology gateway designed to automate account reconciliation, process high-velocity cross-border currency exchanges, and monitor compliance threats for multi-timeline financial datasets.
The application implements an advanced Retrieval-Augmented Generation (RAG) topology inspired by the Cohere Coral architecture to simultaneously ingest and cross-reference structured account ledgers, localized policy manuals, and real-time infrastructure event feeds. To ensure high availability (99.9%), the system features a self-healing, automated local CPU fallback protocol utilizing quantized large language models (LLMs) when cloud orchestrators experience transient network timeouts or credential validation exceptions.
Architectural Topology
The system is engineered as a decoupled, asynchronous, hybrid cloud-edge architecture optimized for performance, security, and computational resilience:
•	Document Parsing Engine (Edge OCR): Utilizes a CPU-bound EasyOCR execution layer to read unstructured document matrices (PNG, JPG, or raw logs). It handles coordinate data-splitting to isolate explicit text blocks before transferring payloads.
•	Cloud Orchestration & Data Structuring: Integrates with the cloud-hosted cohere Command-R suite via a strict prompt engineering syntax. This layer forces non-deterministic visual text arrays to resolve into strongly typed, schema-compliant JSON outputs.
•	Asynchronous Network Worker (Non-Blocking I/O): Built with Fast Api’s Background Tasks framework. High-latency cross-border ledger clearing operations are handled out-of-thread, allowing the front-end browser runtime to remain responsive and unblocked.
•	Fail-Safe Processing (Self-Healing Fallback): Implements structural exception handling. If a cloud endpoint fails, a fallback worker automatically redirects model constraints to a localized, quantized GGUF instance (llama-cpp-python) running locally, preventing pipeline failures.
Technology Stack & Core Systems
•	Backend Framework: Fast API (ASGI Web Server Engine)
•	AI & Machine Learning Ecosystem: Cohere Cloud API Client V2, EasyOCR (Computer Vision Core), Llama.cpp Python (GGUF Quantization Runtime)
•	Data Processing & Automation: Python-Multipart, Pillow (PIL Engine), Regular Expression Pattern Matchers
•	Outbound Notification Layer: Python smtplib executing secure TLS handshakes over Google's standard network wire protocol on Port 587
•	Frontend Web Component: Responsive HTML5/JavaScript application with Tailwind CSS utility engines and dynamic database cache rendering





System Dependencies & Installation
To deploy the workspace engine locally, execute the following dependency installations inside your terminal console:
PowerShell
# Install production-grade web frameworks, computer vision packages, and cloud SDKs
pip install fastapi uvicorn cohere easyocr llama-cpp-python pillow python-multipart
Edge Weight Mount Configuration (Local Backup Model)
To support the self-healing local execution fallback protocols, mount your localized model weights directly inside your standard user profile directory:
C:/Users/<your_machine_username>/Downloads/qwen2.5-1.5b-instruct-q4_k_m.gguf
Enterprise Network Parameters
Configure your cloud authorization credentials and local network socket definitions directly within the main configuration block of your banking_agent.py file:
Python
# --- COHERE CLOUD CORE handshakes ---
COHERE_API_KEY = "your_secret_production_cloud_token_here"
# --- PRODUCTION GOOGLE SMTP NETWORK WIRE SETTINGS ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your.verified.identity@gmail.com"
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"  # Dedicated 16-character secure App Password
Deployment Sequence
To boot up the active web gateway and begin listening on localized interface loopbacks, route your terminal path context to your project space and launch Uvicorn:
PowerShell
# Step 1: Initialize terminal focus to the development workspace folder
cd "C:\Users\Bhargav gajjala\OneDrive\Desktop"
# Step 2: Boot server loops with live-reload watching active
uvicorn banking_agent:app --host 127.0.0.1 --port 8000 --reload
Once initialized, open index.html in any standard web browser to launch the client-facing financial dashboard.


Ingestive Evaluation Dataset Format
To evaluate your statement layout tables, regular expression boundaries, and multi-timeline data-splitting functions, save the following structural pipe-delimited block as a plain text file (.txt) and process it via the Statement Ingestion portal:
---------------------------------------------------------------------------------------------------------------------------SUTRADHARA GLOBAL BANK PLC - EXPAT MEMBER ACCOUNT STATEMENT LEDGER
---------------------------------------------------------------------------------------------------------------------------
05/01/2026 | INFLOW  | INFUSION RES TECH SALARY       | 2900.00 | Salary
12/01/2026 | OUTFLOW | LANDLORD HOUSING RENT          | -850.00 | Rent
18/01/2026 | OUTFLOW | SWEET MAGIC RESTAURANT CO      | -45.50  | Leisure
20/01/2026 | OUTFLOW | MKS FUSION RESTAURANT LON      | -38.20  | Leisure
28/01/2026 | OUTFLOW | SHELL CORP ALPHA INTERNATIONAL | -500.00 | Risk_Transfer
---------------------------------------------------------------------------------------------------------------------------
Key System Feature Matrix
•	Document OCR Ingestion: Automates end-to-end computer vision text layer discovery via custom EasyOCR array blocks.
•	Asynchronous Task Workers: Avoids server thread exhaustion by offloading currency transaction holding states to out-of-thread background execution tasks.
•	Outbound SMTP Notification Loops: Handles instant transaction receipts and status reports using direct, secure TLS handshakes with Google's mail infrastructure.
•	Coral RAG Multi-Source Ingestion: Simultaneously references active memory caches, mock internal compliance documents, and global fraud databases to synthesize unified security reports.
•	Resilient Self-Healing Fallback Logic: Monitors cloud connectivity and safely down-shifts task execution to localized local CPU constraints if external web sockets time out or drop.

