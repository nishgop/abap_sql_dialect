"""
Basic AQL (Ariba Query Language) SQL Syntax Tests

This module contains basic tests for fundamental AQL SQL syntax validation,
covering SELECT, INSERT, UPDATE, DELETE, and basic query patterns.

Author: Generated with Claude
License: MIT
"""

import unittest
from aql_sql_checker import AQLSQLChecker
from sqlglot import exp


class TestBasicAQLSyntax(unittest.TestCase):
    """Test basic AQL SQL syntax validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_simple_select(self):
        """Test simple SELECT statement."""
        sql = "SELECT Document.DocumentId, Document.Title FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
        self.assertIsNotNone(ast)
    
    def test_select_with_where(self):
        """Test SELECT with WHERE clause."""
        sql = "SELECT * FROM Document WHERE Document.Status = 'Active'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_select_with_multiple_conditions(self):
        """Test SELECT with AND/OR conditions."""
        sql = "SELECT * FROM Document WHERE Document.Status = 'Active' AND Document.Amount > 1000"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_select_with_in_clause(self):
        """Test SELECT with IN clause."""
        sql = "SELECT * FROM Document WHERE Document.Status IN ('Active', 'Pending')"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_select_with_between(self):
        """Test SELECT with BETWEEN."""
        sql = "SELECT * FROM Invoice WHERE Invoice.Amount BETWEEN 1000 AND 5000"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_select_with_like(self):
        """Test SELECT with LIKE pattern."""
        sql = "SELECT * FROM Supplier WHERE Supplier.Name LIKE '%Corp%'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_select_missing_from(self):
        """Test that SELECT without FROM is detected as invalid."""
        sql = "SELECT Document.DocumentId WHERE Document.Status = 'Active'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should be invalid: missing FROM")
        self.assertIn("Missing FROM", str(errors))
    
    def test_select_with_alias(self):
        """Test SELECT with table and column aliases."""
        sql = "SELECT d.DocumentId as Id, d.Title as Name FROM Document d"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_select_distinct(self):
        """Test SELECT DISTINCT."""
        sql = "SELECT DISTINCT Supplier.Region FROM Supplier"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_select_top(self):
        """Test SELECT TOP."""
        sql = "SELECT TOP 10 Document.DocumentId FROM Document ORDER BY Document.Amount DESC"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestAQLInsertUpdateDelete(unittest.TestCase):
    """Test INSERT, UPDATE, DELETE statements."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_insert_with_values(self):
        """Test INSERT with VALUES."""
        sql = "INSERT INTO Document (DocumentId, Title, Status) VALUES (1, 'Test', 'Active')"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_insert_without_values(self):
        """Test INSERT without VALUES is invalid."""
        sql = "INSERT INTO Document (DocumentId, Title)"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should be invalid: missing VALUES")
    
    def test_update_with_set(self):
        """Test UPDATE with SET clause."""
        sql = "UPDATE Document SET Status = 'Completed' WHERE DocumentId = 1"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_update_without_set(self):
        """Test UPDATE without SET is invalid."""
        sql = "UPDATE Document WHERE DocumentId = 1"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should be invalid: missing SET")
    
    def test_delete_with_where(self):
        """Test DELETE with WHERE clause."""
        sql = "DELETE FROM Document WHERE DocumentId = 1"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_delete_all(self):
        """Test DELETE without WHERE (delete all)."""
        sql = "DELETE FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestAQLOrderBy(unittest.TestCase):
    """Test ORDER BY clause."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_order_by_asc(self):
        """Test ORDER BY ascending."""
        sql = "SELECT * FROM Document ORDER BY Document.Amount ASC"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_order_by_desc(self):
        """Test ORDER BY descending."""
        sql = "SELECT * FROM Document ORDER BY Document.Amount DESC"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_order_by_multiple_columns(self):
        """Test ORDER BY with multiple columns."""
        sql = "SELECT * FROM Document ORDER BY Document.Status ASC, Document.Amount DESC"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestAQLQueryAnalysis(unittest.TestCase):
    """Test query analysis functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_analyze_basic_select(self):
        """Test analysis of basic SELECT query."""
        sql = "SELECT DocumentId, Title FROM Document WHERE Status = 'Active'"
        analysis = self.checker.analyze_query(sql)
        
        self.assertTrue(analysis['is_valid'])
        self.assertIn('Document', analysis['tables'])
        self.assertIn('FROM', analysis['clauses'])
        self.assertIn('WHERE', analysis['clauses'])
        self.assertEqual(analysis['statement_type'], 'Select')
    
    def test_analyze_with_aggregate(self):
        """Test analysis of query with aggregates."""
        sql = "SELECT Status, COUNT(*) FROM Document GROUP BY Status"
        analysis = self.checker.analyze_query(sql)
        
        self.assertTrue(analysis['is_valid'])
        self.assertIn('COUNT', analysis['functions'])
        self.assertIn('GROUP BY', analysis['clauses'])
    
    def test_format_sql(self):
        """Test SQL formatting."""
        sql = "SELECT DocumentId,Title FROM Document WHERE Status='Active'"
        formatted = self.checker.format_sql(sql)
        
        self.assertIsNotNone(formatted)
        self.assertIn('SELECT', formatted.upper())


if __name__ == '__main__':
    unittest.main(verbosity=2)

