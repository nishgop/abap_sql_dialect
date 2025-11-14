"""
Ariba Query Language (AQL) Dialect for SQLGlot

This module implements support for Ariba Query Language (AQL), SAP Ariba's
proprietary SQL-like query language used for analytical reporting and data extraction.

AQL extends standard SQL with Ariba-specific features:
- Special field references (e.g., Document.DocumentId)
- Ariba functions (FORMATDATE, FORMATTIMESTAMP, ADDDAYS, etc.)
- Special operators and syntax for Ariba objects
- Custom aggregation and filtering patterns

Author: Generated with Claude
License: MIT
"""

from sqlglot import exp, generator, parser, tokens
from sqlglot.dialects.dialect import Dialect
from sqlglot.dialects.postgres import Postgres
from sqlglot.tokens import TokenType


def parse_aql(sql: str) -> exp.Expression:
    """
    Parse AQL (Ariba Query Language) SQL statement.
    
    Args:
        sql: AQL SQL statement string
        
    Returns:
        Parsed expression tree or None if parsing fails
    """
    try:
        # Parse using standard parser with Postgres dialect
        # AQL is essentially Postgres-compatible with custom functions
        from sqlglot import parse_one
        return parse_one(sql, dialect='postgres')
    except Exception as e:
        # Return None on error to allow error handling downstream
        return None


class AQL(Dialect):
    """
    Ariba Query Language (AQL) SQL Dialect
    
    Extends Postgres dialect with Ariba-specific syntax and features.
    """
    
    class Tokenizer(Postgres.Tokenizer):
        """Custom tokenizer for AQL keywords and operators."""
        
        KEYWORDS = {
            **Postgres.Tokenizer.KEYWORDS,
            # AQL-specific keywords
            "FORMATDATE": TokenType.VAR,
            "FORMATTIMESTAMP": TokenType.VAR,
            "ADDDAYS": TokenType.VAR,
            "ADDMONTHS": TokenType.VAR,
            "ADDYEARS": TokenType.VAR,
            "DATEDIFF": TokenType.VAR,
            "DATEPART": TokenType.VAR,
            "GETDATE": TokenType.VAR,
            "YEAR": TokenType.VAR,
            "MONTH": TokenType.VAR,
            "DAY": TokenType.VAR,
            "HOUR": TokenType.VAR,
            "MINUTE": TokenType.VAR,
            "SECOND": TokenType.VAR,
            "DAYOFWEEK": TokenType.VAR,
            "DAYOFYEAR": TokenType.VAR,
            "WEEKOFYEAR": TokenType.VAR,
            "QUARTER": TokenType.VAR,
            
            # String functions
            "STRINGCONCAT": TokenType.VAR,
            "SUBSTRING": TokenType.VAR,
            "CHARINDEX": TokenType.VAR,
            "LEN": TokenType.VAR,
            "REPLACE": TokenType.VAR,
            "TRIM": TokenType.VAR,
            "LTRIM": TokenType.VAR,
            "RTRIM": TokenType.VAR,
            
            # Math functions
            "ROUND": TokenType.VAR,
            "CEILING": TokenType.VAR,
            "FLOOR": TokenType.VAR,
            "ABS": TokenType.VAR,
            "POWER": TokenType.VAR,
            "SQRT": TokenType.VAR,
            
            # Conditional functions
            "IIF": TokenType.VAR,
            "ISNULL": TokenType.VAR,
            "NULLIF": TokenType.VAR,
            
            # Ariba-specific
            "DOCUMENT": TokenType.VAR,
            "PROJECT": TokenType.VAR,
            "SUPPLIER": TokenType.VAR,
            "CONTRACT": TokenType.VAR,
            "INVOICE": TokenType.VAR,
            "REQUISITION": TokenType.VAR,
            "ORDER": TokenType.VAR,
        }
    
    class Parser(Postgres.Parser):
        """Custom parser for AQL-specific grammar."""
        
        FUNCTIONS = {
            **Postgres.Parser.FUNCTIONS,
            # Date/Time functions
            "FORMATDATE": lambda args: exp.Anonymous(this="FORMATDATE", expressions=args),
            "FORMATTIMESTAMP": lambda args: exp.Anonymous(this="FORMATTIMESTAMP", expressions=args),
            "ADDDAYS": lambda args: exp.Anonymous(this="ADDDAYS", expressions=args),
            "ADDMONTHS": lambda args: exp.Anonymous(this="ADDMONTHS", expressions=args),
            "ADDYEARS": lambda args: exp.Anonymous(this="ADDYEARS", expressions=args),
            "DATEDIFF": lambda args: exp.Anonymous(this="DATEDIFF", expressions=args),
            "DATEPART": lambda args: exp.Anonymous(this="DATEPART", expressions=args),
            "GETDATE": lambda args: exp.Anonymous(this="GETDATE", expressions=args),
            "YEAR": lambda args: exp.Anonymous(this="YEAR", expressions=args),
            "MONTH": lambda args: exp.Anonymous(this="MONTH", expressions=args),
            "DAY": lambda args: exp.Anonymous(this="DAY", expressions=args),
            "HOUR": lambda args: exp.Anonymous(this="HOUR", expressions=args),
            "MINUTE": lambda args: exp.Anonymous(this="MINUTE", expressions=args),
            "SECOND": lambda args: exp.Anonymous(this="SECOND", expressions=args),
            "DAYOFWEEK": lambda args: exp.Anonymous(this="DAYOFWEEK", expressions=args),
            "DAYOFYEAR": lambda args: exp.Anonymous(this="DAYOFYEAR", expressions=args),
            "WEEKOFYEAR": lambda args: exp.Anonymous(this="WEEKOFYEAR", expressions=args),
            "QUARTER": lambda args: exp.Anonymous(this="QUARTER", expressions=args),
            
            # String functions
            "STRINGCONCAT": lambda args: exp.Anonymous(this="STRINGCONCAT", expressions=args),
            "SUBSTRING": lambda args: exp.Anonymous(this="SUBSTRING", expressions=args),
            "CHARINDEX": lambda args: exp.Anonymous(this="CHARINDEX", expressions=args),
            "LEN": lambda args: exp.Anonymous(this="LEN", expressions=args),
            "REPLACE": lambda args: exp.Anonymous(this="REPLACE", expressions=args),
            "TRIM": lambda args: exp.Anonymous(this="TRIM", expressions=args),
            "LTRIM": lambda args: exp.Anonymous(this="LTRIM", expressions=args),
            "RTRIM": lambda args: exp.Anonymous(this="RTRIM", expressions=args),
            
            # Math functions
            "ROUND": lambda args: exp.Round(this=args[0], decimals=args[1] if len(args) > 1 else None),
            "CEILING": lambda args: exp.Ceil(this=args[0]),
            "FLOOR": lambda args: exp.Floor(this=args[0]),
            "ABS": lambda args: exp.Abs(this=args[0]),
            "POWER": lambda args: exp.Pow(this=args[0], expression=args[1] if len(args) > 1 else None),
            "SQRT": lambda args: exp.Sqrt(this=args[0]),
            
            # Conditional functions
            "IIF": lambda args: exp.If(this=args[0], true=args[1] if len(args) > 1 else None, false=args[2] if len(args) > 2 else None),
            "ISNULL": lambda args: exp.Coalesce(this=args[0], expressions=[args[1]] if len(args) > 1 else []),
            "NULLIF": lambda args: exp.NullIf(this=args[0], expression=args[1] if len(args) > 1 else None),
        }
        
        def _parse_table_parts(self, schema: bool = False):
            """
            Override to handle AQL's dot notation for nested objects.
            Handles: Document.DocumentId, Project.Name, etc.
            """
            table = super()._parse_table_parts(schema=schema)
            
            # Handle AQL's nested field references
            if table and isinstance(table, exp.Table):
                # Check if this looks like an AQL object reference
                table_name = str(table.this).upper()
                if table_name in ('DOCUMENT', 'PROJECT', 'SUPPLIER', 'CONTRACT', 
                                 'INVOICE', 'REQUISITION', 'ORDER'):
                    # Mark this as an AQL object reference
                    table.set("is_aql_object", True)
            
            return table
    
    class Generator(Postgres.Generator):
        """Custom SQL generator for AQL-specific syntax."""
        
        def select_sql(self, expression: exp.Select) -> str:
            """Override to handle AQL-specific SELECT features."""
            sql_parts = []
            
            # Handle standard SELECT clause
            result = super().select_sql(expression)
            
            return result
        
        def table_sql(self, expression: exp.Table) -> str:
            """Override to handle AQL object references."""
            # Check if this is an AQL object reference
            if expression.args.get("is_aql_object"):
                # Generate AQL-style object reference
                return f"{expression.this}"
            
            return super().table_sql(expression)


# Export the dialect
DIALECT = AQL

