"""
ABAP SQL Syntax Checker - Using Custom ABAP Dialect

This module provides a comprehensive syntax checker for ABAP SQL statements
using a custom ABAP dialect built on SQLGlot.

The ABAP dialect properly supports ABAP-specific keywords and syntax:
- SELECT SINGLE
- Host variables (@var and :var)
- ABAP keywords (BYPASSING BUFFER, CLIENT SPECIFIED, etc.)
- Enhanced ABAP-specific validations
"""

import sys
from typing import List, Dict, Tuple, Optional
from sqlglot import parse_one, exp
from sqlglot.errors import ParseError
from abap_dialect import ABAP, parse_abap_sql, format_abap_sql

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


class ABAPSQLChecker:
    """
    Enhanced ABAP SQL Syntax Checker using custom ABAP dialect.
    """
    
    def __init__(self):
        """Initialize the ABAP SQL Checker with custom dialect."""
        self.dialect = ABAP
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
    
    def check_syntax(self, sql: str) -> Tuple[bool, Optional[exp.Expression], List[str]]:
        """
        Check the syntax of an ABAP SQL statement using ABAP dialect.
        
        Args:
            sql: The SQL statement to check
            
        Returns:
            Tuple of (is_valid, parsed_ast, error_messages)
        """
        errors = []
        
        try:
            # Pre-validation: Check for common syntax errors
            self._pre_validate_syntax(sql, errors)
            
            if errors:
                return False, None, errors
            
            # Parse using ABAP dialect
            parsed = parse_abap_sql(sql)
            
            if parsed is None:
                errors.append("Failed to parse SQL statement")
                return False, None, errors
            
            # Additional ABAP-specific validation
            self._validate_abap_specific_rules(parsed, errors)
            
            return len(errors) == 0, parsed, errors
            
        except ParseError as e:
            errors.append(f"Syntax error: {str(e)}")
            return False, None, errors
        except Exception as e:
            errors.append(f"Unexpected error: {str(e)}")
            return False, None, errors
    
    def _pre_validate_syntax(self, sql: str, errors: List[str]):
        """
        Pre-validation checks for syntax errors that might be silently ignored.
        
        Args:
            sql: The SQL statement
            errors: List to append errors to
        """
        import re
        
        # Normalize SQL: replace multiple spaces with single space
        normalized = re.sub(r'\s+', ' ', sql.strip())
        
        # Check for invalid operators without operands
        # Pattern: SELECT followed by comma and operator before FROM
        if re.search(r'SELECT\s+.*,\s*[+\-*/]\s+FROM', normalized, re.IGNORECASE):
            errors.append("Invalid arithmetic expression: operator without operand")
    
    def _validate_abap_specific_rules(self, ast: exp.Expression, errors: List[str]):
        """
        Validate ABAP-specific SQL rules and semantic correctness.
        
        Args:
            ast: The parsed AST
            errors: List to append errors to
        """
        # Semantic validation for SELECT statements
        if isinstance(ast, exp.Select):
            # Check 1: SELECT must have a FROM clause
            from_clause = ast.find(exp.From)
            if not from_clause:
                errors.append("Missing FROM clause in SELECT statement")
            
            # Check 2: JOINs must have ON conditions (except CROSS JOIN)
            for join in ast.find_all(exp.Join):
                # CROSS JOIN doesn't require ON condition
                if join.kind != "CROSS" and not join.args.get("on"):
                    errors.append(f"{join.kind} JOIN requires ON condition")
            
            # Check 3: Window functions must have OVER clause
            # Check for specific window function types
            window_func_types = [
                (exp.RowNumber, "ROW_NUMBER"),
                (exp.Rank, "RANK"),
                (exp.DenseRank, "DENSE_RANK"),
                (exp.PercentRank, "PERCENT_RANK"),
            ]
            
            for func_type, func_name in window_func_types:
                for func in ast.find_all(func_type):
                    # Window functions must be wrapped in a Window expression
                    if not func.find_ancestor(exp.Window):
                        errors.append(f"Window function {func_name}() requires OVER clause")
            
            # Also check Anonymous functions that might be window functions
            for func in ast.find_all(exp.Anonymous):
                func_name_str = str(func.this).upper()
                if func_name_str in ('LAG', 'LEAD', 'FIRST_VALUE', 'LAST_VALUE', 'NTILE'):
                    if not func.find_ancestor(exp.Window):
                        errors.append(f"Window function {func_name_str}() requires OVER clause")
            
            # Check 4: Validate arithmetic expressions
            for binary_expr in ast.find_all(exp.Binary):
                if binary_expr.left is None or binary_expr.right is None:
                    errors.append("Invalid arithmetic expression: missing operand")
            
            # Check for SELECT * usage (warning only)
            if ast.find(exp.Star):
                self.warnings.append({
                    "type": "PERFORMANCE",
                    "message": "Using SELECT * is discouraged in ABAP SQL. Specify explicit columns."
                })
            
            # Check for SINGLE without proper WHERE clause (warning only)
            if ast.args.get("single"):
                where = ast.find(exp.Where)
                if not where:
                    self.warnings.append({
                        "type": "ABAP_BEST_PRACTICE",
                        "message": "SELECT SINGLE should have a WHERE clause with key fields."
                    })
            
            # Check for missing WHERE clause on large operations (warning only)
            if not ast.find(exp.Where) and not ast.find(exp.Limit):
                up_to_rows = ast.args.get("up_to_rows")
                if not up_to_rows:
                    self.warnings.append({
                        "type": "PERFORMANCE",
                        "message": "Consider adding WHERE clause or LIMIT to restrict result set."
                    })
        
        # Semantic validation for INSERT statements
        elif isinstance(ast, exp.Insert):
            # Check 5: INSERT must have VALUES or SELECT
            if not ast.args.get("expression"):
                errors.append("INSERT statement requires VALUES clause or SELECT query")
        
        # Semantic validation for UPDATE statements
        elif isinstance(ast, exp.Update):
            # UPDATE must have SET clause
            if not ast.args.get("expressions"):
                errors.append("UPDATE statement requires SET clause")
        
        # Semantic validation for DELETE statements
        elif isinstance(ast, exp.Delete):
            # DELETE must have a target table (in 'this', 'from', or 'tables' argument)
            if not ast.args.get("this") and not ast.args.get("from") and not ast.args.get("tables"):
                errors.append("DELETE statement requires target table")
    
    def analyze_query(self, sql: str) -> Dict:
        """
        Perform detailed analysis of an ABAP SQL query.
        
        Args:
            sql: The SQL statement to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        is_valid, ast, errors = self.check_syntax(sql)
        
        analysis = {
            "valid": is_valid,
            "errors": errors,
            "warnings": [w["message"] for w in self.warnings],
            "sql": sql.strip(),
            "dialect": "ABAP",
        }
        
        if ast:
            analysis.update({
                "query_type": ast.__class__.__name__,
                "tables": self._extract_tables(ast),
                "columns": self._extract_columns(ast),
                "has_where_clause": bool(ast.find(exp.Where)),
                "has_join": bool(ast.find(exp.Join)),
                "has_group_by": bool(ast.find(exp.Group)),
                "has_order_by": bool(ast.find(exp.Order)),
            })
            
            # ABAP-specific features
            if isinstance(ast, exp.Select):
                analysis["abap_features"] = {
                    "is_single": ast.args.get("single", False),
                    "up_to_rows": ast.args.get("up_to_rows"),
                    "bypassing_buffer": ast.args.get("bypassing_buffer", False),
                    "client_specified": ast.args.get("client_specified", False),
                }
        
        self.warnings.clear()
        return analysis
    
    def _extract_tables(self, ast: exp.Expression) -> List[str]:
        """Extract table names from the AST."""
        tables = []
        for table in ast.find_all(exp.Table):
            tables.append(table.name)
        return tables
    
    def _extract_columns(self, ast: exp.Expression) -> List[str]:
        """Extract column names from the AST."""
        columns = []
        if isinstance(ast, exp.Select):
            for col in ast.expressions:
                if isinstance(col, exp.Column):
                    columns.append(col.name)
                elif isinstance(col, exp.Alias):
                    columns.append(col.alias)
        return columns
    
    def format_sql(self, sql: str, pretty: bool = True) -> Optional[str]:
        """
        Format an ABAP SQL statement using ABAP dialect.
        
        Args:
            sql: The SQL statement to format
            pretty: Whether to use pretty printing
            
        Returns:
            Formatted SQL string or None if parsing fails
        """
        try:
            return format_abap_sql(sql, pretty=pretty)
        except Exception:
            return None


def print_colored(text: str, color: str = ""):
    """Print colored text if colorama is available."""
    if COLORAMA_AVAILABLE and color:
        print(f"{color}{text}{Style.RESET_ALL}")
    else:
        print(text)


def print_analysis(analysis: Dict):
    """Print a formatted analysis report."""
    print("\n" + "=" * 70)
    print_colored("ABAP SQL SYNTAX CHECK REPORT", 
                  Fore.CYAN if COLORAMA_AVAILABLE else "")
    print("=" * 70)
    
    print_colored(f"\n✓ Valid Syntax: {analysis['valid']}", 
                  (Fore.GREEN if analysis['valid'] else Fore.RED) if COLORAMA_AVAILABLE else "")
    
    print(f"\nSQL Statement:\n{analysis['sql']}")
    
    if analysis['errors']:
        print_colored("\n❌ ERRORS:", Fore.RED if COLORAMA_AVAILABLE else "")
        for error in analysis['errors']:
            print(f"  • {error}")
    
    if analysis['warnings']:
        print_colored("\n⚠ WARNINGS:", Fore.YELLOW if COLORAMA_AVAILABLE else "")
        for warning in analysis['warnings']:
            print(f"  • {warning}")
    
    if analysis['valid']:
        print_colored("\n📊 QUERY ANALYSIS:", Fore.CYAN if COLORAMA_AVAILABLE else "")
        print(f"  Dialect: {analysis.get('dialect', 'N/A')}")
        print(f"  Query Type: {analysis.get('query_type', 'N/A')}")
        print(f"  Tables: {', '.join(analysis.get('tables', [])) or 'None'}")
        print(f"  Columns: {', '.join(analysis.get('columns', [])) or 'All (*)'}")
        print(f"  Has WHERE clause: {analysis.get('has_where_clause', False)}")
        print(f"  Has JOIN: {analysis.get('has_join', False)}")
        print(f"  Has GROUP BY: {analysis.get('has_group_by', False)}")
        print(f"  Has ORDER BY: {analysis.get('has_order_by', False)}")
        
        # Show ABAP-specific features if present
        if 'abap_features' in analysis:
            abap_features = analysis['abap_features']
            if any(abap_features.values()):
                print_colored("\n🎨 ABAP-SPECIFIC FEATURES:", Fore.MAGENTA if COLORAMA_AVAILABLE else "")
                if abap_features['is_single']:
                    print("  • SINGLE keyword detected")
                if abap_features['up_to_rows']:
                    print(f"  • UP TO {abap_features['up_to_rows']} ROWS")
                if abap_features['bypassing_buffer']:
                    print("  • BYPASSING BUFFER enabled")
                if abap_features['client_specified']:
                    print("  • CLIENT SPECIFIED mode")
    
    print("\n" + "=" * 70 + "\n")


def main():
    """Main function to demonstrate the ABAP SQL checker."""
    checker = ABAPSQLChecker()
    
    # Example ABAP SQL queries including ABAP-specific syntax
    test_queries = [
        # Standard SELECT
        "SELECT carrid, connid, fldate FROM sflight WHERE carrid = 'AA'",
        
        # ABAP SINGLE keyword
        "SELECT SINGLE carrid, connid FROM sflight WHERE carrid = 'AA'",
        
        # Modern ABAP host variable syntax
        "SELECT carrid, connid FROM sflight WHERE carrid = @lv_carrid",
        
        # Classic parameter syntax
        "SELECT carrid, connid FROM sflight WHERE carrid = :lv_carrid",
        
        # Complex JOIN
        """SELECT f.carrid, f.connid, f.fldate, p.cityfrom, p.cityto
           FROM sflight AS f
           INNER JOIN spfli AS p ON f.carrid = p.carrid AND f.connid = p.connid
           WHERE f.carrid = 'AA'""",
        
        # SELECT with aggregates
        "SELECT carrid, COUNT(*) as flight_count FROM sflight GROUP BY carrid",
        
        # Window function
        """SELECT carrid, fldate, seatsocc,
                  ROW_NUMBER() OVER (PARTITION BY carrid ORDER BY fldate) as row_num
           FROM sflight""",
        
        # Invalid query
        "SELECT FROM WHERE",
    ]
    
    print_colored("\n🚀 ABAP SQL Syntax Checker - Using Custom ABAP Dialect\n", 
                  Fore.MAGENTA if COLORAMA_AVAILABLE else "")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'─' * 70}")
        print_colored(f"Test Query #{i}", Fore.YELLOW if COLORAMA_AVAILABLE else "")
        print(f"{'─' * 70}")
        
        analysis = checker.analyze_query(query)
        print_analysis(analysis)
    
    print_colored("✨ Demo completed!\n", Fore.MAGENTA if COLORAMA_AVAILABLE else "")


if __name__ == "__main__":
    main()

