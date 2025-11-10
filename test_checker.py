"""
Unit Tests for ABAP SQL Checker

This test suite validates the ABAP SQL Syntax Checker using the custom
ABAP dialect implementation.

Run with: python -m pytest test_checker.py
Or simply: python test_checker.py
"""

import unittest
from abap_sql_checker import ABAPSQLChecker


class TestABAPSQLChecker(unittest.TestCase):
    """Test cases for ABAP SQL Checker."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_simple_select(self):
        """Test basic SELECT statement."""
        sql = "SELECT carrid, connid FROM sflight WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, but got errors: {errors}")
        self.assertIsNotNone(ast)
        self.assertEqual(len(errors), 0)
    
    def test_select_with_join(self):
        """Test SELECT with JOIN."""
        sql = """SELECT f.carrid, p.cityfrom
                 FROM sflight AS f
                 INNER JOIN spfli AS p ON f.carrid = p.carrid"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, but got errors: {errors}")
    
    def test_select_with_aggregate(self):
        """Test SELECT with aggregate functions."""
        sql = "SELECT carrid, COUNT(*) as cnt FROM sflight GROUP BY carrid"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, but got errors: {errors}")
    
    def test_select_with_subquery(self):
        """Test SELECT with subquery."""
        sql = """SELECT carrid FROM spfli
                 WHERE carrid IN (SELECT carrid FROM sflight WHERE seatsocc > 100)"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, but got errors: {errors}")
    
    def test_invalid_syntax(self):
        """Test invalid SQL syntax."""
        sql = "SELECT FROM WHERE"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_update_statement(self):
        """Test UPDATE statement."""
        sql = "UPDATE sflight SET seatsocc = 100 WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, but got errors: {errors}")
    
    def test_delete_statement(self):
        """Test DELETE statement."""
        sql = "DELETE FROM sbook WHERE customid = '123'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, but got errors: {errors}")
    
    def test_insert_statement(self):
        """Test INSERT statement."""
        sql = "INSERT INTO spfli (carrid, connid) VALUES ('XX', '1234')"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, but got errors: {errors}")
    
    def test_analyze_query(self):
        """Test query analysis."""
        sql = "SELECT carrid, connid FROM sflight WHERE carrid = 'AA'"
        analysis = self.checker.analyze_query(sql)
        
        self.assertTrue(analysis['valid'])
        self.assertIn('sflight', analysis['tables'])
        self.assertIn('carrid', analysis['columns'])
        self.assertIn('connid', analysis['columns'])
        self.assertTrue(analysis['has_where_clause'])
        self.assertFalse(analysis['has_join'])
    
    def test_format_sql(self):
        """Test SQL formatting."""
        sql = "SELECT carrid,connid FROM sflight WHERE carrid='AA'"
        formatted = self.checker.format_sql(sql, pretty=True)
        self.assertIsNotNone(formatted)
        self.assertIn('SELECT', formatted)
    
    def test_select_star_warning(self):
        """Test that SELECT * generates a warning."""
        sql = "SELECT * FROM sflight"
        analysis = self.checker.analyze_query(sql)
        self.assertTrue(analysis['valid'])
        self.assertGreater(len(analysis['warnings']), 0)
    
    def test_case_expression(self):
        """Test CASE expression."""
        sql = """SELECT carrid,
                        CASE
                          WHEN seatsocc > 200 THEN 'HIGH'
                          ELSE 'LOW'
                        END as level
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, but got errors: {errors}")
    
    def test_order_by(self):
        """Test ORDER BY clause."""
        sql = "SELECT carrid, connid FROM sflight ORDER BY carrid DESC, connid ASC"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, but got errors: {errors}")
    
    def test_having_clause(self):
        """Test HAVING clause."""
        sql = """SELECT carrid, COUNT(*) as cnt
                 FROM sflight
                 GROUP BY carrid
                 HAVING COUNT(*) > 10"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, but got errors: {errors}")


def run_tests():
    """Run all tests and display results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestABAPSQLChecker)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)

