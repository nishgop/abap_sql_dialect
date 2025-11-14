# Real Ariba AQL Syntax Analysis

## Problem: Production AQL Queries Failing to Parse

Your real-world Ariba AQL queries contain advanced Ariba-specific syntax that goes significantly beyond standard SQL. These features require deep parser modifications.

## Example Query That Fails
```sql
SELECT cr FROM ariba.sourcing.rfx.RFXDocument AS cr INCLUDE INACTIVE 
WHERE cr IN (BaseId(:PARAM), BaseId(:PARAM))
```

## Ariba-Specific Features Not Currently Supported

### 1. **INCLUDE INACTIVE** Clause ❌
- **Syntax**: `FROM table AS alias INCLUDE INACTIVE`
- **Issue**: This is a non-standard clause that appears after the table alias
- **Standard SQL**: No equivalent
- **Challenge**: SQLGlot's parser expects standard FROM...WHERE...ORDER BY structure

### 2. **SUBCLASS NONE** Clause ❌
- **Syntax**: `FROM table AS alias SUBCLASS NONE`
- **Example**: `FROM ariba.sourcing.rfx.RFXBid AS RFXBid SUBCLASS NONE`
- **Challenge**: Another Ariba-specific modifier after table name

### 3. **Multi-Level Schema/Table Names** ⚠️
- **Syntax**: `ariba.sourcing.rfx.RFXDocument`
- **Standard SQL**: Usually `schema.table` (2 levels max)
- **Ariba**: Can have 3-4 levels with quoted parts: `ariba."user".core."Group"`
- **Status**: Postgres dialect can handle this with proper quoting

### 4. **Colon Parameters** ❌
- **Syntax**: `:PARAM`, `:NUM`, `:BOOLEAN`, `:NULL`
- **Standard SQL**: `?` or `$1`, `$2` (positional)
- **Status**: Could work if treated as named parameters

### 5. **Complex Nested Field Access** ⚠️
- **Syntax**: `RFXDocument.ParentWorkspace.ProjectAddin.WorkspaceType`
- **Challenge**: Multiple levels of dot notation
- **Status**: Postgres handles dot notation but may need testing for deep nesting

## What Would Be Required for Full Support

### Option 1: Parser Extension (Complex)
Would require:
1. Override `_parse_from` to handle `INCLUDE INACTIVE` and `SUBCLASS NONE`
2. Create custom AST nodes for these Ariba clauses
3. Modify generator to output these clauses correctly
4. Extensive testing with real Ariba queries
5. **Estimated effort**: 40-80 hours

### Option 2: Pre-processing (Simpler)
Strip or transform Ariba-specific syntax before parsing:
```python
def preprocess_aql(sql):
    # Remove INCLUDE INACTIVE
    sql = sql.replace(' INCLUDE INACTIVE', '')
    # Remove SUBCLASS NONE
    sql = sql.replace(' SUBCLASS NONE', '')
    # Convert :PARAM to $1, :NUM to $2, etc.
    # ... more transformations
    return sql
```

### Option 3: Validation-Only Approach (Recommended)
Instead of full parsing, validate key aspects:
- Check for required clauses (SELECT, FROM, WHERE)
- Validate parentheses matching
- Check for Ariba function names (BaseId, etc.)
- Validate parameter syntax
- **Does not** build full AST
- **Does** provide syntax validation
- **Estimated effort**: 8-16 hours

## Current Implementation Status

### ✅ What Works
- Standard SQL SELECT/INSERT/UPDATE/DELETE
- Standard JOINs, subqueries, aggregates
- Simple table names (single level)
- Standard SQL functions
- Dot notation for simple field access (table.field)

### ❌ What Doesn't Work (Real Ariba AQL)
- `INCLUDE INACTIVE` clause
- `SUBCLASS NONE` clause
- Multi-level schema names (3-4 levels)
- `:PARAM` style parameters
- `BaseId(:PARAM)` in WHERE IN clauses
- Complex nested field paths

## Recommendations

### Immediate Options

**1. Use Simplified AQL Subset**
If you can reformulate queries without Ariba-specific syntax:
```sql
-- Instead of:
SELECT cr FROM ariba.sourcing.rfx.RFXDocument AS cr INCLUDE INACTIVE

-- Use:
SELECT cr FROM rfxdocument AS cr
WHERE status = 'inactive' OR status = 'active'
```

**2. Pre-processing Wrapper**
Create a wrapper that strips Ariba-specific syntax:
```python
def validate_ariba_aql(sql):
    # Strip Ariba-specific clauses
    clean_sql = sql
    clean_sql = clean_sql.replace(' INCLUDE INACTIVE', '')
    clean_sql = clean_sql.replace(' SUBCLASS NONE', '')
    
    # Validate with standard parser
    checker = AQLSQLChecker()
    return checker.check_syntax(clean_sql)
```

**3. Regular Expression Validation**
For production Ariba AQL, use regex patterns to validate:
- Required keywords present (SELECT, FROM, WHERE)
- Balanced parentheses
- Valid Ariba object names
- Proper parameter syntax
- **Pro**: Fast, handles Ariba syntax
- **Con**: No full AST, limited semantic checking

## Test Results with Real Queries

| Query Feature | Parsing Status | Notes |
|---------------|----------------|-------|
| Simple SELECT | ✅ Works | Standard SQL |
| FROM table AS alias | ✅ Works | Standard SQL |
| BaseId() function | ✅ Works | Added to dialect |
| INCLUDE INACTIVE | ❌ Fails | Non-standard clause |
| SUBCLASS NONE | ❌ Fails | Non-standard clause |
| Multi-level table names | ⚠️ Partial | May work with proper quoting |
| :PARAM parameters | ⚠️ Untested | May parse as identifiers |
| Complex nested paths | ⚠️ Partial | May work depending on depth |

## Conclusion

The current implementation handles **standard SQL with Ariba functions**, but does not support **Ariba-proprietary syntax extensions** like `INCLUDE INACTIVE` and `SUBCLASS NONE`.

For full production Ariba AQL support, you would need either:
1. A complete custom parser (40-80 hours of work)
2. Pre-processing to strip Ariba-specific syntax
3. A validation-only approach using regex patterns

**Recommendation**: If you need to validate production Ariba queries, I suggest creating a pre-processing function that strips/transforms Ariba-specific syntax before passing to the checker, or use a regex-based validation approach that checks for syntax patterns without full parsing.

Would you like me to implement one of these alternative approaches?

