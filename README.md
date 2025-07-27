# Project Drishti – Multi-Agent Workflow

Drishti is an AI-powered event monitoring system that leverages multiple autonomous agents to analyze CCTV footage, forecast crowd levels, detect panic or hazards, and generate real-time summaries. It uses Google's Agentic Development Kit (ADK), Gemini models, and a Flask backend to orchestrate interactions between agents.

## 🧠 Architecture Overview

Drishti is composed of a **Root Agent** that coordinates several **Child Agents**, each handling a distinct capability:

- 🔍 `SummaryAgent` — Generates real-time event summaries using Firestore logs and Gemini.
- 📈 `ForecastAgent` — Predicts future crowd density using time-series data and BQML or ARIMA.
- 🎯 `PanicDetectionAgent` — Detects chaos or panic in video feeds using Gemini + MoviePy.
- 🚨 `SosAgent` — Triggers SOS alerts based on hazard detection or crowd severity.
- 🗺️ `NavigationAgent` — Recommends the safest exit routes using Google Maps + crowd data.

Agents communicate using ADK’s multi-agent orchestration interface.

---

## 🧪 Environment Setup

This project runs in a **Nix-based environment** managed by **Firebase Studio** and uses **Python 3**.

### 1. Activate the virtual environment
```bash
source .venv/bin/activate
adk run multi_tool_agent/