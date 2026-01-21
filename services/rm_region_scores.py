from psycopg2.extras import RealDictCursor
from db_config import get_db_connection


def get_region_rm_scores(region, session_rm_id, superadmin_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    query = """
            SELECT
        um.rm_id,
        um.name,
        ri.score_json
    FROM investigen.transaction_info ti
    JOIN investigen.user_master um
        ON ti.rm_id = um.rm_id
    JOIN investigen.recorded_info ri
        ON ti.record_id = ri.record_id
    WHERE um.region = 'Mumbai'
    AND um.rm_id <> 'SAB001'
    AND um.superadminid = 'SAB001'
    AND ri.score_json IS NOT NULL;
    """

    cur.execute(query, (region, session_rm_id, superadmin_id))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    scores = []

    for row in rows:
        try:
            score = float(
                row["score_json"]["summery_score"]["data"]["final_score"].split("/")[0]
            )
            scores.append({
                "rm_id": row["rm_id"],
                "name": row["name"],
                "score": score
            })
        except Exception:
            continue

    if not scores:
        return {}

    best = max(scores, key=lambda x: x["score"])
    worst = min(scores, key=lambda x: x["score"])
    average = round(sum(s["score"] for s in scores) / len(scores), 2)

    return {
        "region": region,
        "average_score": average,
        "best_rm": best,
        "worst_rm": worst
    }


if __name__ == "__main__":
    region = "Mumbai"
    session_rm_id = "RM001"
    superadmin_id = "SA001"

    result = get_region_rm_scores(region, session_rm_id, superadmin_id)
    print(result)
