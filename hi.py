# from fastapi import FastAPI, HTTPException
# import psycopg2
# from psycopg2.extras import RealDictCursor

# app = FastAPI(title="RM Scores API")

# # DB connection function
# def get_db_connection():
#     try:
#         conn = psycopg2.connect(
#             host="34.93.126.207",
#             port=5432,
#             database="tvaweb",
#             user="intern_user",
#             password="Investigen@User1"
#         )
#         return conn
#     except Exception as e:
#         print("DB connection error:", e)
#         raise HTTPException(status_code=500, detail="Database connection failed")


# # GET endpoint to fetch RM scores
# @app.get("/rm-scores")
# def get_rm_scores():
#     query = """
#     SELECT
#         um.zone,
#         um.region,
#         r.rm_id,
#         ROUND(
#             AVG(
#                 regexp_replace(
#                     (r.score_json::jsonb
#                         -> 'summery_score'
#                         -> 'data'
#                         ->> 'final_score'),
#                     '/.*', '', 'g'
#                 )::numeric
#             ), 2
#         ) AS avg_rm_score
#     FROM investigen.recorded_info r
#     JOIN investigen.user_master um
#         ON r.rm_id = um.rm_id
#     WHERE r.score_json IS NOT NULL
#       AND um.zone IS NOT NULL
#       AND um.region IS NOT NULL
#     GROUP BY
#         um.zone,
#         um.region,
#         r.rm_id
#     ORDER BY avg_rm_score DESC
#     LIMIT 10;
#     """
#     conn = get_db_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute(query)
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()
#     return rows


# # POST endpoint (example: fetch scores filtered by zone)
# @app.post("/rm-scores/filter")
# def post_rm_scores(filter_data: dict):
#     zone = filter_data.get("zone")
#     if not zone:
#         raise HTTPException(status_code=400, detail="Zone is required")
    
#     query = """
#     SELECT
#         um.zone,
#         um.region,
#         r.rm_id,
#         ROUND(
#             AVG(
#                 regexp_replace(
#                     (r.score_json::jsonb
#                         -> 'summery_score'
#                         -> 'data'
#                         ->> 'final_score'),
#                     '/.*', '', 'g'
#                 )::numeric
#             ), 2
#         ) AS avg_rm_score
#     FROM investigen.recorded_info r
#     JOIN investigen.user_master um
#         ON r.rm_id = um.rm_id
#     WHERE r.score_json IS NOT NULL
#       AND um.zone = %s
#     GROUP BY
#         um.zone,
#         um.region,
#         r.rm_id
#     ORDER BY avg_rm_score DESC
#     LIMIT 10;
#     """
    
#     conn = get_db_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute(query, (zone,))
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()
#     return rows


# import psycopg2
# from psycopg2.extras import RealDictCursor

# def get_rm_scores_with_extremes():
#     query = """
#     SELECT
#         um.zone,
#         um.region,
#         r.rm_id,
#         ROUND(AVG(
#             regexp_replace(
#                 (r.score_json::jsonb
#                     -> 'summery_score'
#                     -> 'data'
#                     ->> 'final_score'),
#                 '/.*', '', 'g'
#             )::numeric
#         ), 2) AS avg_rm_score,
#         ROUND(MAX(
#             regexp_replace(
#                 (r.score_json::jsonb
#                     -> 'summery_score'
#                     -> 'data'
#                     ->> 'final_score'),
#                 '/.*', '', 'g'
#             )::numeric
#         ), 2) AS best_score,
#         ROUND(MIN(
#             regexp_replace(
#                 (r.score_json::jsonb
#                     -> 'summery_score'
#                     -> 'data'
#                     ->> 'final_score'),
#                 '/.*', '', 'g'
#             )::numeric
#         ), 2) AS worst_score
#     FROM investigen.recorded_info r
#     JOIN investigen.user_master um
#         ON r.rm_id = um.rm_id
#     WHERE r.score_json IS NOT NULL
#       AND um.zone IS NOT NULL
#       AND um.region IS NOT NULL
#     GROUP BY um.zone, um.region, r.rm_id
#     ORDER BY avg_rm_score DESC
#     LIMIT 20;
#     """

#     conn = psycopg2.connect(
#         host="34.93.126.207",
#         port=5432,
#         database="tvaweb",
#         user="intern_user",
#         password="Investigen@User1"
#     )
    
#     cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute(query)
#     results = cur.fetchall()
#     cur.close()
#     conn.close()
    
#     return results


# # Example usage
# for row in get_rm_scores_with_extremes():
#     print(row)


# from fastapi import FastAPI
# import psycopg2
# from psycopg2.extras import RealDictCursor

# app = FastAPI(title="RM Scores API")  # <-- This 'app' is what Uvicorn looks for

# def get_db_connection():
#     return psycopg2.connect(
# #         host="34.93.126.207",
# #         port=5432,
# #         database="tvaweb",
# #         user="intern_user",
# #         password="Investigen@User1"
# #     )

# # @app.get("/rm-scores")
# # def get_rm_scores():
# #     query = """... your RM scores query with AVG, MAX, MIN ..."""
# #     conn = get_db_connection()
# #     cur = conn.cursor(cursor_factory=RealDictCursor)
# #     cur.execute(query)
# #     rows = cur.fetchall()
# #     cur.close()
# #     conn.close()
# #     return rows
