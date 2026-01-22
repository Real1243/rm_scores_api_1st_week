# Python and SQL Code For the RM Scores -->

from psycopg2.extras import RealDictCursor
from db_config import get_db_connection


def get_region_score_summary(region, exclude_rm_id, superadmin_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    query = """
    WITH rm_scores AS (
        SELECT
            um.rm_id,
            um.name,
            CASE
                WHEN ri.score_json::jsonb
                     -> 'summery_score'
                     -> 'data'
                     ->> 'final_score' LIKE '%%/%%'
                THEN
                    split_part(
                        ri.score_json::jsonb
                        -> 'summery_score'
                        -> 'data'
                        ->> 'final_score',
                        '/',
                        1
                    )::numeric
                ELSE
                    (ri.score_json::jsonb
                     -> 'summery_score'
                     -> 'data'
                     ->> 'final_score')::numeric
            END AS score
        FROM investigen.transaction_info ti
        JOIN investigen.user_master um ON ti.rm_id = um.rm_id
        JOIN investigen.recorded_info ri ON ti.record_id = ri.record_id
        WHERE um.region = 'Mumbai'
          AND um.rm_id <> 'SAB001'
          AND um.superadminid = 'SAB001'
          AND ri.score_json IS NOT NULL
    )
    SELECT
        ROUND(AVG(score), 2) AS average_score, 
        MAX(score) AS best_score,
        MIN(score) AS worst_score
    FROM rm_scores;
    """

    cur.execute(query, (region, exclude_rm_id, superadmin_id))
    result = cur.fetchone()

    cur.close()
    conn.close()

    return result


if __name__ == "__main__":
    print(
        get_region_score_summary("Mumbai", "SAB001", "SAB001")
    )
