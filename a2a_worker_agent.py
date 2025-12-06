from flask import Flask, request, jsonify
import statistics
import time

app = Flask(__name__)

def compute_stats(numbers):
    if not numbers:
        raise ValueError("Empty input list")
    return {
        "count": len(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": statistics.fmean(numbers),
    }

def generate_summary(stats):
    return (
        f"The dataset contains {stats['count']} values. "
        f"The minimum value is {stats['min']}, the maximum value is {stats['max']}, "
        f"and the average value is {stats['mean']:.2f}."
    )

@app.route("/process_task", methods=["POST"])
def process_task():
    """
    A2A-style worker endpoint (Agent B).
    Expected JSON:
    {
        "task_id": "...",
        "operation": "analyze_and_summarize",
        "data": [...]
    }
    """
    start = time.time()
    try:
        payload = request.get_json(force=True)
        task_id = payload.get("task_id")
        operation = payload.get("operation")
        data = payload.get("data", [])

        if operation != "analyze_and_summarize":
            raise ValueError(f"Unsupported operation: {operation}")

        stats = compute_stats(data)
        summary_text = generate_summary(stats)
        duration_ms = (time.time() - start) * 1000.0

        return jsonify({
            "task_id": task_id,
            "status": "success",
            "stats": stats,
            "summary": summary_text,
            "duration_ms": duration_ms
        }), 200
    except Exception as e:
        return jsonify({
            "task_id": payload.get("task_id") if "payload" in locals() else None,
            "status": "error",
            "error": str(e)
        }), 400


if __name__ == "__main__":
    print("🚀 A2A Worker Agent running on http://127.0.0.1:5002")
    app.run(host="127.0.0.1", port=5002)
