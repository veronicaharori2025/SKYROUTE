
import sys
import os

# Make Python find the local hyperon Python folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hyperon-experimental', 'python'))
# app.py
from flask import Flask, request, jsonify, render_template, send_from_directory
from metta_integration import add_route, find_route
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    # serve the HTML page (templates/index.html)
    return render_template("index.html")

@app.route("/find-route", methods=["GET"])
def api_find_route():
    start = request.args.get("start")
    end = request.args.get("end")
    criteria = request.args.get("criteria", "Duration")
    if not start or not end:
        return jsonify({"error": "start and end parameters required"}), 400
    res = find_route(start, end, criteria)
    return jsonify(res), 200

@app.route("/add-route", methods=["POST"])
def api_add_route():
    data = request.json or {}
    try:
        add_route(data["from"], data["to"], data["airline"], data["duration"], data["cost"], data.get("layovers", 0))
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# optional: static files
@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(debug=True)
