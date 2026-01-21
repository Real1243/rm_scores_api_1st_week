from flask import Flask, jsonify
from services.rm_scores import get_rm_scores_with_extremes

app = Flask(__name__)

@app.route("/rm-scores", methods=["GET"])
def rm_scores():
    return jsonify(get_rm_scores_with_extremes())

if __name__ == "__main__":
    app.run(debug=True)
