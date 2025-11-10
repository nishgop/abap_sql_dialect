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
            "APPENDING": TokenType.VAR,  # APPENDING TABLE
            "CORRESPONDING": TokenType.VAR,  # CORRESPONDING FIELDS OF
            "BYPASSING": TokenType.VAR,  # BYPASSING BUFFER
            "BUFFER": TokenType.VAR,
            "CLIENT": TokenType.VAR,  # CLIENT SPECIFIED
            "SPECIFIED": TokenType.VAR,
            "PACKAGE": TokenType.VAR,  # PACKAGE SIZE
            "SIZE": TokenType.VAR,
            # ABAP table operations
            "FIELDS": TokenType.VAR,
            # Additional keywords
            "UP": TokenType.VAR,  # UP TO n ROWS
            "ROWS": TokenType.ROWS,  # For UP TO n ROWS
            # ABAP-specific string operators
            "CP": TokenType.VAR,  # Contains Pattern
            "NP": TokenType.VAR,  # Not contains Pattern
            "CA": TokenType.VAR,  # Contains Any
            "NA": TokenType.VAR,  # Not contains Any
            "CS": TokenType.VAR,  # Contains String
            "NS": TokenType.VAR,  # Not contains String
            "CO": TokenType.VAR,  # Contains Only
            "CN": TokenType.VAR,  # Not contains Only
        }
        
        # ABAP uses both @ for host variables (modern) and : for parameters
        # Also supports ~ for field symbols and => for associations
        SINGLE_TOKENS = {
            **Postgres.Tokenizer.SINGLE_TOKENS,
            "@": TokenType.PARAMETER,  # Modern ABAP host variable syntax
            "~": TokenType.TILDA,  # Tilde for field access (table~field)
        }
    
    class Parser(Postgres.Parser):
        """ABAP SQL Parser with ABAP-specific grammar rules."""
        
        FUNCTIONS = {
            **Postgres.Parser.FUNCTIONS,
            # ABAP-specific string functions
            "CONCAT_WITH_SPACE": lambda args: exp.Anonymous(this="CONCAT_WITH_SPACE", expressions=args),
            # ABAP aggregate functions
            "STRING_AGG": lambda args: exp.GroupConcat(this=args[0], separator=args[1] if len(args) > 1 else exp.Literal.string(",")),
            # ABAP conversion functions
            "CAST": lambda args: exp.Cast(this=args[0], to=args[1]) if len(args) > 1 else exp.Cast(this=args[0]),
        }
        
        def _parse_term(self):
            """Override to handle ABAP string comparison operators at term level."""
            # Parse left side using standard term parsing
            this = super()._parse_term()
            
            # Check if next token is an ABAP string operator
            if self._curr and self._curr.text and self._curr.text.upper() in ("CP", "NP", "CS", "NS", "CA", "NA", "CO", "CN"):
                op_text = self._curr.text.upper()
                self._advance()  # Consume the operator token
                
                # Parse right side
                right = super()._parse_term()
                
                # Map to LIKE/NOT LIKE (closest SQL equivalent)
                if op_text.startswith("N"):  # Negated operators (NP, NS, NA, CN)
                    return self.expression(exp.Not, this=self.expression(exp.Like, this=this, expression=right))
                else:  # Positive operators (CP, CS, CA, CO)
                    return self.expression(exp.Like, this=this, expression=right)
            
            return this
        
        def _parse_select(self, nested: bool = False, table: bool = False, **kwargs):
            """
            Override SELECT parsing to handle ABAP-specific keywords.
            
            ABAP SELECT can have:
            - SINGLE (select single row)
            - DISTINCT
            - UP TO n ROWS
            - FOR UPDATE
            - BYPASSING BUFFER
            - CLIENT SPECIFIED
            - PACKAGE SIZE
            """
            # Check for SINGLE keyword (it's tokenized as VAR)
            single = self._match_text_seq("SINGLE")
            
            # Continue with standard SELECT parsing
            # This will parse: SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT
            select = super()._parse_select(nested=nested, table=table, **kwargs)
            
            # Mark if this is a SINGLE select (store in metadata)
            if single and select:
                select.set("single", True)
            
            # NOW parse ABAP-specific clauses that come after standard SQL clauses
            # These are at the end: UP TO, BYPASSING BUFFER, CLIENT SPECIFIED, FOR UPDATE, PACKAGE SIZE
            if select:
                # Try to parse each ABAP clause (order matters!)
                
                # UP TO n ROWS (like LIMIT but ABAP-specific)
                if self._match_text_seq("UP"):
                    if self._match_text_seq("TO"):
                        if self._match(TokenType.NUMBER):
                            rows_value = self._prev.text
                            if self._match(TokenType.ROWS):
                                select.set("up_to_rows", rows_value)
                
                # BYPASSING BUFFER
                if self._match_text_seq("BYPASSING"):
                    if self._match_text_seq("BUFFER"):
                        select.set("bypassing_buffer", True)
                
                # CLIENT SPECIFIED
                if self._match_text_seq("CLIENT"):
                    if self._match_text_seq("SPECIFIED"):
                        select.set("client_specified", True)
                
                # FOR UPDATE
                if self._match_text_seq("FOR"):
                    if self._match(TokenType.UPDATE):
                        select.set("for_update", True)
                
                # PACKAGE SIZE n
                if self._match_text_seq("PACKAGE"):
                    if self._match_text_seq("SIZE"):
                        if self._match(TokenType.NUMBER):
                            size_value = self._prev.text
                            select.set("package_size", size_value)
            
            return select
        
        def _parse_abap_specific_clauses(self, select):
            """
            Parse ABAP-specific clauses.
            
            Supports:
            - INTO @var, INTO TABLE @itab, APPENDING TABLE @itab
            - UP TO n ROWS
            - BYPASSING BUFFER
            - CLIENT SPECIFIED  
            - FOR UPDATE
            - PACKAGE SIZE n
            """
            if not select:
                return
            
            # Check for "INTO" clause (must come before other clauses)
            if self._match(TokenType.INTO):
                into_expr = self._parse_into_clause()
                if into_expr:
                    select.set("into", into_expr)
            
            # Check for "APPENDING TABLE"
            if self._match_text_seq("APPENDING"):
                if self._match(TokenType.TABLE):
                    table_var = self._parse_field()
                    select.set("appending_table", table_var)
            
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
            
            # Check for "FOR UPDATE"
            if self._match_text_seq("FOR"):
                if self._match(TokenType.UPDATE):
                    select.set("for_update", True)
            
            # Check for "PACKAGE SIZE"
            if self._match_text_seq("PACKAGE", "SIZE"):
                size = self._parse_number()
                select.set("package_size", size.this if size else None)
            
            return select
        
        def _parse_into_clause(self):
            """
            Parse INTO clause variations:
            - INTO @var
            - INTO TABLE @itab
            - INTO CORRESPONDING FIELDS OF @var
            """
            # Check for "TABLE" keyword
            is_table = self._match(TokenType.TABLE)
            
            # Check for "CORRESPONDING FIELDS OF"
            is_corresponding = False
            if self._match_text_seq("CORRESPONDING", "FIELDS"):
                if self._match_text_seq("OF"):
                    is_corresponding = True
            
            # Parse the target variable
            target = self._parse_field()
            
            if target:
                into_dict = {"target": target}
                if is_table:
                    into_dict["type"] = "table"
                if is_corresponding:
                    into_dict["corresponding"] = True
                return into_dict
            
            return None
    
    class Generator(Postgres.Generator):
        """ABAP SQL Generator for converting AST back to ABAP SQL."""
        
        def select_sql(self, expression: exp.Select) -> str:
            """
            Generate ABAP SQL SELECT statement.
            
            Handles ABAP-specific keywords:
            - SINGLE
            - INTO clauses
            - UP TO n ROWS
            - BYPASSING BUFFER
            - CLIENT SPECIFIED
            - FOR UPDATE
            - PACKAGE SIZE
            """
            # Start with SELECT keyword
            sql_parts = ["SELECT"]
            
            # Add SINGLE if present
            if expression.args.get("single"):
                sql_parts.append("SINGLE")
            
            # Add DISTINCT if present
            if expression.args.get("distinct"):
                sql_parts.append("DISTINCT")
            
            # Add select expressions
            expressions = expression.expressions
            if expressions:
                sql_parts.append(", ".join([self.sql(e) for e in expressions]))
            
            # Add INTO clause if present
            into = expression.args.get("into")
            if into:
                into_sql = self._generate_into_clause(into)
                sql_parts.append(into_sql)
            
            # Add APPENDING TABLE if present
            appending = expression.args.get("appending_table")
            if appending:
                sql_parts.append(f"APPENDING TABLE {self.sql(appending)}")
            
            # Add FROM clause
            from_clause = expression.args.get("from")
            if from_clause:
                sql_parts.append(f"FROM {self.sql(from_clause)}")
            
            # Add JOIN clauses
            joins = expression.args.get("joins")
            if joins:
                for join in joins:
                    sql_parts.append(self.sql(join))
            
            # Add WHERE clause
            where = expression.args.get("where")
            if where:
                sql_parts.append(f"WHERE {self.sql(where.this)}")
            
            # Add GROUP BY
            group = expression.args.get("group")
            if group:
                sql_parts.append(self.sql(group))
            
            # Add HAVING
            having = expression.args.get("having")
            if having:
                sql_parts.append(f"HAVING {self.sql(having.this)}")
            
            # Add ORDER BY
            order = expression.args.get("order")
            if order:
                sql_parts.append(self.sql(order))
            
            # Add UP TO n ROWS
            up_to_rows = expression.args.get("up_to_rows")
            if up_to_rows:
                sql_parts.append(f"UP TO {up_to_rows} ROWS")
            
            # Add BYPASSING BUFFER
            if expression.args.get("bypassing_buffer"):
                sql_parts.append("BYPASSING BUFFER")
            
            # Add CLIENT SPECIFIED
            if expression.args.get("client_specified"):
                sql_parts.append("CLIENT SPECIFIED")
            
            # Add FOR UPDATE
            if expression.args.get("for_update"):
                sql_parts.append("FOR UPDATE")
            
            # Add PACKAGE SIZE
            package_size = expression.args.get("package_size")
            if package_size:
                sql_parts.append(f"PACKAGE SIZE {package_size}")
            
            return " ".join(sql_parts)
        
        def _generate_into_clause(self, into_dict):
            """Generate INTO clause from parsed dictionary."""
            parts = ["INTO"]
            
            if into_dict.get("type") == "table":
                parts.append("TABLE")
            
            if into_dict.get("corresponding"):
                parts.append("CORRESPONDING FIELDS OF")
            
            target = into_dict.get("target")
            if target:
                parts.append(self.sql(target))
            
            return " ".join(parts)
        
        def limit_sql(self, expression: exp.Limit) -> str:
            """
            Override LIMIT to support ABAP's 'UP TO n ROWS' syntax.
            """
            # For ABAP, use UP TO n ROWS instead of LIMIT
            return f"UP TO {self.sql(expression, 'expression')} ROWS"


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

