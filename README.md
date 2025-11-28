# **Agent-to-Agent (A2A) vs Model Context Protocol (MCP)**

This project benchmarks two coordination strategies — **Agent-to-Agent (A2A)** communication vs **Model Context Protocol (MCP)** tool-based execution — using a shared dataset of numeric arrays. Each protocol processes the same inputs and computes statistics (min, max, mean, count) before generating a summary response.

The experiment runs **fully manually** using Python scripts and lightweight Flask servers. No frameworks or orchestration systems are required.

---

## **📁 Project Structure**

```
.
├── a2a_experiment.py
├── a2a_worker_agent.py
├── a2a_results.json
│
├── mcp_experiment.py
├── mcp_tool_server.py
├── mcp_results.json
│
├── dataset_generator.py
├── common_dataset.json
│
└── README.md
```

---

## **🎯 Experiment Goal**

The objective is to evaluate **latency**, **success rate**, and **message complexity** between:

### ✅ **A2A Protocol**

A coordinator agent sends a task directly to a worker agent.
Two message exchanges per request.

### ✅ **MCP Protocol**

A single orchestrator calls two tools sequentially:

1. `analyze_data`
2. `generate_summary`

Both protocols use identical datasets and identical logic for computing statistics and summarization.

---

## **📌 1. Dataset Generation**

Before running any experiment, generate the shared dataset:

```bash
python dataset_generator.py
```

This creates `common_dataset.json`, which contains 30 random numeric arrays used by both experiments.

Reference: *dataset generator script* 

---

## **📌 2. Running the A2A Experiment**

### **Step 1 — Start the Worker Agent (Agent B)**

```bash
python a2a_worker_agent.py
```

This launches a Flask server at:

```
http://127.0.0.1:5002/process_task
```

The worker computes stats and generates summaries for each request.
Reference: *worker implementation* 

---

### **Step 2 — Run the A2A Experiment Script**

```bash
python a2a_experiment.py
```

The coordinator:

* Loads `common_dataset.json`
* Sends each numeric array as a task to the worker
* Receives the summary
* Logs success, latency, and message count

Results are saved to:

```
a2a_results.json
```

Reference: *A2A experiment coordinator* 
Reference: *A2A results sample* 

---

## **📌 3. Running the MCP Experiment**

### **Step 1 — Start the MCP Tool Server**

```bash
python mcp_tool_server.py
```

This exposes two tools:

```
/analyze_data
/generate_summary
```

Each tool is a separate endpoint.
Reference: *MCP tool server* 

---

### **Step 2 — Run the MCP Experiment Script**

```bash
python mcp_experiment.py
```

The script:

* Loads the same dataset
* Calls the MCP tools in sequence
* Logs request metrics
* Saves results to:

```
mcp_results.json
```

Reference: *MCP experiment coordinator* 
Reference: *MCP results sample* 

---

## **📊 Output Files**

### **1. A2A Results — `a2a_results.json`**

Each entry logs:

* request index
* duration (ms)
* success/failure
* message count (always 2)
* error if any

### **2. MCP Results — `mcp_results.json`**

Same structure but includes latency for both tool calls combined.

---

## **📌 Requirements**

* Python 3.10+
* Flask
* Requests library

Install dependencies (if needed):

```bash
pip install flask requests
```

---

## **🚀 Running Everything Together**

1. Generate dataset

   ```bash
   python dataset_generator.py
   ```

2. Start MCP server

   ```bash
   python mcp_tool_server.py
   ```

3. Start A2A worker

   ```bash
   python a2a_worker_agent.py
   ```

4. Run both experiments

   ```bash
   python mcp_experiment.py
   python a2a_experiment.py
   ```

---
