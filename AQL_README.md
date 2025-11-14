# AQL (Ariba Query Language) SQL Dialect for SQLGlot

A comprehensive **Ariba Query Language (AQL) SQL Dialect** implementation using SQLGlot, featuring advanced syntax validation, semantic checking, and query analysis for SAP Ariba reporting and analytics.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![SQLGlot](https://img.shields.io/badge/SQLGlot-Custom%20Dialect-green.svg)](https://sqlglot.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Features

### ✅ Core AQL SQL Support
- **SELECT** statements with WHERE, ORDER BY, GROUP BY, HAVING, LIMIT
- **INSERT, UPDATE, DELETE** statements
- **JOINs** (INNER, LEFT, RIGHT, CROSS)
- **Subqueries** and nested queries
- **UNION** and UNION ALL operations
- **DISTINCT** and TOP N queries

### ✅ Production Ariba AQL Support **NEW!** 🎉
- **Pre-processing** for Ariba-proprietary syntax
- **INCLUDE INACTIVE** clause handling
- **SUBCLASS NONE** clause handling
- **Multi-level table names** (e.g., `ariba.sourcing.rfx.RFXDocument`)
- **BaseId(:PARAM)** function support
- **Nested field access** (e.g., `Document.ParentWorkspace.ProjectAddin`)
- **Parameter syntax** (`:PARAM`, `:NUM`, `:BOOLEAN`, `:NULL`)
- All production Ariba queries validated successfully

### ✅ AQL-Specific Features
- 📦 **Ariba Object References** - Document, Project, Supplier, Invoice, Contract, Requisition, Order
- 🔗 **Dot Notation** - Document.DocumentId, Project.ProjectName, etc.
- 📅 **Date/Time Functions** - FORMATDATE, FORMATTIMESTAMP, ADDDAYS, ADDMONTHS, DATEDIFF, GETDATE
- 📝 **String Functions** - STRINGCONCAT, SUBSTRING, CHARINDEX, LEN, REPLACE, TRIM
- 🔢 **Math Functions** - ROUND, CEILING, FLOOR, ABS, POWER, SQRT
- 🔀 **Conditional Functions** - IIF, ISNULL, NULLIF, CASE expressions
- 📊 **Aggregate Functions** - COUNT, SUM, AVG, MIN, MAX with GROUP BY/HAVING

### ✅ Validation & Analysis
- 🔍 **Syntax Validation** - Comprehensive error detection
- 🧠 **Semantic Validation** - Missing clauses, invalid JOINs, incomplete statements
- 📊 **Query Analysis** - Extract tables, columns, functions, clauses
- 💅 **SQL Formatting** - Pretty-print and normalize AQL queries

---

## 📦 Installation

### Prerequisites
```bash
Python 3.8 or higher
pip package manager
```

### Install Dependencies
```bash
pip install sqlglot
```

### Clone Repository
```bash
git clone https://github.com/nishgop/abap_sql_dialect.git
cd abap_sql_dialect
```

---

## 🚀 Quick Start

### Basic Usage

```python
from aql_sql_checker import AQLSQLChecker

# Initialize checker
checker = AQLSQLChecker()

# Check standard AQL
sql = "SELECT Document.DocumentId, Document.Title FROM Document WHERE Document.Status = 'Active'"
is_valid, ast, errors = checker.check_syntax(sql)

# Check production Ariba AQL (with pre-processing enabled by default)
ariba_sql = """
SELECT cr FROM ariba.sourcing.rfx.RFXDocument AS cr INCLUDE INACTIVE 
WHERE cr IN (BaseId(:PARAM), BaseId(:PARAM))
"""
is_valid, ast, errors = checker.check_syntax(ariba_sql)  # Pre-processing enabled by default

if is_valid:
    print("✅ Valid AQL!")
else:
    print("❌ Errors found:")
    for error in errors:
        print(f"  - {error}")
```

### Production Ariba AQL

The checker now handles **real production Ariba queries** with proprietary syntax:

```python
# This query has INCLUDE INACTIVE and BaseId() - both work now!
real_ariba_query = """
SELECT RFXBid FROM ariba.sourcing.rfx.RFXBid AS RFXBid SUBCLASS NONE 
WHERE RFXBid.ContentDocumentReference.DocumentId = BaseId(:PARAM) 
AND RFXBid.ContentDocumentReference.DocumentVersion = :NUM
ORDER BY RFXBid.SubmissionDate DESC
"""

is_valid, ast, errors = checker.check_syntax(real_ariba_query)
print(f"Valid: {is_valid}")  # ✅ True!
```

### Disable Pre-processing (Optional)

If you want to check strict SQL without Ariba extensions:

```python
is_valid, ast, errors = checker.check_syntax(sql, preprocess=False)
```

# Analyze query
analysis = checker.analyze_query(sql)
print(f"Tables: {analysis['tables']}")
print(f"Columns: {analysis['columns']}")
print(f"Clauses: {analysis['clauses']}")

# Format SQL
formatted = checker.format_sql(sql, pretty=True)
print(formatted)
```

### Interactive Mode

```bash
python interactive_aql_checker.py
```

Provides an interactive CLI for checking AQL queries:
- Check syntax interactively
- Format SQL statements
- Load and validate SQL from files
- Run example queries

---

## 📚 Example Queries

### Production Ariba AQL **NEW!** 🎉

Real production queries that now work with pre-processing:

```sql
-- INCLUDE INACTIVE clause
SELECT cr FROM ariba.sourcing.rfx.RFXDocument AS cr INCLUDE INACTIVE 
WHERE cr IN (BaseId(:PARAM), BaseId(:PARAM));

-- SUBCLASS NONE clause
SELECT RFXBid FROM ariba.sourcing.rfx.RFXBid AS RFXBid SUBCLASS NONE 
WHERE RFXBid.ContentDocumentReference.DocumentId = BaseId(:PARAM);

-- Multi-level table names with quoted identifiers
SELECT g FROM ariba."user".core."Group" AS g 
WHERE g.Users = BaseId(:PARAM) AND g.IsGlobal = :BOOLEAN;

-- Complex nested field access
SELECT RFXDocument.ParentWorkspace.ProjectAddin.WorkspaceType 
FROM ariba.sourcing.rfx.RFXDocument AS RFXDocument;

-- Parameter syntax (:PARAM, :NUM, :BOOLEAN, :NULL)
SELECT * FROM Document WHERE Status = :PARAM AND Version = :NUM;
```

### Basic SELECT
```sql
SELECT Document.DocumentId, Document.Title, Document.Amount
FROM Document
WHERE Document.Status = 'Active'
ORDER BY Document.Amount DESC;
```

### JOIN with Aggregates
```sql
SELECT 
    s.Name,
    COUNT(i.InvoiceId) as InvoiceCount,
    SUM(i.Amount) as TotalAmount
FROM Supplier s
LEFT JOIN Invoice i ON s.SupplierId = i.SupplierId
GROUP BY s.Name
HAVING SUM(i.Amount) > 10000;
```

### Date Functions
```sql
SELECT 
    Document.DocumentId,
    FORMATDATE(Document.CreatedDate, 'yyyy-MM-dd') as FormattedDate,
    ADDDAYS(Document.CreatedDate, 30) as DueDate,
    DATEDIFF('day', Document.CreatedDate, GETDATE()) as DaysOld
FROM Document;
```

### String Functions
```sql
SELECT 
    STRINGCONCAT(Supplier.FirstName, ' ', Supplier.LastName) as FullName,
    SUBSTRING(Supplier.Name, 1, 50) as ShortName,
    LEN(Supplier.Description) as DescLength
FROM Supplier;
```

### Complex Query with CASE
```sql
SELECT 
    Project.ProjectName,
    COUNT(DISTINCT Document.DocumentId) as DocCount,
    SUM(CASE 
        WHEN Document.Status = 'Completed' THEN Document.Amount 
        ELSE 0 
    END) as CompletedAmount,
    AVG(Document.Amount) as AvgAmount
FROM Project
INNER JOIN Document ON Project.ProjectId = Document.ProjectId
WHERE Project.Status = 'Active'
GROUP BY Project.ProjectName
HAVING COUNT(*) > 5
ORDER BY CompletedAmount DESC;
```

More examples in `example_queries_aql.sql` (400+ lines covering all features)

---

## 🧪 Testing

### Run All Tests
```bash
# Run AQL tests only
python -m unittest discover -s . -p "test_aql_*.py" -v

# Run unified tests (both ABAP and AQL)
python run_unified_tests.py
```

### Test Coverage

| Test Suite | Tests | Coverage |
|------------|-------|----------|
| **AQL Basic** | 14 tests | SELECT, INSERT, UPDATE, DELETE, ORDER BY, analysis |
| **AQL Extended** | 55 tests | JOINs, aggregates, date/time, strings, math, conditionals, subqueries |
| **AQL Specific** | 20 tests | Object references, dot notation, complex queries, batch processing |
| **AQL Negative** | 21 tests | Error detection, invalid syntax, missing clauses |
| **Total** | **110 tests** | Comprehensive AQL validation |

### Test Example
```bash
python -m unittest test_aql_basic.TestBasicAQLSyntax -v
python -m unittest test_aql_extended.TestAQLJoins -v
python -m unittest test_aql_negative -v
```

---

## 📖 API Reference

### AQLSQLChecker

Main class for AQL SQL syntax checking and validation.

#### Methods

##### `check_syntax(sql: str) -> Tuple[bool, Optional[exp.Expression], List[str]]`
Check SQL syntax and return validation results.

**Parameters:**
- `sql` (str): AQL SQL statement to check

**Returns:**
- `is_valid` (bool): Whether the SQL is valid
- `ast` (Expression): Parsed abstract syntax tree (or None if invalid)
- `errors` (List[str]): List of error messages

**Example:**
```python
checker = AQLSQLChecker()
is_valid, ast, errors = checker.check_syntax("SELECT * FROM Document")
if not is_valid:
    print(f"Errors: {errors}")
```

##### `analyze_query(sql: str) -> Dict`
Analyze a query and extract detailed information.

**Returns dict with:**
- `sql`: Original SQL statement
- `is_valid`: Validation status
- `errors`: List of errors
- `warnings`: List of warnings
- `tables`: List of referenced tables
- `columns`: List of referenced columns
- `functions`: List of used functions
- `clauses`: List of SQL clauses (FROM, WHERE, JOIN, etc.)
- `statement_type`: Type of statement (Select, Insert, etc.)
- `ast`: Parsed AST

##### `format_sql(sql: str, pretty: bool = True) -> Optional[str]`
Format an AQL SQL statement.

**Parameters:**
- `sql` (str): SQL to format
- `pretty` (bool): Use pretty printing (default: True)

**Returns:**
- Formatted SQL string or None if formatting fails

##### `batch_check(sql_statements: List[str]) -> List[Dict]`
Check multiple SQL statements in batch.

**Parameters:**
- `sql_statements` (List[str]): List of SQL statements

**Returns:**
- List of analysis dictionaries

---

## 🏗️ Architecture

### Dialect Structure
```
aql_dialect.py
├── AQL (Dialect)
│   ├── Tokenizer - AQL keywords and operators
│   ├── Parser - AQL-specific grammar rules
│   └── Generator - AQL SQL generation
```

### Checker Structure
```
aql_sql_checker.py
├── AQLSQLChecker
│   ├── check_syntax() - Main validation
│   ├── _pre_validate_syntax() - Lexical checks
│   ├── _validate_aql_specific_rules() - Semantic validation
│   ├── analyze_query() - Query analysis
│   └── format_sql() - SQL formatting
```

---

## 🎯 Supported AQL Objects

| Object Type | Example Fields |
|-------------|----------------|
| **Document** | DocumentId, Title, Status, Amount, CreatedDate, Description |
| **Project** | ProjectId, ProjectName, ProjectOwner, StartDate, EndDate, Status |
| **Supplier** | SupplierId, Name, Region, Status, RegistrationDate |
| **Invoice** | InvoiceId, InvoiceNumber, Amount, InvoiceDate, DueDate, Status |
| **Contract** | ContractId, ContractNumber, ContractAmount, StartDate, EndDate, Status |
| **Requisition** | RequisitionId, RequisitionNumber, TotalAmount, CreatedDate, Status |
| **Order** | OrderId, OrderNumber, OrderAmount, OrderDate, DeliveryDate, Status |

---

## ⚠️ Known Limitations

1. **Window Functions**: Limited window function support (basic ROW_NUMBER, RANK supported)
2. **CTEs**: Common Table Expressions (WITH clause) not fully tested
3. **Schema Validation**: No runtime schema/table validation (syntax only)
4. **Format Strings**: Date format strings validated at runtime, not parse-time
5. **Advanced Features**: Some advanced AQL features may require extension

---

## 🔧 Configuration

### Custom Validation Rules

Extend `AQLSQLChecker` to add custom validation:

```python
class CustomAQLChecker(AQLSQLChecker):
    def _validate_aql_specific_rules(self, ast, errors):
        super()._validate_aql_specific_rules(ast, errors)
        
        # Add custom validation
        if isinstance(ast, exp.Select):
            # Your custom logic here
            pass
```

---

## 📝 Example Use Cases

1. **AQL Query Validation**: Validate user-generated AQL queries before execution
2. **Migration Tools**: Convert and validate AQL queries during system migrations
3. **Query Analysis**: Analyze AQL queries for optimization and dependencies
4. **IDE Integration**: Provide real-time syntax checking in development tools
5. **Automated Testing**: Validate AQL query libraries in CI/CD pipelines

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- Built with [SQLGlot](https://sqlglot.com/) - Amazing SQL parser and transpiler
- SAP Ariba for the AQL specification
- Python community for excellent tooling

---

## 📧 Contact

For questions, issues, or feature requests, please open an issue on GitHub.

---

**Made with ❤️ for the SAP Ariba community**

