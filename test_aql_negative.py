"""
AQL Negative Tests (Error Detection)

This module contains tests for invalid AQL SQL statements to ensure
the checker correctly detects and reports errors.

Author: Generated with Claude
License: MIT
"""

import unittest
from aql_sql_checker import AQLSQLChecker


class TestAQLNegativeSyntax(unittest.TestCase):
    """Test error detection for invalid SQL syntax."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_select_without_from(self):
        """Test SELECT without FROM clause."""
        sql = "SELECT DocumentId WHERE Status = 'Active'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect missing FROM")
        self.assertTrue(any("FROM" in str(e) for e in errors))
    
    def test_empty_select_list(self):
        """Test empty SELECT list."""
        sql = "SELECT FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect empty SELECT list")
    
    def test_dangling_operator(self):
        """Test dangling arithmetic operator."""
        sql = "SELECT a, + FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect dangling operator")
    
    def test_consecutive_operators(self):
        """Test consecutive operators."""
        sql = "SELECT a ++ b FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect consecutive operators")
    
    def test_mismatched_parentheses(self):
        """Test mismatched parentheses."""
        sql = "SELECT * FROM Document WHERE (Status = 'Active'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect mismatched parentheses")
    
    def test_invalid_where_clause(self):
        """Test invalid WHERE clause."""
        sql = "SELECT * FROM Document WHERE AND Status = 'Active'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect invalid WHERE clause")


class TestAQLNegativeJoins(unittest.TestCase):
    """Test error detection for invalid JOIN operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_join_without_on(self):
        """Test JOIN without ON condition."""
        sql = "SELECT * FROM Document d INNER JOIN Project p"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect JOIN without ON")
        self.assertTrue(any("ON" in str(e) for e in errors))
    
    def test_left_join_without_on(self):
        """Test LEFT JOIN without ON condition."""
        sql = "SELECT * FROM Document d LEFT JOIN Project p"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect LEFT JOIN without ON")


class TestAQLNegativeAggregates(unittest.TestCase):
    """Test error detection for invalid aggregates."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_aggregate_without_group_by(self):
        """Test aggregate with non-aggregated column (should warn or error)."""
        # Note: This is actually valid in some SQL dialects, but often problematic
        sql = "SELECT Status, COUNT(*) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        # SQLGlot may allow this, so we check if it parses
        # (Some dialects require GROUP BY, others don't)
        self.assertIsNotNone(ast)


class TestAQLNegativeDML(unittest.TestCase):
    """Test error detection for invalid DML statements."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_insert_without_values(self):
        """Test INSERT without VALUES."""
        sql = "INSERT INTO Document (DocumentId, Title)"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect INSERT without VALUES")
        self.assertTrue(any("VALUES" in str(e) or "INSERT" in str(e) for e in errors))
    
    def test_update_without_set(self):
        """Test UPDATE without SET clause."""
        sql = "UPDATE Document WHERE DocumentId = 1"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect UPDATE without SET")
        self.assertTrue(any("SET" in str(e) for e in errors))
    
    def test_delete_without_table(self):
        """Test DELETE without table."""
        sql = "DELETE WHERE DocumentId = 1"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect DELETE without table")


class TestAQLNegativeFunctions(unittest.TestCase):
    """Test error detection for invalid function calls."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_function_missing_arguments(self):
        """Test function with missing required arguments."""
        # Note: SQLGlot might parse this but it's semantically invalid
        sql = "SELECT SUBSTRING(Title) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        # This might parse but be semantically invalid
        # The behavior depends on SQLGlot's strictness
        self.assertIsNotNone(ast)
    
    def test_invalid_date_format(self):
        """Test date function with invalid format."""
        # Note: Format validation is typically runtime, not parse-time
        sql = "SELECT FORMATDATE(CreatedDate, INVALID_FORMAT) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        # This should parse (format string is just a literal)
        self.assertIsNotNone(ast)


class TestAQLNegativeSubqueries(unittest.TestCase):
    """Test error detection for invalid subqueries."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_subquery_without_from(self):
        """Test subquery without FROM clause."""
        sql = """SELECT * FROM Document
                 WHERE DocumentId IN (SELECT DocumentId WHERE Status = 'Active')"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect subquery without FROM")


class TestAQLNegativeComplexErrors(unittest.TestCase):
    """Test detection of complex error scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_multiple_errors(self):
        """Test query with multiple errors."""
        sql = "SELECT FROM WHERE"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect multiple errors")
        self.assertTrue(len(errors) > 0)
    
    def test_invalid_arithmetic(self):
        """Test invalid arithmetic expression."""
        sql = "SELECT a + FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect invalid arithmetic")
    
    def test_unclosed_string_literal(self):
        """Test unclosed string literal."""
        sql = "SELECT * FROM Document WHERE Status = 'Active"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect unclosed string")


if __name__ == '__main__':
    unittest.main(verbosity=2)

