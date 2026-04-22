from llm import ask_llm
from db import engine
from sqlalchemy import text
import re

def clean_sql(sql):
    # Remove ```sql ... ``` or ``` ... ``` blocks
    sql = re.sub(r"```(?:sql)?", "", sql, flags=re.IGNORECASE)
    # Remove any remaining backticks
    sql = sql.replace("`", "")
    # Remove lines that are just the word "sql"
    lines = [line for line in sql.splitlines() if line.strip().lower() != "sql"]
    sql = "\n".join(lines)
    return sql.strip()

def fix_sql(sql, error):
    prompt = f"""
Fix this SQL query for SQLite. Return only the corrected SQL, no explanation.

Query: {sql}
Error: {error}
"""
    fixed = ask_llm(prompt)
    return clean_sql(fixed)

def run_pipeline(query):
    prompt = f"""
Convert the following natural language query to a valid SQL query for a SQLite database.
The database has two tables:
- sales: id (INTEGER), product (TEXT), region (TEXT), amount (INTEGER), customer_id (INTEGER)
- customers: id (INTEGER), name (TEXT), city (TEXT)

Query: {query}

Return only the SQL query, no explanations, no markdown.
"""
    sql = clean_sql(ask_llm(prompt))

    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql)).fetchall()
        return sql, result
    except Exception as e:
        # Self-healing: ask LLM to fix and retry once
        fixed_sql = fix_sql(sql, str(e))
        try:
            with engine.connect() as conn:
                result = conn.execute(text(fixed_sql)).fetchall()
            return fixed_sql, result
        except Exception as e2:
            return fixed_sql, str(e2)