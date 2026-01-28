from flask import Flask, jsonify, render_template, request
from services.region_superadminid_scores import get_topic_best_worst_by_region_all_rms

app = Flask(__name__, template_folder="../frontend")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/rm-topic-scores", methods=["GET"])
def rm_scores():
    try:
        # Read query params (if provided)
        region = request.args.get("region")
        superadmin_id = request.args.get("superadmin_id")

        # If not provided, use default values (so normal UI works)
        if not region:
            region = "Mumbai"
        if not superadmin_id:
            superadmin_id = "SAB001"

        result = get_topic_best_worst_by_region_all_rms(region, superadmin_id)

        # If result is empty or invalid
        if not result or not result.get("results"):
            return jsonify({"message": "No data found"}), 204  # No Content

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
