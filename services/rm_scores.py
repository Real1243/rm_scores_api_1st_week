from psycopg2.extras import RealDictCursor
from db_config import get_db_connection

def get_rm_scores_with_extremes():
    query = """
    SELECT
        um.zone,
        um.region,
        r.rm_id,
        ROUND(AVG(
            regexp_replace(
                (r.score_json::jsonb
                    -> 'summery_score'
                    -> 'data'
                    ->> 'final_score'),
                '/.*', '', 'g'
            )::numeric
        ), 2) AS avg_rm_score,
        ROUND(MAX(
            regexp_replace(
                (r.score_json::jsonb
                    -> 'summery_score'
                    -> 'data'
                    ->> 'final_score'),
                '/.*', '', 'g'
            )::numeric
        ), 2) AS best_score,
        ROUND(MIN(
            regexp_replace(
                (r.score_json::jsonb
                    -> 'summery_score'
                    -> 'data'
                    ->> 'final_score'),
                '/.*', '', 'g'
            )::numeric
        ), 2) AS worst_score
    FROM investigen.recorded_info r
    JOIN investigen.user_master um
        ON r.rm_id = um.rm_id
    WHERE r.score_json IS NOT NULL
      AND um.zone IS NOT NULL
      AND um.region IS NOT NULL
    GROUP BY um.zone, um.region, r.rm_id
    ORDER BY avg_rm_score DESC
    LIMIT 20;
    """

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()

    return results
