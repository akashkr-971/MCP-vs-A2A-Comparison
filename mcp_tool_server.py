from flask import Flask, request, jsonify
import statistics
import time

app = Flask(__name__)

def compute_stats(numbers):
    """Compute simple statistics from a list of numbers."""
    if not numbers:
        raise ValueError("Empty input list")
    return {
        "count": len(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": statistics.fmean(numbers),
    }

def generate_summary(stats):
    """Generate a simple text summary from stats dict."""
    return (
        f"The dataset contains {stats['count']} values. "
        f"The minimum value is {stats['min']}, the maximum value is {stats['max']}, "
        f"and the average value is {stats['mean']:.2f}."
    )

@app.route("/analyze_data", methods=["POST"])
def analyze_data():
    """
    MCP-like tool: analyze_data
    Expected JSON:
    {
        "request_id": "...",
        "args": {
            "numbers": [...]
        }
    }
    """
    start = time.time()
    try:
        payload = request.get_json(force=True)
        request_id = payload.get("request_id")
        args = payload.get("args", {})
        numbers = args.get("numbers", [])

        stats = compute_stats(numbers)
        duration_ms = (time.time() - start) * 1000.0

        return jsonify({
            "request_id": request_id,
            "tool": "analyze_data",
            "status": "success",
            "stats": stats,
            "duration_ms": duration_ms
        }), 200
    except Exception as e:
        return jsonify({
            "request_id": payload.get("request_id") if "payload" in locals() else None,
            "tool": "analyze_data",
            "status": "error",
            "error": str(e)
        }), 400

@app.route("/generate_summary", methods=["POST"])
def summary():
    """
    MCP-like tool: generate_summary
    Expected JSON:
    {
        "request_id": "...",
        "args": {
            "stats": { ... }
        }
    }
    """
    start = time.time()
    try:
        payload = request.get_json(force=True)
        request_id = payload.get("request_id")
        args = payload.get("args", {})
        stats = args.get("stats")

        if not isinstance(stats, dict):
            raise ValueError("Missing or invalid 'stats' in args")

        summary_text = generate_summary(stats)
        duration_ms = (time.time() - start) * 1000.0

        return jsonify({
            "request_id": request_id,
            "tool": "generate_summary",
            "status": "success",
            "summary": summary_text,
            "duration_ms": duration_ms
        }), 200
    except Exception as e:
        return jsonify({
            "request_id": payload.get("request_id") if "payload" in locals() else None,
            "tool": "generate_summary",
            "status": "error",
            "error": str(e)
        }), 400


if __name__ == "__main__":
    print("🚀 MCP Tool Server running on http://127.0.0.1:5001")
    app.run(host="127.0.0.1", port=5001)
