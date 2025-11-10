# Quick Start Guide - ABAP SQL Syntax Checker

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage Examples

### 1. Run the Demo Script

The fastest way to see the checker in action:

```bash
python abap_sql_checker.py
```

This runs pre-defined test queries and shows detailed analysis.

### 2. Interactive Mode

For an interactive command-line interface:

```bash
python interactive_checker.py
```

Features:
- Check SQL syntax interactively
- Format SQL statements
- Load SQL from files
- Run built-in examples

### 3. Use as a Python Library

```python
from abap_sql_checker import ABAPSQLChecker

# Create checker instance
checker = ABAPSQLChecker()

# Example 1: Basic syntax check
sql = "SELECT carrid, connid FROM sflight WHERE carrid = 'AA'"
is_valid, ast, errors = checker.check_syntax(sql)

if is_valid:
    print("✓ SQL is valid!")
else:
    print("✗ Errors found:")
    for error in errors:
        print(f"  - {error}")

# Example 2: Full analysis
analysis = checker.analyze_query(sql)
print(f"Tables: {analysis['tables']}")
print(f"Columns: {analysis['columns']}")
print(f"Has WHERE: {analysis['has_where_clause']}")

# Example 3: Format SQL
formatted = checker.format_sql(sql, pretty=True)
print(formatted)
```

### 4. Check SQL File

Check all queries in a file:

```python
from abap_sql_checker import ABAPSQLChecker

checker = ABAPSQLChecker()

with open('example_queries.sql', 'r') as f:
    sql_content = f.read()

# Split by semicolon
queries = [q.strip() for q in sql_content.split(';') if q.strip()]

for i, query in enumerate(queries, 1):
    print(f"\n=== Query {i} ===")
    analysis = checker.analyze_query(query)
    
    if analysis['valid']:
        print(f"✓ Valid - Tables: {', '.join(analysis['tables'])}")
    else:
        print(f"✗ Invalid - Errors: {analysis['errors']}")
```

## Common ABAP SQL Patterns

### Basic SELECT
```sql
SELECT carrid, connid, fldate
FROM sflight
WHERE carrid = 'AA';
```

### JOIN
```sql
SELECT f.carrid, f.connid, p.cityfrom, p.cityto
FROM sflight AS f
INNER JOIN spfli AS p
  ON f.carrid = p.carrid
  AND f.connid = p.connid
WHERE f.carrid = 'LH';
```

### Aggregates
```sql
SELECT carrid, COUNT(*) as flight_count, AVG(seatsocc) as avg_seats
FROM sflight
GROUP BY carrid
HAVING COUNT(*) > 10
ORDER BY flight_count DESC;
```

### Subquery
```sql
SELECT carrid, connid
FROM spfli
WHERE carrid IN (
  SELECT DISTINCT carrid
  FROM sflight
  WHERE seatsocc > 250
);
```

### CASE Expression
```sql
SELECT carrid,
       CASE
         WHEN seatsocc > 200 THEN 'HIGH'
         WHEN seatsocc > 100 THEN 'MEDIUM'
         ELSE 'LOW'
       END as occupancy_level
FROM sflight;
```

## Understanding the Output

### Valid Query
```
======================================================================
ABAP SQL SYNTAX CHECK REPORT
======================================================================

✓ Valid Syntax: True

SQL Statement:
SELECT carrid, connid FROM sflight WHERE carrid = 'AA'

📊 QUERY ANALYSIS:
  Query Type: Select
  Tables: sflight
  Columns: carrid, connid
  Has WHERE clause: True
  Has JOIN: False
  Has GROUP BY: False
  Has ORDER BY: False

======================================================================
```

### Invalid Query
```
======================================================================
ABAP SQL SYNTAX CHECK REPORT
======================================================================

✓ Valid Syntax: False

SQL Statement:
SELECT FROM WHERE

❌ ERRORS:
  • Syntax error: Expected table name but got WHERE

======================================================================
```

### With Warnings
```
⚠ WARNINGS:
  • Using SELECT * is discouraged in ABAP SQL. Specify explicit columns.
```

## Tips

1. **Specify Columns**: Avoid `SELECT *` for better performance
2. **Use Aliases**: Make complex queries more readable
3. **Index Conditions**: Put indexed fields in WHERE clauses
4. **Limit Results**: Use appropriate WHERE conditions to limit result sets
5. **Test First**: Always validate syntax before running in production

## API Reference

### ABAPSQLChecker Class

#### `__init__(dialect: str = "postgres")`
Initialize the checker with specified SQL dialect.

#### `check_syntax(sql: str) -> Tuple[bool, Optional[exp.Expression], List[str]]`
Check SQL syntax. Returns (is_valid, AST, errors).

#### `analyze_query(sql: str) -> Dict`
Perform full analysis. Returns dictionary with:
- `valid`: bool
- `errors`: list of error messages
- `warnings`: list of warnings
- `query_type`: type of query (Select, Insert, etc.)
- `tables`: list of table names
- `columns`: list of column names
- `has_where_clause`: bool
- `has_join`: bool
- `has_group_by`: bool
- `has_order_by`: bool

#### `format_sql(sql: str, pretty: bool = True) -> Optional[str]`
Format SQL statement. Returns formatted string or None.

## Troubleshooting

### Import Error
```
ImportError: No module named 'sqlglot'
```
**Solution**: Run `pip install -r requirements.txt`

### Parse Error
If valid ABAP SQL is flagged as invalid, the dialect may not support that specific syntax. You can:
1. Use standard SQL equivalents
2. Extend the checker with custom validation
3. Report unsupported syntax

## Next Steps

- Check out `example_queries.sql` for more examples
- Read `README.md` for detailed documentation
- Run `python test_checker.py` to see all test cases
- Extend the checker with custom validations

## Support

For ABAP SQL syntax reference:
- [ABAP SQL Reference](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/abensql.htm)
- [SQLGlot Documentation](https://sqlglot.com/sqlglot.html)

