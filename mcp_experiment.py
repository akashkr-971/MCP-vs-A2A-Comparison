import json
import time
import uuid
from statistics import mean
from pathlib import Path

import requests

MCP_BASE_URL = "http://127.0.0.1:5001"

def load_dataset(path: str = "common_dataset.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def call_tool(endpoint: str, request_id: str, args: dict):
    url = f"{MCP_BASE_URL}/{endpoint}"
    payload = {
        "request_id": request_id,
        "args": args
    }
    response = requests.post(url, json=payload, timeout=5)
    return response.status_code, response.json()

def run_mcp_experiment():
    data = load_dataset()
    results = []

    print(f"📊 Running MCP experiment on {len(data)} requests...")

    for idx, numbers in enumerate(data, start=1):
        request_id = str(uuid.uuid4())
        overall_start = time.time()
        success = True
        error_msg = None

        try:
            status_code1, resp1 = call_tool(
                "analyze_data",
                request_id=request_id,
                args={"numbers": numbers}
            )
            if status_code1 != 200 or resp1.get("status") != "success":
                raise RuntimeError(f"analyze_data failed: {resp1}")

            stats = resp1.get("stats")

            
            status_code2, resp2 = call_tool(
                "generate_summary",
                request_id=request_id,
                args={"stats": stats}
            )
            if status_code2 != 200 or resp2.get("status") != "success":
                raise RuntimeError(f"generate_summary failed: {resp2}")

            summary_text = resp2.get("summary")

            if not isinstance(summary_text, str) or not summary_text:
                raise RuntimeError("Empty summary returned")

        except Exception as e:
            success = False
            error_msg = str(e)

        overall_end = time.time()
        duration_ms = (overall_end - overall_start) * 1000.0

        results.append({
            "protocol": "MCP",
            "request_index": idx,
            "duration_ms": duration_ms,
            "success": success,
            "error": error_msg,
            "messages_or_calls": 2  # two tool calls per request
        })

        status_str = "OK" if success else "FAIL"
        print(f"[MCP] Request {idx:02d}: {duration_ms:.2f} ms, {status_str}")

    # Compute aggregate metrics
    successful = [r for r in results if r["success"]]
    durations = [r["duration_ms"] for r in successful]

    avg_time = mean(durations) if durations else None
    min_time = min(durations) if durations else None
    max_time = max(durations) if durations else None
    success_rate = (len(successful) / len(results) * 100.0) if results else 0.0

    print("\n=== MCP Experiment Summary ===")
    print(f"Total Requests      : {len(results)}")
    print(f"Successful Requests : {len(successful)}")
    print(f"Success Rate        : {success_rate:.2f} %")
    if durations:
        print(f"Avg Time (ms)       : {avg_time:.2f}")
        print(f"Min Time (ms)       : {min_time:.2f}")
        print(f"Max Time (ms)       : {max_time:.2f}")
    print("Messages/Calls per Request : 2 tool calls")

    out_path = Path("mcp_results.json")
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 MCP detailed results saved to {out_path.resolve()}")


if __name__ == "__main__":
    run_mcp_experiment()
