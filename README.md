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