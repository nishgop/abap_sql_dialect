# Quick Start Guide

Get started with the ABAP SQL Syntax Checker in 5 minutes.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Test

```bash
# Run demo
python abap_sql_checker.py

# Run all tests
python run_all_tests.py
```

## Basic Usage

### 1. Command Line

```bash
# Interactive mode
python interactive_checker.py

# Validate a file
python batch_validator.py example_queries.sql
```

### 2. Python Code

```python
from abap_sql_checker import ABAPSQLChecker

checker = ABAPSQLChecker()

# Check syntax
sql = "SELECT carrid, connid FROM sflight WHERE carrid = 'AA'"
is_valid, ast, errors = checker.check_syntax(sql)

if is_valid:
    print("✓ Valid SQL")
else:
    print(f"✗ Errors: {errors}")

# Analyze query
analysis = checker.analyze_query(sql)
print(f"Tables: {analysis['tables']}")
print(f"Columns: {analysis['columns']}")
```

## Example Queries

### Standard SQL

```sql
-- Basic SELECT
SELECT carrid, connid, fldate FROM sflight WHERE carrid = 'AA';

-- JOIN
SELECT f.carrid, p.cityfrom 
FROM sflight AS f 
INNER JOIN spfli AS p ON f.carrid = p.carrid;

-- Aggregate
SELECT carrid, COUNT(*) as cnt 
FROM sflight 
GROUP BY carrid 
HAVING COUNT(*) > 10;
```

### ABAP-Specific

```sql
-- SELECT SINGLE
SELECT SINGLE * FROM sflight WHERE carrid = 'AA';

-- Modern host variables (@)
SELECT carrid FROM sflight WHERE carrid = @lv_carrid;

-- Tilde operator
SELECT f~carrid, p~cityfrom 
FROM sflight AS f 
INNER JOIN spfli AS p ON f~carrid = p~carrid;

-- String operators
SELECT * FROM customers WHERE name CP '*Smith*';
SELECT * FROM products WHERE code CO '0123456789';

-- FOR UPDATE
SELECT * FROM sflight WHERE carrid = 'AA' FOR UPDATE;
```

## Testing

```bash
# All tests (178 total)
python run_all_tests.py

# Individual suites
python test_checker.py              # Basic (14 tests)
python test_checker_extended.py     # SQL variants (69 tests)
python test_abap_specific.py        # ABAP features (38 tests)
python test_abap_enhanced.py        # Enhanced ABAP (36 tests)
python test_negative.py             # Error detection (21 tests)
```

## Key Features

### ✅ What Works (94% - 167/178 tests)
- All standard SQL (JOINs, aggregates, window functions, etc.)
- ABAP SELECT SINGLE
- Host variables (@var and :var)
- Tilde operator (~)
- String operators (CP, CS, CA, CO, NP, NS, NA, CN)
- ABAP functions (CONCAT_WITH_SPACE, STRING_AGG, CAST)
- FOR UPDATE
- 100% error detection (21/21 tests)

### ⚠️ Limited Support (6% - 11/178 tests)
- UP TO n ROWS (use LIMIT instead)
- BYPASSING BUFFER  
- CLIENT SPECIFIED
- PACKAGE SIZE
- Some INTO variations

## Common Tasks

### Validate Multiple Files

```bash
python batch_validator.py sql_files/*.sql
```

### Format SQL

```python
formatted = checker.format_sql(sql, pretty=True)
print(formatted)
```

### Get Detailed Analysis

```python
analysis = checker.analyze_query(sql)
print(analysis['query_type'])    # SELECT, INSERT, etc.
print(analysis['tables'])         # ['sflight', 'spfli']
print(analysis['columns'])        # ['carrid', 'connid']
print(analysis['has_where'])      # True/False
print(analysis['has_join'])       # True/False
```

## Next Steps

- **Full Documentation**: See [README.md](README.md)
- **Technical Details**: See [ABAP_DIALECT_GUIDE.md](ABAP_DIALECT_GUIDE.md)
- **Example SQL**: Check `example_queries*.sql` files

## Troubleshooting

**Issue**: Import errors  
**Fix**: `pip install -r requirements.txt`

**Issue**: Test failures  
**Fix**: Check you're in the project directory

**Issue**: Unsupported ABAP clause  
**Fix**: See Known Limitations in [README.md](README.md#-known-limitations)

---

**Repository**: https://github.com/nishgop/abap_sql_dialect  
**Version**: 3.0.0  
**Tests**: 167/178 passing (94%)
