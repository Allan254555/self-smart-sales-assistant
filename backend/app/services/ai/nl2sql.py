import json
from backend.app.services.ai.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from backend.app.services.ai.llm_client import chat_json
from backend.app.services.ai.sql_guard import is_safe_sql

def question_to_sql(question: str) -> dict:
    user_prompt = USER_PROMPT_TEMPLATE.format(question=question)
    raw = chat_json(SYSTEM_PROMPT, user_prompt)

    # Gemini returns text; we expect JSON string
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "LLM did not return valid JSON.", "raw": raw}

    sql = data.get("sql", "")
    ok, fixed_or_err = is_safe_sql(sql)
    if not ok:
        return {"error": fixed_or_err, "sql": sql, "raw": raw}

    return {"sql": fixed_or_err, "reasoning": data.get("reasoning", "")}
