from psycopg2.extras import RealDictCursor
from db_config import get_db_connection
from collections import defaultdict

def get_rm_scores_with_extremes():
    query = """
    SELECT
        r.rm_id,
        r.score_json,
        um.zone,
        um.region
    FROM investigen.recorded_info r
    JOIN investigen.user_master um
        ON r.rm_id = um.rm_id
    WHERE r.score_json IS NOT NULL
      AND um.zone IS NOT NULL
      AND um.region IS NOT NULL;
    """

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Group scores by (zone, region, rm_id)
    score_map = defaultdict(list)

    for row in rows:
        try:
            score = float(
                row["score_json"]["summery_score"]["data"]["final_score"]
            )
            key = (row["zone"], row["region"], row["rm_id"])
            score_map[key].append(score)
        except Exception:
            # Skip malformed / missing scores safely
            continue

    results = []

    for (zone, region, rm_id), scores in score_map.items():
        avg_score = round(sum(scores) / len(scores), 2)
        best_score = round(max(scores), 2)
        worst_score = round(min(scores), 2)

        results.append({
            "zone": zone,
            "region": region,
            "rm_id": rm_id,
            "avg_rm_score": avg_score,
            "best_score": best_score,
            "worst_score": worst_score
        })

    # Sort by average score (descending) and take top 20
    results.sort(key=lambda x: x["avg_rm_score"], reverse=True)

    return results[:20]
