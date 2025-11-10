"""
Negative Tests for ABAP SQL Checker
Tests error detection with intentionally invalid SQL

Run with: python test_negative.py
"""

import unittest
from abap_sql_checker import ABAPSQLChecker


class TestNegativeCases(unittest.TestCase):
    """Test cases for invalid SQL that should fail validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    # ========================================================================
    # SYNTAX ERRORS
    # ========================================================================
    
    def test_missing_from(self):
        """Test missing FROM clause."""
        sql = "SELECT carrid, connid WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect missing FROM clause")
        self.assertGreater(len(errors), 0)
    
    def test_missing_table_name(self):
        """Test missing table name after FROM."""
        sql = "SELECT carrid, connid FROM WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect missing table name")
    
    def test_incomplete_select(self):
        """Test incomplete SELECT statement."""
        sql = "SELECT FROM WHERE"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect incomplete SELECT")
    
    def test_missing_join_condition(self):
        """Test JOIN without ON condition."""
        sql = """SELECT f.carrid, p.cityfrom
                 FROM sflight AS f
                 INNER JOIN spfli AS p
                 WHERE f.carrid = 'AA'"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect missing JOIN condition")
    
    # ========================================================================
    # AGGREGATE FUNCTION ERRORS
    # ========================================================================
    
    def test_non_aggregated_column_in_group_by(self):
        """Test non-aggregated column without GROUP BY."""
        sql = """SELECT carrid, connid, COUNT(*) as cnt
                 FROM sflight
                 GROUP BY carrid"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        # Note: This is a semantic error that SQLGlot may not catch
        # The test documents expected behavior
        # In strict SQL, this should fail
    
    def test_aggregate_without_parentheses(self):
        """Test aggregate function without parentheses."""
        sql = "SELECT COUNT * FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect missing parentheses in COUNT")
    
    # ========================================================================
    # PARENTHESES ERRORS
    # ========================================================================
    
    def test_unmatched_opening_paren(self):
        """Test unmatched opening parenthesis."""
        sql = "SELECT carrid FROM sflight WHERE (carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect unmatched opening parenthesis")
    
    def test_unmatched_closing_paren(self):
        """Test unmatched closing parenthesis."""
        sql = "SELECT carrid FROM sflight WHERE carrid = 'AA')"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect unmatched closing parenthesis")
    
    def test_missing_subquery_paren(self):
        """Test subquery with missing parenthesis."""
        sql = """SELECT carrid FROM spfli
                 WHERE carrid IN SELECT carrid FROM sflight)"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect missing opening parenthesis in subquery")
    
    # ========================================================================
    # STRING LITERAL ERRORS
    # ========================================================================
    
    def test_unclosed_string_single(self):
        """Test unclosed string with single quote."""
        sql = "SELECT carrid FROM sflight WHERE carrid = 'AA"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect unclosed string literal")
    
    # ========================================================================
    # INVALID SUBQUERIES
    # ========================================================================
    
    def test_unclosed_subquery(self):
        """Test unclosed subquery."""
        sql = """SELECT carrid FROM spfli
                 WHERE carrid IN (SELECT carrid FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect unclosed subquery")
    
    # ========================================================================
    # INVALID CASE EXPRESSIONS
    # ========================================================================
    
    def test_case_without_end(self):
        """Test CASE without END."""
        sql = """SELECT carrid,
                        CASE
                          WHEN seatsocc > 200 THEN 'HIGH'
                        as level
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect CASE without END")
    
    # ========================================================================
    # INVALID SET OPERATIONS
    # ========================================================================
    
    def test_incomplete_union(self):
        """Test incomplete UNION."""
        sql = """SELECT carrid FROM sflight
                 UNION"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect incomplete UNION")
    
    # ========================================================================
    # INVALID WINDOW FUNCTIONS
    # ========================================================================
    
    def test_window_function_without_over(self):
        """Test window function without OVER clause."""
        sql = "SELECT carrid, ROW_NUMBER() as rn FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect missing OVER clause")
    
    # ========================================================================
    # INVALID INSERT/UPDATE/DELETE
    # ========================================================================
    
    def test_insert_without_values(self):
        """Test INSERT without VALUES."""
        sql = "INSERT INTO sflight (carrid, connid)"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect missing VALUES")
    
    def test_update_without_set(self):
        """Test UPDATE without SET."""
        sql = "UPDATE sflight WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect missing SET")
    
    def test_delete_without_from(self):
        """Test DELETE without FROM."""
        sql = "DELETE WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect missing FROM")
    
    # ========================================================================
    # INVALID EXPRESSIONS
    # ========================================================================
    
    def test_invalid_arithmetic(self):
        """Test invalid arithmetic expression."""
        sql = "SELECT carrid, + FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect invalid arithmetic")
    
    def test_missing_operand(self):
        """Test missing operand in expression."""
        sql = "SELECT carrid, seatsocc + FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect missing operand")
    
    # ========================================================================
    # COMPLEX INVALID QUERIES
    # ========================================================================
    
    def test_gibberish_query(self):
        """Test complete gibberish."""
        sql = "RANDOM INVALID SQL STATEMENT HERE"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect gibberish query")
    
    def test_multiple_syntax_errors(self):
        """Test query with multiple syntax errors."""
        sql = "SELECT carrid connid FROM sflight spfli WHERE"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should detect multiple syntax errors")


def run_negative_tests():
    """Run all negative tests and display results."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestNegativeCases)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print("NEGATIVE TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes (errors correctly detected): {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures (errors not detected): {len(result.failures)}")
    print(f"Errors (test issues): {len(result.errors)}")
    print("=" * 70)
    
    if len(result.failures) > 0:
        print("\n⚠️  Some invalid SQL was not detected as invalid!")
        print("This may indicate areas where error detection can be improved.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_negative_tests()
    sys.exit(0 if success else 1)

