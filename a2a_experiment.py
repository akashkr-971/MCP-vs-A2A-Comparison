import json
import time
import uuid
from statistics import mean
from pathlib import Path

import requests

A2A_WORKER_URL = "http://127.0.0.1:5002/process_task"

def load_dataset(path: str = "common_dataset.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def send_task_to_worker(task_id: str, data):
    payload = {
        "task_id": task_id,
        "operation": "analyze_and_summarize",
        "data": data
    }
    response = requests.post(A2A_WORKER_URL, json=payload, timeout=5)
    return response.status_code, response.json()

def run_a2a_experiment():
    data = load_dataset()
    results = []

    print(f"📊 Running A2A experiment on {len(data)} requests...")

    for idx, numbers in enumerate(data, start=1):
        task_id = str(uuid.uuid4())
        overall_start = time.time()
        success = True
        error_msg = None

        try:
            status_code, resp = send_task_to_worker(task_id, numbers)

            if status_code != 200 or resp.get("status") != "success":
                raise RuntimeError(f"Worker failed: {resp}")

            summary_text = resp.get("summary")
            if not isinstance(summary_text, str) or not summary_text:
                raise RuntimeError("Empty summary returned from worker")

        except Exception as e:
            success = False
            error_msg = str(e)

        overall_end = time.time()
        duration_ms = (overall_end - overall_start) * 1000.0

        
        # 1) A -> B, 2) B -> A
        results.append({
            "protocol": "A2A",
            "request_index": idx,
            "duration_ms": duration_ms,
            "success": success,
            "error": error_msg,
            "messages_or_calls": 2  # two agent messages per request
        })

        status_str = "OK" if success else "FAIL"
        print(f"[A2A] Request {idx:02d}: {duration_ms:.2f} ms, {status_str}")

    successful = [r for r in results if r["success"]]
    durations = [r["duration_ms"] for r in successful]

    avg_time = mean(durations) if durations else None
    min_time = min(durations) if durations else None
    max_time = max(durations) if durations else None
    success_rate = (len(successful) / len(results) * 100.0) if results else 0.0

    print("\n=== A2A Experiment Summary ===")
    print(f"Total Requests      : {len(results)}")
    print(f"Successful Requests : {len(successful)}")
    print(f"Success Rate        : {success_rate:.2f} %")
    if durations:
        print(f"Avg Time (ms)       : {avg_time:.2f}")
        print(f"Min Time (ms)       : {min_time:.2f}")
        print(f"Max Time (ms)       : {max_time:.2f}")
    print("Messages/Calls per Request : 2 agent messages")

    out_path = Path("a2a_results.json")
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 A2A detailed results saved to {out_path.resolve()}")


if __name__ == "__main__":
    run_a2a_experiment()
