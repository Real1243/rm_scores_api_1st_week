import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from psycopg2.extras import RealDictCursor
from db_config import get_db_connection


def get_best_topic_per_rm():
    query = """
    SELECT
        r.rm_id,
        r.score_json,
        um.zone,
        um.region
    FROM investigen.recorded_info r
    JOIN investigen.user_master um
        ON r.rm_id = um.rm_id
    WHERE r.score_json IS NOT NULL;
    """

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    results = []

    for row in rows:
        score_json = row["score_json"]

        if isinstance(score_json, str):
            score_json = json.loads(score_json)

        sections = (
            score_json
                .get("summery_score", {})
                .get("sections", [])
        )

        best_topic = None
        best_score = -1

        for section in sections:
            topic = section.get("topic")
            score = section.get("score")  # "7/10"

            if not topic or not score:
                continue

            try:
                numeric_score = float(score.split("/")[0])
            except Exception:
                continue

            if numeric_score > best_score:
                best_score = numeric_score
                best_topic = topic

        if best_topic is None:
            continue

        results.append({
            "rm_id": row["rm_id"],
            "zone": row["zone"],
            "region": row["region"],
            "best_topic": best_topic,
            "best_topic_score": best_score
        })

    return results


if __name__ == "__main__":
    data = get_best_topic_per_rm()
    print(data[:5])
