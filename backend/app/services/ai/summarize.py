import json
from backend.app.services.ai.llm_client import chat_json

SUMMARY_SYSTEM = """
You are a data analyst. Summarize SQL query results for business users.
Be concise, accurate, and do not invent numbers not present in the results.
Return ONLY JSON with keys: answer.
No markdown.
"""

def summarize(question: str, sql: str, columns: list[str], rows: list[list]) -> str:
    payload = {
        "question": question,
        "sql": sql,
        "columns": columns,
        "rows": rows[:50]  # keep small for tokens
    }
    user_prompt = "Summarize this result:\n" + json.dumps(payload)
    raw = chat_json(SUMMARY_SYSTEM, user_prompt)

    try:
        data = json.loads(raw)
        return data.get("answer", "Here are the results.")
    except Exception:
        # fallback if model returns non-JSON
        return "Here are the results."
