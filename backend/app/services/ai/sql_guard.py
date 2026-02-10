import re

BLOCKED = re.compile(r"\b(insert|update|delete|drop|alter|truncate|attach|detach|system|create)\b", re.I)

ALLOWED_TABLES = {
    "categories","cities","countries","customer_sales_summary","customers",
    "daily_product_sales","employees","monthly_category_sales","monthly_city_sales",
    "monthly_country_sales","monthly_customer_sales","monthly_product_sales",
    "monthly_salesperson_sales","products","sales"
}

def is_safe_sql(sql: str) -> tuple[bool, str]:
    s = sql.strip().rstrip(";")
    if not s.lower().startswith(("select", "with")):
        return False, "Only SELECT/WITH queries are allowed."
    if BLOCKED.search(s):
        return False, "Query contains a blocked keyword."

    # basic table name allowlist check (simple but effective)
    # looks for FROM/JOIN <name>
    tables = re.findall(r"\b(from|join)\s+([a-zA-Z_][a-zA-Z0-9_]*)", s, flags=re.I)
    used = {t[1].lower() for t in tables}
    bad = [t for t in used if t not in ALLOWED_TABLES]
    if bad:
        return False, f"Query uses non-allowed tables: {bad}"

    # enforce LIMIT if result set could be large
    if "limit" not in s.lower():
        s += " LIMIT 200"
    return True, s
