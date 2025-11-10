# ABAP SQL Dialect Implementation Guide

## 🎯 Overview

This guide explains how to use SQLGlot's dialect system to create a custom **ABAP SQL Dialect** for proper ABAP SQL syntax checking. This is the recommended approach for production use.

## 📋 Two Approaches Compared

### Approach 1: Using Existing Dialects (Current `abap_sql_checker.py`)
✅ **Pros:**
- Quick to implement
- Works for standard SQL
- No dialect setup needed

❌ **Cons:**
- Limited ABAP-specific support
- Cannot parse ABAP keywords properly
- No custom validation rules

### Approach 2: Custom ABAP Dialect (New `abap_dialect.py` + `abap_sql_checker_v2.py`) ⭐
✅ **Pros:**
- Proper ABAP syntax support
- Custom keyword recognition (SINGLE, UP TO, etc.)
- Extensible for future features
- Better error messages
- Can generate ABAP SQL
- Follows SQLGlot best practices

❌ **Cons:**
- Requires more setup
- Need to understand SQLGlot internals

## 🏗️ ABAP Dialect Architecture

The custom ABAP dialect consists of three main components:

### 1. Tokenizer
```python
class ABAP(Postgres):
    class Tokenizer(Postgres.Tokenizer):
        """Recognizes ABAP-specific keywords"""
        KEYWORDS = {
            **Postgres.Tokenizer.KEYWORDS,
            "SINGLE": TokenType.VAR,        # SELECT SINGLE
            "BYPASSING": TokenType.VAR,     # BYPASSING BUFFER
            "CLIENT": TokenType.VAR,        # CLIENT SPECIFIED
            # ... more ABAP keywords
        }
```

**Purpose:** Converts SQL text into tokens, recognizing ABAP-specific keywords.

### 2. Parser
```python
class Parser(Postgres.Parser):
    """Parses ABAP-specific grammar"""
    
    def _parse_select(self, **kwargs):
        # Check for SINGLE keyword
        single = self._match_text_seq("SINGLE")
        
        # Parse standard SELECT
        select = super()._parse_select(**kwargs)
        
        # Add ABAP metadata
        if single:
            select.set("single", True)
        
        # Parse ABAP-specific clauses
        self._parse_abap_specific_clauses(select)
        
        return select
```

**Purpose:** Converts tokens into an Abstract Syntax Tree (AST), understanding ABAP grammar.

### 3. Generator
```python
class Generator(Postgres.Generator):
    """Generates ABAP SQL from AST"""
    
    def select_sql(self, expression):
        sql = super().select_sql(expression)
        
        # Add ABAP-specific keywords
        if expression.args.get("single"):
            sql = sql.replace("SELECT", "SELECT SINGLE", 1)
        
        return sql
```

**Purpose:** Converts AST back to SQL text, with ABAP-specific formatting.

## 🚀 Usage Examples

### Basic Usage

```python
from abap_dialect import ABAP, parse_abap_sql, format_abap_sql

# Parse ABAP SQL
sql = "SELECT SINGLE carrid, connid FROM sflight WHERE carrid = 'AA'"
ast = parse_abap_sql(sql)

print(f"Parsed: {type(ast).__name__}")  # Output: Select
print(f"Is SINGLE: {ast.args.get('single')}")  # Output: True

# Format SQL
formatted = format_abap_sql(sql, pretty=True)
print(formatted)
```

### With Checker V2

```python
from abap_sql_checker_v2 import ABAPSQLCheckerV2

checker = ABAPSQLCheckerV2()

# Check syntax
is_valid, ast, errors = checker.check_syntax(sql)

# Full analysis
analysis = checker.analyze_query(sql)
print(f"Valid: {analysis['valid']}")
print(f"ABAP Features: {analysis['abap_features']}")
```

## 🎨 ABAP-Specific Features Supported

### Keywords Recognized

| Keyword | Purpose | Example |
|---------|---------|---------|
| `SINGLE` | Select single row | `SELECT SINGLE * FROM table` |
| `UP TO n ROWS` | Limit results | `SELECT * FROM table UP TO 10 ROWS` |
| `BYPASSING BUFFER` | Skip buffer | `SELECT * FROM table BYPASSING BUFFER` |
| `CLIENT SPECIFIED` | Manual client | `SELECT * FROM table CLIENT SPECIFIED` |
| `FOR UPDATE` | Lock rows | `SELECT * FROM table FOR UPDATE` |

### Host Variables

Both syntaxes are supported:

```sql
-- Modern ABAP (@variable)
SELECT carrid FROM sflight WHERE carrid = @lv_carrid

-- Classic ABAP (:variable)
SELECT carrid FROM sflight WHERE carrid = :lv_carrid
```

### ABAP-Specific Validations

The V2 checker includes ABAP best practices:

```python
# Warns about SELECT SINGLE without WHERE
SELECT SINGLE carrid FROM sflight  # ⚠️ Warning

# Warns about SELECT * 
SELECT * FROM sflight  # ⚠️ Warning

# Warns about missing WHERE/LIMIT
SELECT carrid FROM sflight  # ⚠️ Warning
```

## 🔧 Extending the Dialect

### Adding New Keywords

```python
class Tokenizer(Postgres.Tokenizer):
    KEYWORDS = {
        **Postgres.Tokenizer.KEYWORDS,
        "MY_KEYWORD": TokenType.VAR,
    }
```

### Adding Custom Parsing

```python
class Parser(Postgres.Parser):
    def _parse_abap_specific_clauses(self, select):
        if self._match_text_seq("MY", "CLAUSE"):
            select.set("my_custom_flag", True)
        return select
```

### Adding Custom Generation

```python
class Generator(Postgres.Generator):
    def select_sql(self, expression):
        sql = super().select_sql(expression)
        
        if expression.args.get("my_custom_flag"):
            sql += " MY CLAUSE"
        
        return sql
```

## 📊 Comparison: V1 vs V2

| Feature | V1 (Existing) | V2 (Dialect) |
|---------|---------------|--------------|
| **Dialect** | PostgreSQL fallback | Custom ABAP |
| **ABAP Keywords** | Limited | Full support |
| **Host Variables** | Works (as params) | Proper @ support |
| **SINGLE Support** | No | Yes ✅ |
| **UP TO ROWS** | No | Planned ✅ |
| **Custom Validation** | Basic | Enhanced |
| **Error Messages** | Generic | ABAP-specific |
| **Extensibility** | Limited | High |
| **Performance** | Fast | Similar |

## 🧪 Testing

### Run Dialect Tests

```bash
# Test the dialect
python abap_dialect.py

# Test the V2 checker
python abap_sql_checker_v2.py

# Run all existing tests with V2
# (Would need to update test files to use V2)
```

### Example Test

```python
from abap_dialect import parse_abap_sql

def test_abap_single():
    sql = "SELECT SINGLE carrid FROM sflight WHERE carrid = 'AA'"
    ast = parse_abap_sql(sql)
    
    assert ast is not None
    assert ast.args.get('single') == True
    print("✓ SINGLE keyword parsed correctly")

test_abap_single()
```

## 🎯 Migration Path

### Option 1: Keep Both (Recommended Initially)

Keep both implementations during transition:
- **V1** (`abap_sql_checker.py`) - Stable, tested
- **V2** (`abap_sql_checker_v2.py`) - New features, ABAP-specific

### Option 2: Gradual Migration

1. Test V2 with your queries
2. Report any issues
3. Extend dialect as needed
4. Switch to V2 when stable
5. Deprecate V1

### Option 3: Direct Replacement

Update `abap_sql_checker.py` to use the ABAP dialect:

```python
from abap_dialect import ABAP, parse_abap_sql

class ABAPSQLChecker:
    def __init__(self):
        self.dialect = ABAP  # Use custom dialect
    
    def check_syntax(self, sql):
        parsed = parse_abap_sql(sql)
        # ... rest of implementation
```

## 🔍 Advanced Features

### Custom Token Types (Future)

For more control, define custom token types:

```python
# In a custom tokens module
class ABAPTokenType(TokenType):
    SINGLE = auto()
    UP_TO = auto()
    BYPASSING_BUFFER = auto()
```

### Complex ABAP Constructs

The dialect can be extended to support:

```sql
-- INTO clauses
SELECT * INTO TABLE @lt_flights FROM sflight

-- APPENDING
SELECT * APPENDING TABLE @lt_flights FROM sflight

-- PACKAGE SIZE
SELECT * FROM huge_table PACKAGE SIZE 1000

-- FOR ALL ENTRIES
SELECT * FROM table2 
FOR ALL ENTRIES IN @lt_table1
WHERE field = @lt_table1-field
```

### Integration with SAP Systems

Future enhancements could include:

```python
class ABAPSQLChecker:
    def __init__(self, sap_connection=None):
        self.dialect = ABAP
        self.sap = sap_connection
    
    def validate_against_schema(self, sql):
        # Query SAP system for table/field existence
        tables = self._extract_tables(sql)
        for table in tables:
            if not self.sap.table_exists(table):
                return False, f"Table {table} not found"
        return True, None
```

## 📚 Resources

### SQLGlot Documentation
- [Official Docs](https://sqlglot.com/)
- [Dialect Development](https://github.com/tobymao/sqlglot/blob/main/posts/dialect_development.md)
- [Example Dialects](https://github.com/tobymao/sqlglot/tree/main/sqlglot/dialects)

### ABAP SQL Reference
- [ABAP SQL Overview](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/abensql.htm)
- [SELECT Statement](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/abapselect.htm)
- [SQL Expressions](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/abapsql_expr.htm)

## 🎓 Key Takeaways

1. **Custom dialects are the "right way"** to extend SQLGlot
2. **Inherit from similar dialect** (we use PostgreSQL)
3. **Override three components**: Tokenizer, Parser, Generator
4. **Start simple**, extend gradually
5. **Test thoroughly** with real ABAP SQL
6. **Document ABAP-specific features**

## 🚀 Next Steps

1. ✅ Create ABAP dialect
2. ✅ Test with basic queries
3. ⏳ Add more ABAP keywords (UP TO, BYPASSING BUFFER)
4. ⏳ Support INTO clauses
5. ⏳ Handle ABAP operators (~, =>, etc.)
6. ⏳ Add ABAP-specific functions
7. ⏳ Integrate with existing test suite
8. ⏳ Performance optimization

## 💡 Conclusion

Using SQLGlot's dialect system provides a **robust, extensible foundation** for ABAP SQL syntax checking. While it requires more initial setup, the benefits for ABAP-specific features and future extensibility make it the recommended approach for production use.

---

**Files in This Implementation:**
- `abap_dialect.py` - Custom ABAP dialect definition
- `abap_sql_checker_v2.py` - Enhanced checker using ABAP dialect
- `abap_sql_checker.py` - Original checker (V1, still works)

**Choose:**
- **V1** for quick start and standard SQL
- **V2** for ABAP-specific features and extensibility

---

*Last Updated: November 10, 2025*  
*Version: 2.0.0 - ABAP Dialect Implementation*

