# 🚁 Autonomous Drone Mission Intelligence & Safety System

An agentic AI system that combines **RAG, multi-agent reasoning, computer vision, safety rules, human-in-the-loop approval, persistent mission memory, and drone simulation** to make explainable drone mission decisions.

## 🎯 Project Objective

The system is designed to assist autonomous drone missions by:

- Retrieving safety and operational knowledge using RAG
- Analyzing drone inspection imagery
- Detecting mission risks
- Making explainable mission decisions
- Applying deterministic safety gates
- Requesting human approval for risky decisions
- Executing actions through a simulated drone
- Storing mission history
- Generating mission reports

---

## 🏗️ System Architecture

```text
                         USER
                           |
                           v
                  Mission Request
                           |
                           v
                  +----------------+
                  |   LangGraph    |
                  |  Orchestrator  |
                  +-------+--------+
                          |
             +------------+------------+
             |            |            |
             v            v            v
        RAG Agent    Vision Agent   Risk Agent
             |            |            |
             v            v            v
       Drone Docs      Image/VLM    Sensor Data
             |            |            |
             +------------+------------+
                          |
                          v
                  Decision Agent
                          |
                          v
                    Safety Gate
                          |
                   +------+------+
                   |             |
                   v             v
             Human Review    Safe Action
                   |             |
                   +------+------+
                          |
                          v
                  Drone Simulator
                          |
                          v
                   Mission Memory
                          |
                          v
                   Mission Report
🧠 Technologies Used
Python
LangGraph
LangChain
ChromaDB
RAG
Ollama
Llama 3.2 3B
Qwen2.5-VL 3B
Scikit-learn
PyPDF
FastAPI
Git & GitHub
🤖 AI Agents
1. RAG Agent

The RAG Agent retrieves relevant information from the drone knowledge base.

Knowledge sources include:

Drone Safety Policy
Drone Operations Manual
Inspection Procedures
Mission History

The retrieved information is passed to the decision pipeline as evidence.

2. Vision Agent

The Vision Agent uses Qwen2.5-VL to analyze drone inspection images.

It identifies:

Objects visible in the image
Possible anomalies
Anomaly type
Confidence
Image description

Run the Vision Agent separately:

python -m agents.vision_agent

The default test image is:

data/images/sample_drone_image.png

The included image is a test/placeholder image. A real drone inspection image can be provided for a more realistic demonstration.

3. Risk Agent

The Risk Agent evaluates mission conditions such as:

Battery level
Wind speed
GPS availability
Vision anomalies

It assigns a risk level:

LOW
MEDIUM
HIGH
CRITICAL
4. Decision Agent

The Decision Agent combines retrieved evidence and risk information to produce an explainable decision.

Possible decisions include:

APPROVE
HUMAN_REVIEW
RETURN_TO_HOME
ABORT_MISSION
MISSION_START_BLOCKED
5. Safety Gate

The Safety Gate provides a deterministic safety layer before the system executes an action.

High-risk decisions can require human approval.

This prevents the LLM from directly controlling the simulated drone without safety validation.

📚 RAG Knowledge Base

The system contains the following knowledge documents:

data/
│
├── drone_operations_manual.txt
├── drone_safety_policy.txt
├── inspection_procedures.txt
├── mission_history.txt
└── images/

The documents are:

Loaded
Split into chunks
Converted into vectors
Stored in ChromaDB
Retrieved based on the user's question
⚙️ How to Run the Project
1. Clone the repository
git clone https://github.com/yvangeti-byte/autonomous-drone-ai.git
cd autonomous-drone-ai
2. Create a virtual environment

On Windows:

python -m venv venv

Activate it:

.\venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Install Ollama

Install Ollama on your computer.

Then download the required models:

ollama pull llama3.2:3b

For image analysis:

ollama pull qwen2.5vl:3b

Verify the models:

ollama list
🚀 Run the Complete System

Run:

python main.py

The system will ask:

What should the drone system check?
Enter battery percentage:
Enter wind speed (km/h):
Is GPS available? (yes/no):

Example:

What should the drone system check? Check whether it is safe to start the drone mission.
Enter battery percentage: 80
Enter wind speed (km/h): 15
Is GPS available? (yes/no): yes

The system will execute:

RAG Agent
    ↓
Vision Agent
    ↓
Risk Agent
    ↓
Decision Agent
    ↓
Safety Gate
    ↓
Drone Simulator
    ↓
Mission Memory
    ↓
Mission Report
❓ Example Questions and Expected Results
Question 1 — Battery Below 20%
Question
What should happen if the drone battery falls below 20 percent during a mission?
Expected Answer
If the drone battery falls below 20% during a mission,
the drone should immediately initiate Return-to-Home (RTH).
Expected Decision
Risk Level: HIGH
Decision: RETURN_TO_HOME
Safety Action: RETURN_TO_HOME
❓ Question 2 — Battery Below 10%
Question
What should happen if the drone battery falls below 10 percent?
Expected Result
Risk Level: CRITICAL
Decision: ABORT_MISSION
Safety Action: ABORT_MISSION

The simulated drone aborts the mission and performs a safe landing procedure.

❓ Question 3 — Normal Mission

Enter:

What should the drone system check? Check whether it is safe to start the drone mission.
Enter battery percentage: 80
Enter wind speed (km/h): 15
Is GPS available? (yes/no): yes
Expected Result
Risk Level: LOW
Decision: APPROVE
Safety Action: START_MISSION
Success: True
❓ Question 4 — Unsafe Wind

Enter:

What should the drone system check? Check whether it is safe to start the drone mission.
Enter battery percentage: 80
Enter wind speed (km/h): 40
Is GPS available? (yes/no): yes
Expected Result
Risk Level: HIGH
Decision: HUMAN_REVIEW

The system does not automatically execute a high-risk mission.

The Safety Gate requests human approval before proceeding.

❓ Question 5 — GPS Failure

Enter:

What should the drone system check? Check whether it is safe to start the drone mission.
Enter battery percentage: 80
Enter wind speed (km/h): 15
Is GPS available? (yes/no): no
Expected Result
Risk Level: HIGH
Decision: HUMAN_REVIEW

The drone simulator prevents mission execution when GPS is unavailable.

👁️ Vision Agent Example

Run:

python -m agents.vision_agent

The Vision Agent sends the image to Qwen2.5-VL and returns information such as:

Anomaly Detected: False
Anomaly Type: none
Confidence: 0%
Description: ...

The current sample image is a placeholder test image, so it is expected to report no visible anomaly.

🧪 Automated Testing

Run the complete automated test suite:

python -m tests.test_missions

The test suite checks:

Normal Mission
Low Battery
Critical Battery
Unsafe Wind
GPS Failure

Example:

TEST: Normal Mission
Risk: LOW
Decision: APPROVE

TEST: Low Battery
Risk: HIGH
Decision: RETURN_TO_HOME

TEST: Critical Battery
Risk: CRITICAL
Decision: ABORT_MISSION

TEST: Unsafe Wind
Risk: HIGH
Decision: HUMAN_REVIEW

TEST: GPS Failure
Risk: HIGH
Decision: HUMAN_REVIEW
🔍 Test Individual Components
Test RAG
python rag/rag_pipeline.py
Test RAG Agent
python -m agents.rag_agent

Example question:

What should happen if the battery falls below 20 percent during a mission?
Test Risk Agent
python -m agents.risk_agent
Test Vision Agent
python -m agents.vision_agent
Test Mission System
python -m tests.test_missions
💾 Mission Memory

The system stores mission information in:

data/mission_memory.json

The stored information can include:

Mission timestamp
Mission conditions
Risk level
Decision
Drone simulator result

The memory file is intentionally excluded from GitHub because it is generated runtime data.

📄 Mission Reports

After running the complete system, a mission report is automatically generated.

Reports are stored locally in:

reports/

Example:

mission_report_20260905_223015.txt

A report contains:

Mission Data
Vision Analysis
Risk Analysis
AI Decision
RAG Evidence
Safety Gate Result
Drone Simulator Result

The generated reports are excluded from GitHub.

🛡️ Safety Design

Safety-critical decisions are not delegated entirely to the LLM.

The system uses deterministic safety rules such as:

Battery < 30%
    → Block new mission

Battery < 20%
    → Return-to-Home

Battery < 10%
    → Abort mission / safe landing

Wind > 30 km/h
    → Unsafe condition

GPS unavailable
    → Pause / Return / Human Review

High-risk decision
    → Human approval

The system also follows a fail-safe principle:

If required information is not available, the system should request human review instead of inventing a safety decision.

🔐 Security

Sensitive configuration such as API keys is stored in .env.

The .env file is excluded from Git using .gitignore.

The following runtime files are also excluded:

.env
venv/
chroma_db/
reports/
data/mission_memory.json
📁 Project Structure
autonomous-drone-ai/
│
├── agents/
│   ├── decision_agent.py
│   ├── rag_agent.py
│   ├── risk_agent.py
│   └── vision_agent.py
│
├── data/
│   ├── drone_operations_manual.txt
│   ├── drone_safety_policy.txt
│   ├── inspection_procedures.txt
│   ├── mission_history.txt
│   └── images/
│
├── rag/
│   ├── rag_answer.py
│   └── rag_pipeline.py
│
├── safety/
│   └── safety_gate.py
│
├── tests/
│   └── test_missions.py
│
├── tools/
│   ├── drone_simulator.py
│   ├── mission_memory.py
│   └── mission_report.py
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
🎯 Key Features
Feature	Implementation
RAG	LangChain + ChromaDB
Agent Orchestration	LangGraph
Local LLM	Llama 3.2 3B
Vision AI	Qwen2.5-VL 3B
Risk Analysis	Python Risk Agent
Decision Making	Decision Agent
Safety	Deterministic Safety Gate
Human-in-the-Loop	Approval mechanism
Drone Execution	Python Drone Simulator
Memory	JSON-based Mission Memory
Reporting	Automatic Mission Reports
Testing	Automated Mission Test Suite
🚧 Future Improvements

Possible future improvements include:

Real drone simulator integration
PX4 / ArduPilot integration
Real-time sensor streaming
AWS/GCP deployment
Production vector database such as Pinecone or Milvus
Better semantic embedding models
Persistent agent memory
Advanced VLM anomaly detection
Real-time weather APIs
Web-based monitoring dashboard
LangGraph checkpointing
Observability and tracing
More sophisticated human approval workflows
⚠️ Disclaimer

This project is an educational and portfolio-oriented simulation.

It does not control real drones and should not be used for real-world flight operations without appropriate testing, certification, safety validation, and human supervision.
