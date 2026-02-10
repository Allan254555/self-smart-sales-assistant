def format_chart(rows, columns, chart_spec):
    if not chart_spec:
        return {"type": "table", "columns": columns, "rows": rows}

    ctype = chart_spec.get("type", "table")
    x_col = chart_spec.get("x")
    y_col = chart_spec.get("y")

    if ctype in ("bar", "line", "pie") and x_col in columns and y_col in columns:
        xi = columns.index(x_col)
        yi = columns.index(y_col)
        return {
            "type": ctype,
            "x": [r[xi] for r in rows],
            "y": [float(r[yi]) if r[yi] is not None else 0.0 for r in rows],
            "x_label": x_col,
            "y_label": y_col
        }

    return {"type": "table", "columns": columns, "rows": rows}
