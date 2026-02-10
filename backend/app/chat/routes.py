from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.app.services.ai.nl2sql import question_to_sql
from etl.load.clickhouse_loader import get_clickhouse_client
from backend.app.services.ai.summarize import summarize

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

class ChatRequest(BaseModel):
    question: str

@router.post("/query")
def chat_query(req: ChatRequest):
    data = question_to_sql(req.question)
    if "error" in data:
        return {"answer": "I couldn't generate a safe SQL query for that question.", "error": data["error"], "sql": data.get("sql")}
    sql = data["sql"]

    ch = get_clickhouse_client()
    res = ch.query(sql)
    columns = res.column_names
    rows = res.result_rows

    answer = summarize(req.question, sql, columns, rows)
    return {
        "answer": answer,
        "sql": sql,
        "columns": columns,
        "rows": rows[:20],

    }