# This is the pure python code which does all the calculations on the best score and the worst score
# based on the rm_id's and the superadmin_id of the respective RM's.
import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from psycopg2.extras import RealDictCursor


from psycopg2.extras import RealDictCursor
from db_config import get_db_connection
import json


def get_topic_best_worst_by_region_all_rms(region, superadmin_id):
    query = """
        SELECT um.rm_id, ri.score_json
        FROM investigen.transaction_info ti
        JOIN investigen.user_master um ON ti.rm_id = um.rm_id
        JOIN investigen.recorded_info ri ON ti.record_id = ri.record_id
        WHERE um.region = %s
          AND um.superadminid = %s
          AND ri.score_json IS NOT NULL;
    """

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, (region, superadmin_id))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    rm_topic_scores = {}

    for row in rows:
        rm_id = row.get("rm_id")
        score_json = row.get("score_json")

        if not rm_id or not score_json:
            continue

        if isinstance(score_json, str):
            score_json = json.loads(score_json)

        sections = (
            score_json
            .get("summery_score", {})
            .get("sections", [])
        )

        if rm_id not in rm_topic_scores:
            rm_topic_scores[rm_id] = {}

        for section in sections:
            topic = section.get("topic")
            score_raw = section.get("score")

            if not topic or not score_raw:
                continue

            try:
                score = float(score_raw.split("/")[0])
            except (ValueError, AttributeError):
                continue

            if topic not in rm_topic_scores[rm_id]:
                rm_topic_scores[rm_id][topic] = {
                    "best_score": score,
                    "worst_score": score
                }
            else:
                rm_topic_scores[rm_id][topic]["best_score"] = max(
                    rm_topic_scores[rm_id][topic]["best_score"], score
                )
                rm_topic_scores[rm_id][topic]["worst_score"] = min(
                    rm_topic_scores[rm_id][topic]["worst_score"], score
                )

    return {
        "region": region,
        "results": [
            {
                "rm_id": rm_id,
                "topics": [
                    { 
                        "topic": topic,
                        "best_score": data["best_score"],
                        "worst_score": data["worst_score"]
                    } 
                    for topic, data in topics.items()
                ]
            }
            for rm_id, topics in rm_topic_scores.items()
        ]
    }

if __name__ == "__main__":
    REGION = "Mumbai"
    SUPERADMIN_ID = "SAB001"

    output = get_topic_best_worst_by_region_all_rms(
        region=REGION,
        superadmin_id=SUPERADMIN_ID
    )

    print(json.dumps(output, indent=2))


# def get_topic_best_worst_by_region_all_rms(region, superadmin_id):
#     query = """
#         SELECT 
#             um.rm_id, 
#             ri.score_json
#         FROM investigen.user_master um
#         LEFT JOIN investigen.transaction_info ti 
#             ON ti.rm_id = um.rm_id
#         LEFT JOIN investigen.recorded_info ri 
#             ON ti.record_id = ri.record_id
#         WHERE um.region = %s
#           AND um.superadminid = %s;
#     """

#     conn = get_db_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute(query, (region, superadmin_id))
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()

#     rm_topic_scores = {}

#     for row in rows:
#         rm_id = row.get("rm_id")
#         score_json = row.get("score_json")

#         # Create rm entry even if score_json is None
#         if rm_id not in rm_topic_scores:
#             rm_topic_scores[rm_id] = {}

#         if not score_json:
#             continue

#         if isinstance(score_json, str):
#             score_json = json.loads(score_json)

#         sections = (
#             score_json
#             .get("summery_score", {})
#             .get("sections", [])
#         )

#         for section in sections:
#             topic = section.get("topic")
#             score_raw = section.get("score")

#             if not topic or not score_raw:
#                 continue

#             try:
#                 score = float(score_raw.split("/")[0])
#             except (ValueError, AttributeError):
#                 continue

#             if topic not in rm_topic_scores[rm_id]:
#                 rm_topic_scores[rm_id][topic] = {
#                     "best_score": score,
#                     "worst_score": score
#                 }
#             else:
#                 rm_topic_scores[rm_id][topic]["best_score"] = max(
#                     rm_topic_scores[rm_id][topic]["best_score"], score
#                 )
#                 rm_topic_scores[rm_id][topic]["worst_score"] = min(
#                     rm_topic_scores[rm_id][topic]["worst_score"], score
#                 )

#     return {
#         "region": region,
#         "results": [
#             {
#                 "rm_id": rm_id,
#                 "topics": [
#                     { 
#                         "topic": topic,
#                         "best_score": data["best_score"],
#                         "worst_score": data["worst_score"]
#                     } 
#                     for topic, data in topics.items()
#                 ]
#             }
#             for rm_id, topics in rm_topic_scores.items()
#         ]
#     }

























