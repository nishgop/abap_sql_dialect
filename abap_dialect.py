"""
ABAP SQL Dialect for SQLGlot

This module defines a custom ABAP SQL dialect that extends SQLGlot's
standard SQL capabilities to support ABAP-specific syntax and features.
"""

from sqlglot import exp
from sqlglot.dialects.dialect import Dialect
from sqlglot.dialects.postgres import Postgres
from sqlglot.tokens import TokenType, Tokenizer as BaseTokenizer
from sqlglot.parser import Parser as BaseParser
from sqlglot.generator import Generator as BaseGenerator


class ABAP(Postgres):
    """
    ABAP SQL Dialect
    
    Extends PostgreSQL dialect as it shares many similar features.
    Adds ABAP-specific keywords and syntax rules.
    """
    
    class Tokenizer(Postgres.Tokenizer):
        """ABAP SQL Tokenizer with ABAP-specific keywords."""
        
        KEYWORDS = {
            **Postgres.Tokenizer.KEYWORDS,
            # ABAP-specific keywords for SELECT (using VAR for custom keywords)
            "SINGLE": TokenType.VAR,  # SELECT SINGLE
            "APPENDING": TokenType.VAR,
            "CORRESPONDING": TokenType.VAR,
            "BYPASSING": TokenType.VAR,
            "BUFFER": TokenType.VAR,
            "CLIENT": TokenType.VAR,
            "SPECIFIED": TokenType.VAR,
            "PACKAGE": TokenType.VAR,
            "SIZE": TokenType.VAR,
            # ABAP table operations
            "FIELDS": TokenType.VAR,
            # Keep standard SQL keywords
            "UP": TokenType.VAR,
        }
        
        # ABAP uses both @ for host variables (modern) and : for parameters
        SINGLE_TOKENS = {
            **Postgres.Tokenizer.SINGLE_TOKENS,
            "@": TokenType.PARAMETER,  # Modern ABAP host variable syntax
        }
    
    class Parser(Postgres.Parser):
        """ABAP SQL Parser with ABAP-specific grammar rules."""
        
        FUNCTIONS = {
            **Postgres.Parser.FUNCTIONS,
            # Add ABAP-specific functions if needed
        }
        
        def _parse_select(self, nested: bool = False, table: bool = False, **kwargs):
            """
            Override SELECT parsing to handle ABAP-specific keywords.
            
            ABAP SELECT can have:
            - SINGLE (select single row)
            - DISTINCT
            - UP TO n ROWS
            - FOR UPDATE
            - BYPASSING BUFFER
            """
            # Check for SINGLE keyword (it's tokenized as VAR)
            single = self._match_text_seq("SINGLE")
            
            # Continue with standard SELECT parsing
            select = super()._parse_select(nested=nested, table=table, **kwargs)
            
            # Mark if this is a SINGLE select (store in metadata)
            if single and select:
                select.set("single", True)
            
            # Parse ABAP-specific clauses after standard clauses
            self._parse_abap_specific_clauses(select)
            
            return select
        
        def _parse_abap_specific_clauses(self, select):
            """Parse ABAP-specific clauses like BYPASSING BUFFER."""
            if not select:
                return
            
            # Check for "UP TO n ROWS"
            if self._match_text_seq("UP", "TO"):
                rows = self._parse_number()
                if self._match(TokenType.ROWS):
                    select.set("up_to_rows", rows.this if rows else None)
            
            # Check for "BYPASSING BUFFER"
            if self._match_text_seq("BYPASSING", "BUFFER"):
                select.set("bypassing_buffer", True)
            
            # Check for "CLIENT SPECIFIED"
            if self._match_text_seq("CLIENT", "SPECIFIED"):
                select.set("client_specified", True)
            
            return select
    
    class Generator(Postgres.Generator):
        """ABAP SQL Generator for converting AST back to ABAP SQL."""
        
        def select_sql(self, expression: exp.Select) -> str:
            """
            Generate ABAP SQL SELECT statement.
            
            Handles ABAP-specific keywords like SINGLE, UP TO n ROWS.
            """
            # Get standard SELECT
            sql = super().select_sql(expression)
            
            # Add ABAP-specific keywords
            if expression.args.get("single"):
                sql = sql.replace("SELECT", "SELECT SINGLE", 1)
            
            # Note: UP TO and BYPASSING BUFFER would need more complex handling
            # as they appear in different positions in the statement
            
            return sql
        
        def limit_sql(self, expression: exp.Limit) -> str:
            """
            Override LIMIT to support ABAP's 'UP TO n ROWS' syntax.
            """
            # Can generate either standard LIMIT or ABAP's UP TO n ROWS
            if self.dialect == "abap":
                return f"UP TO {self.sql(expression, 'expression')} ROWS"
            return super().limit_sql(expression)


# Convenience function to parse ABAP SQL
def parse_abap_sql(sql: str, **kwargs):
    """
    Parse ABAP SQL statement using the ABAP dialect.
    
    Args:
        sql: ABAP SQL statement to parse
        **kwargs: Additional arguments for parse_one
        
    Returns:
        Parsed expression tree
    """
    from sqlglot import parse_one
    return parse_one(sql, dialect=ABAP, **kwargs)


def format_abap_sql(sql: str, pretty: bool = True, **kwargs) -> str:
    """
    Format ABAP SQL statement.
    
    Args:
        sql: ABAP SQL statement to format
        pretty: Whether to use pretty printing
        **kwargs: Additional arguments
        
    Returns:
        Formatted SQL string
    """
    from sqlglot import parse_one
    parsed = parse_one(sql, dialect=ABAP, error_level=None)
    if parsed:
        return parsed.sql(dialect=ABAP, pretty=pretty)
    return sql


# Example usage and testing
if __name__ == "__main__":
    # Test ABAP-specific syntax
    test_queries = [
        # Standard SELECT
        "SELECT carrid, connid FROM sflight WHERE carrid = 'AA'",
        
        # SINGLE keyword
        "SELECT SINGLE carrid, connid FROM sflight WHERE carrid = 'AA'",
        
        # Host variables (modern @ syntax)
        "SELECT carrid FROM sflight WHERE carrid = @lv_carrid",
        
        # Host variables (classic : syntax)  
        "SELECT carrid FROM sflight WHERE carrid = :lv_carrid",
        
        # Complex query
        """SELECT f.carrid, f.connid, p.cityfrom
           FROM sflight AS f
           INNER JOIN spfli AS p ON f.carrid = p.carrid
           WHERE f.carrid = 'AA'""",
    ]
    
    print("=" * 80)
    print("ABAP SQL Dialect - Test Queries")
    print("=" * 80)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing: {query[:60]}...")
        try:
            parsed = parse_abap_sql(query)
            print(f"   ✓ Parsed successfully: {type(parsed).__name__}")
            
            # Try to format it
            formatted = format_abap_sql(query, pretty=False)
            print(f"   Formatted: {formatted[:80]}...")
            
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 80)

