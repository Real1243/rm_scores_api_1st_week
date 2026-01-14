from fastapi import FastAPI
from services.rm_scores import get_rm_scores_with_extremes

app = FastAPI(title="RM Scores API")

@app.get("/rm-scores")
def rm_scores():
    return get_rm_scores_with_extremes()





# from fastapi import FastAPI
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import os
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI(title="RM Scores API")

# def get_db_connection():
#     return psycopg2.connect(
#         host=os.getenv("DB_HOST"),
#         port=os.getenv("DB_PORT"),
#         database=os.getenv("DB_NAME"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD")
#     )

























