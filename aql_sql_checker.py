"""
Ariba Query Language (AQL) SQL Syntax Checker

This module provides syntax checking and semantic validation for AQL SQL statements.
It uses the custom AQL dialect to parse and validate queries, detecting both
syntax errors and logical issues.

Features:
- Syntax validation using AQL dialect
- Semantic validation (missing clauses, invalid constructs)
- Query analysis (tables, columns, clauses, functions)
- SQL formatting and pretty-printing

Author: Generated with Claude
License: MIT
"""

import re
from typing import List, Dict, Optional, Tuple
from sqlglot import exp, parse_one, ParseError
from aql_dialect import AQL, parse_aql


def preprocess_ariba_aql(sql: str) -> str:
    """
    Pre-process Ariba AQL to remove proprietary syntax that SQLGlot cannot parse.
    
    This function strips Ariba-specific clauses while preserving the query logic:
    - INCLUDE INACTIVE - Ariba clause for including inactive records
    - SUBCLASS NONE - Ariba inheritance control clause
    - Normalizes whitespace
    
    Args:
        sql: Raw Ariba AQL query string
        
    Returns:
        Cleaned SQL that can be parsed by standard Postgres parser
        
    Example:
        >>> sql = "SELECT cr FROM ariba.rfx.Document AS cr INCLUDE INACTIVE"
        >>> preprocess_ariba_aql(sql)
        "SELECT cr FROM ariba.rfx.Document AS cr"
    """
    # Remove INCLUDE INACTIVE (case-insensitive)
    sql = re.sub(r'\s+INCLUDE\s+INACTIVE\b', '', sql, flags=re.IGNORECASE)
    
    # Remove SUBCLASS NONE (case-insensitive)
    sql = re.sub(r'\s+SUBCLASS\s+NONE\b', '', sql, flags=re.IGNORECASE)
    
    # Remove SUBCLASS <identifier> (case-insensitive)
    sql = re.sub(r'\s+SUBCLASS\s+\w+\b', '', sql, flags=re.IGNORECASE)
    
    # Normalize whitespace
    sql = ' '.join(sql.split())
    
    return sql


def print_analysis(analysis: Dict) -> None:
    """
    Pretty-print analysis results.
    
    Args:
        analysis: Dictionary containing analysis results
    """
    print("\n" + "="*80)
    print("AQL SQL ANALYSIS RESULTS")
    print("="*80)
    
    # SQL statement
    print(f"\nSQL: {analysis['sql']}")
    
    # Validity
    print(f"\nValid: {analysis['is_valid']}")
    
    # Errors
    if analysis['errors']:
        print("\nErrors:")
        for i, error in enumerate(analysis['errors'], 1):
            print(f"  {i}. {error}")
    
    # Warnings
    if analysis['warnings']:
        print("\nWarnings:")
        for i, warning in enumerate(analysis['warnings'], 1):
            print(f"  {i}. {warning}")
    
    # Tables
    if analysis['tables']:
        print(f"\nTables: {', '.join(analysis['tables'])}")
    
    # Columns
    if analysis['columns']:
        print(f"Columns: {', '.join(analysis['columns'])}")
    
    # Functions
    if analysis['functions']:
        print(f"Functions: {', '.join(analysis['functions'])}")
    
    # Clauses
    if analysis['clauses']:
        print(f"Clauses: {', '.join(analysis['clauses'])}")
    
    # Statement type
    if analysis['statement_type']:
        print(f"Statement Type: {analysis['statement_type']}")
    
    print("\n" + "="*80 + "\n")


class AQLSQLChecker:
    """
    AQL SQL Syntax Checker and Validator
    
    This class provides comprehensive syntax checking and semantic validation
    for AQL SQL statements using the custom AQL dialect.
    """
    
    def __init__(self):
        """Initialize the AQL SQL checker."""
        self.dialect = AQL
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
    
    def check_syntax(self, sql: str, preprocess: bool = True) -> Tuple[bool, Optional[exp.Expression], List[str]]:
        """
        Check SQL syntax and validate the query.
        
        Args:
            sql: AQL SQL statement to check
            preprocess: Whether to apply Ariba-specific pre-processing (default: True)
            
        Returns:
            Tuple of (is_valid, ast, errors)
        """
        errors = []
        original_sql = sql
        
        try:
            # Pre-process Ariba-specific syntax if enabled
            if preprocess:
                sql = preprocess_ariba_aql(sql)
            
            # Pre-validation: check for obvious syntax issues
            self._pre_validate_syntax(sql, errors)
            if errors:
                return False, None, errors
            
            # Parse the SQL
            parsed = parse_aql(sql)
            
            if parsed is None:
                errors.append("Failed to parse SQL statement")
                # If preprocessing was enabled and parsing still failed,
                # add a hint about Ariba-specific syntax
                if preprocess and original_sql != sql:
                    errors.append("Note: Ariba-specific clauses were removed during pre-processing")
                return False, None, errors
            
            # Post-parsing semantic validation
            self._validate_aql_specific_rules(parsed, errors)
            
            return len(errors) == 0, parsed, errors
        
        except ParseError as e:
            errors.append(f"Syntax error: {str(e)}")
            return False, None, errors
        
        except Exception as e:
            errors.append(f"Unexpected error: {str(e)}")
            return False, None, errors
    
    def _pre_validate_syntax(self, sql: str, errors: List[str]) -> None:
        """
        Pre-validation checks before parsing.
        Detects common lexical errors that might be silently dropped.
        
        Args:
            sql: SQL statement to validate
            errors: List to append errors to
        """
        # Check for dangling operators in SELECT list
        dangling_op_pattern = r'SELECT\s+[^,]*[+\-*/]\s*(?:,|FROM)'
        if re.search(dangling_op_pattern, sql, re.IGNORECASE):
            errors.append("Dangling arithmetic operator in SELECT list")
        
        # Check for empty SELECT list
        empty_select_pattern = r'SELECT\s+(FROM|WHERE|GROUP|ORDER|LIMIT)'
        if re.search(empty_select_pattern, sql, re.IGNORECASE):
            errors.append("Empty SELECT list")
        
        # Check for consecutive operators
        if re.search(r'[+\-*/]{2,}', sql):
            errors.append("Consecutive arithmetic operators")
        
        # Check for mismatched parentheses
        if sql.count('(') != sql.count(')'):
            errors.append("Mismatched parentheses")
        
        # Check for missing comparison in WHERE clause
        invalid_where_pattern = r'WHERE\s+(?:AND|OR|,)'
        if re.search(invalid_where_pattern, sql, re.IGNORECASE):
            errors.append("Invalid WHERE clause: missing condition before AND/OR")
    
    def _validate_aql_specific_rules(self, ast: exp.Expression, errors: List[str]) -> None:
        """
        Validate AQL-specific semantic rules.
        
        Args:
            ast: Parsed AST to validate
            errors: List to append errors to
        """
        if isinstance(ast, exp.Select):
            # Check for FROM clause
            from_clause = ast.find(exp.From)
            if not from_clause:
                errors.append("Missing FROM clause in SELECT statement")
            
            # Check for JOIN without ON condition
            for join in ast.find_all(exp.Join):
                if join.kind != "CROSS" and not join.args.get("on"):
                    errors.append(f"{join.kind} JOIN requires ON condition")
            
            # Check for window functions without OVER clause
            window_func_types = [
                (exp.RowNumber, "ROW_NUMBER"),
                (exp.Rank, "RANK"),
                (exp.DenseRank, "DENSE_RANK"),
                (exp.PercentRank, "PERCENT_RANK"),
            ]
            
            for func_type, func_name in window_func_types:
                for func in ast.find_all(func_type):
                    if not func.find_ancestor(exp.Window):
                        errors.append(f"Window function {func_name}() requires OVER clause")
            
            # Check for common window functions in Anonymous functions
            for func in ast.find_all(exp.Anonymous):
                func_name_str = str(func.this).upper()
                if func_name_str in ('LAG', 'LEAD', 'FIRST_VALUE', 'LAST_VALUE', 'NTILE'):
                    if not func.find_ancestor(exp.Window):
                        errors.append(f"Window function {func_name_str}() requires OVER clause")
            
            # Check for invalid arithmetic expressions
            for binary_expr in ast.find_all(exp.Binary):
                if binary_expr.left is None or binary_expr.right is None:
                    errors.append("Invalid arithmetic expression: missing operand")
        
        elif isinstance(ast, exp.Insert):
            # INSERT must have VALUES or SELECT
            if not ast.args.get("expression"):
                errors.append("INSERT statement requires VALUES clause or SELECT query")
        
        elif isinstance(ast, exp.Update):
            # UPDATE must have SET clause
            if not ast.args.get("expressions"):
                errors.append("UPDATE statement requires SET clause")
        
        elif isinstance(ast, exp.Delete):
            # DELETE must have target table
            if not ast.args.get("this") and not ast.args.get("from") and not ast.args.get("tables"):
                errors.append("DELETE statement requires target table")
    
    def analyze_query(self, sql: str, preprocess: bool = True) -> Dict:
        """
        Analyze an AQL SQL query and return comprehensive information.
        
        Args:
            sql: AQL SQL statement to analyze
            preprocess: Whether to apply Ariba-specific pre-processing (default: True)
            
        Returns:
            Dictionary with analysis results
        """
        is_valid, ast, errors = self.check_syntax(sql, preprocess=preprocess)
        
        result = {
            'sql': sql,
            'is_valid': is_valid,
            'errors': errors,
            'warnings': [],
            'tables': [],
            'columns': [],
            'functions': [],
            'clauses': [],
            'statement_type': None,
            'ast': ast,
        }
        
        if not ast:
            return result
        
        # Extract statement type
        result['statement_type'] = ast.__class__.__name__
        
        # Extract tables
        for table in ast.find_all(exp.Table):
            table_name = str(table.this)
            if table_name not in result['tables']:
                result['tables'].append(table_name)
        
        # Extract columns
        for column in ast.find_all(exp.Column):
            col_name = str(column.this)
            if col_name and col_name not in result['columns']:
                result['columns'].append(col_name)
        
        # Extract functions
        for func in ast.find_all(exp.Anonymous):
            func_name = str(func.this)
            if func_name and func_name not in result['functions']:
                result['functions'].append(func_name)
        
        # Add standard SQL functions
        for func_type in [exp.Count, exp.Sum, exp.Avg, exp.Min, exp.Max]:
            for func in ast.find_all(func_type):
                func_name = func_type.__name__.upper()
                if func_name not in result['functions']:
                    result['functions'].append(func_name)
        
        # Extract clauses
        if isinstance(ast, exp.Select):
            if ast.args.get('from'):
                result['clauses'].append('FROM')
            if ast.args.get('where'):
                result['clauses'].append('WHERE')
            if ast.args.get('group'):
                result['clauses'].append('GROUP BY')
            if ast.args.get('having'):
                result['clauses'].append('HAVING')
            if ast.args.get('order'):
                result['clauses'].append('ORDER BY')
            if ast.args.get('limit'):
                result['clauses'].append('LIMIT')
            if ast.find(exp.Join):
                result['clauses'].append('JOIN')
        
        return result
    
    def format_sql(self, sql: str, pretty: bool = True) -> Optional[str]:
        """
        Format an AQL SQL statement.
        
        Args:
            sql: SQL statement to format
            pretty: Whether to use pretty printing
            
        Returns:
            Formatted SQL string or None if formatting fails
        """
        try:
            parsed = parse_aql(sql)
            if parsed is None:
                return None
            
            return parsed.sql(dialect='postgres', pretty=pretty)
        except Exception:
            return None
    
    def batch_check(self, sql_statements: List[str]) -> List[Dict]:
        """
        Check multiple SQL statements in batch.
        
        Args:
            sql_statements: List of SQL statements to check
            
        Returns:
            List of analysis results
        """
        results = []
        for sql in sql_statements:
            results.append(self.analyze_query(sql))
        return results


def main():
    """Main function demonstrating AQL SQL Checker usage."""
    checker = AQLSQLChecker()
    
    # Example AQL queries
    examples = [
        # Valid queries
        ("Basic SELECT", 
         "SELECT Document.DocumentId, Document.Title FROM Document WHERE Document.Status = 'Active'"),
        
        ("SELECT with JOIN",
         """SELECT d.DocumentId, p.ProjectName
            FROM Document d
            INNER JOIN Project p ON d.ProjectId = p.ProjectId
            WHERE d.Status = 'Active'"""),
        
        ("SELECT with Aggregate",
         "SELECT Supplier.Name, COUNT(*) as InvoiceCount FROM Invoice GROUP BY Supplier.Name"),
        
        ("SELECT with Date Function",
         "SELECT Document.DocumentId, FORMATDATE(Document.CreatedDate, 'yyyy-MM-dd') as Created FROM Document"),
        
        ("SELECT with CASE",
         """SELECT Document.DocumentId,
            CASE 
                WHEN Document.Amount > 1000 THEN 'High'
                WHEN Document.Amount > 500 THEN 'Medium'
                ELSE 'Low'
            END as AmountCategory
            FROM Document"""),
        
        # Invalid queries
        ("Missing FROM", "SELECT Document.DocumentId WHERE Document.Status = 'Active'"),
        
        ("JOIN without ON", "SELECT * FROM Document d JOIN Project p"),
        
        ("Invalid expression", "SELECT a, + FROM Document"),
    ]
    
    print("\n" + "="*80)
    print("AQL SQL SYNTAX CHECKER - DEMO")
    print("="*80)
    
    for name, sql in examples:
        print(f"\n{'─'*80}")
        print(f"Example: {name}")
        print(f"{'─'*80}")
        analysis = checker.analyze_query(sql)
        print_analysis(analysis)


if __name__ == "__main__":
    main()

