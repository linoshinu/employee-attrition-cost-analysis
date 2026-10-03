"""Execute each statement in sql/analysis_queries.sql and print its result."""

from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "employee_attrition.sqlite"
QUERY_FILE = ROOT / "sql" / "analysis_queries.sql"


def main() -> None:
    if not DB.exists():
        raise FileNotFoundError("Run `python scripts/load_sqlite.py` first.")
    source = QUERY_FILE.read_text(encoding="utf-8")
    statements: list[str] = []
    buffer = ""
    for line in source.splitlines():
        buffer += line + "\n"
        if sqlite3.complete_statement(buffer):
            if buffer.strip() and any(not item.strip().startswith("--") for item in buffer.splitlines()):
                statements.append(buffer)
            buffer = ""

    with sqlite3.connect(DB) as connection:
        for number, statement in enumerate(statements, start=1):
            cursor = connection.execute(statement)
            if cursor.description:
                rows = cursor.fetchall()
                print(f"\nQuery {number}")
                print(" | ".join(column[0] for column in cursor.description))
                for row in rows:
                    print(" | ".join(str(value) for value in row))


if __name__ == "__main__":
    main()
