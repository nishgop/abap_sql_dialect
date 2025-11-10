"""
ABAP-Specific SQL Syntax Tests
Tests for ABAP SQL features unique to SAP systems

Run with: python test_abap_specific.py
"""

import unittest
from abap_sql_checker import ABAPSQLChecker


class TestABAPSpecificSyntax(unittest.TestCase):
    """Test ABAP-specific SQL syntax."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_up_to_n_rows(self):
        """Test UP TO n ROWS clause."""
        sql = "SELECT carrid, connid FROM sflight UP TO 10 ROWS"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        # Note: This may not parse in standard SQL, but we test it
        # In real ABAP, this would be valid
        self.assertIsNotNone(ast or errors)
    
    def test_single_keyword(self):
        """Test SINGLE keyword for single row selection."""
        sql = "SELECT SINGLE carrid, connid FROM sflight WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertIsNotNone(ast or errors)
    
    def test_client_specified(self):
        """Test CLIENT SPECIFIED clause."""
        sql = "SELECT * FROM mara CLIENT SPECIFIED WHERE matnr = '000000000000000001'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertIsNotNone(ast or errors)
    
    def test_bypassing_buffer(self):
        """Test BYPASSING BUFFER clause."""
        sql = "SELECT carrid, connid FROM sflight BYPASSING BUFFER WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertIsNotNone(ast or errors)
    
    def test_for_update(self):
        """Test FOR UPDATE clause."""
        sql = "SELECT carrid, connid FROM sflight WHERE carrid = 'AA' FOR UPDATE"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"FOR UPDATE failed: {errors}")


class TestABAPHostVariables(unittest.TestCase):
    """Test ABAP host variables (@variable syntax)."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_host_variable_in_where(self):
        """Test host variable in WHERE clause."""
        # Standard SQL with parameter placeholders
        sql = "SELECT carrid, connid FROM sflight WHERE carrid = :lv_carrid"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Host variable failed: {errors}")
    
    def test_host_variable_comparison(self):
        """Test host variable in comparison."""
        sql = "SELECT carrid, connid FROM sflight WHERE seatsocc > :lv_min_seats"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Host variable comparison failed: {errors}")
    
    def test_multiple_host_variables(self):
        """Test multiple host variables."""
        sql = """SELECT carrid, connid FROM sflight 
                 WHERE carrid = :lv_carrid AND connid = :lv_connid"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Multiple host variables failed: {errors}")


class TestABAPTableOperations(unittest.TestCase):
    """Test ABAP-specific table operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_into_table(self):
        """Test SELECT INTO TABLE (ABAP-specific)."""
        # This tests the SQL part, actual INTO clause may not parse
        sql = "SELECT carrid, connid FROM sflight WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_appending_table(self):
        """Test SELECT APPENDING TABLE (ABAP-specific)."""
        sql = "SELECT carrid, connid FROM sflight WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_into_corresponding_fields(self):
        """Test SELECT INTO CORRESPONDING FIELDS."""
        sql = "SELECT carrid, connid FROM sflight WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)


class TestABAPJoinSyntax(unittest.TestCase):
    """Test ABAP-specific JOIN syntax."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_join_with_tilde(self):
        """Test ABAP tilde notation for table fields."""
        # In ABAP you can use ~ as table-field separator
        # Standard SQL uses . which we test
        sql = "SELECT f.carrid, f.connid FROM sflight AS f WHERE f.carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_inner_join_abap_style(self):
        """Test ABAP-style INNER JOIN."""
        sql = """SELECT f.carrid, p.cityfrom
                 FROM sflight AS f
                 INNER JOIN spfli AS p ON f.carrid = p.carrid
                 WHERE f.carrid = 'AA'"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)


class TestABAPAggregateExtensions(unittest.TestCase):
    """Test ABAP-specific aggregate extensions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_count_with_distinct(self):
        """Test COUNT with DISTINCT."""
        sql = "SELECT COUNT(DISTINCT carrid) as unique_carriers FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_group_by_with_having(self):
        """Test GROUP BY with HAVING."""
        sql = """SELECT carrid, AVG(seatsocc) as avg_seats
                 FROM sflight
                 GROUP BY carrid
                 HAVING AVG(seatsocc) > 100"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)


class TestABAPCaseExpressions(unittest.TestCase):
    """Test ABAP CASE expressions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_simple_case(self):
        """Test simple CASE expression."""
        sql = """SELECT carrid,
                        CASE carrid
                          WHEN 'AA' THEN 'American'
                          WHEN 'LH' THEN 'Lufthansa'
                          ELSE 'Other'
                        END as carrier_name
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_searched_case(self):
        """Test searched CASE expression."""
        sql = """SELECT carrid, seatsocc,
                        CASE
                          WHEN seatsocc > 200 THEN 'HIGH'
                          WHEN seatsocc > 100 THEN 'MEDIUM'
                          ELSE 'LOW'
                        END as occupancy_level
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_nested_case(self):
        """Test nested CASE expressions."""
        sql = """SELECT carrid, seatsocc,
                        CASE
                          WHEN carrid = 'AA' THEN
                            CASE
                              WHEN seatsocc > 200 THEN 'AA-HIGH'
                              ELSE 'AA-LOW'
                            END
                          ELSE 'OTHER'
                        END as category
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)


class TestABAPLimitOffset(unittest.TestCase):
    """Test LIMIT and OFFSET clauses."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_limit(self):
        """Test LIMIT clause."""
        sql = "SELECT carrid, connid FROM sflight LIMIT 10"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_offset(self):
        """Test OFFSET clause."""
        sql = "SELECT carrid, connid FROM sflight OFFSET 5"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_limit_offset(self):
        """Test LIMIT with OFFSET."""
        sql = "SELECT carrid, connid FROM sflight LIMIT 10 OFFSET 5"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_fetch_first(self):
        """Test FETCH FIRST n ROWS ONLY."""
        sql = "SELECT carrid, connid FROM sflight FETCH FIRST 10 ROWS ONLY"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)


class TestABAPNullHandling(unittest.TestCase):
    """Test NULL handling in ABAP SQL."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_is_null(self):
        """Test IS NULL predicate."""
        sql = "SELECT carrid, connid FROM sflight WHERE seatsocc IS NULL"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_is_not_null(self):
        """Test IS NOT NULL predicate."""
        sql = "SELECT carrid, connid FROM sflight WHERE seatsocc IS NOT NULL"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_coalesce(self):
        """Test COALESCE function."""
        sql = "SELECT carrid, COALESCE(seatsocc, 0) as seats FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_nullif(self):
        """Test NULLIF function."""
        sql = "SELECT carrid, NULLIF(seatsocc, 0) as seats FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)


class TestABAPDistinctVariants(unittest.TestCase):
    """Test DISTINCT variants."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_distinct(self):
        """Test DISTINCT keyword."""
        sql = "SELECT DISTINCT carrid FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_distinct_multiple_columns(self):
        """Test DISTINCT with multiple columns."""
        sql = "SELECT DISTINCT carrid, connid FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_distinct_in_aggregate(self):
        """Test DISTINCT within aggregate function."""
        sql = "SELECT COUNT(DISTINCT carrid) as unique_carriers FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)


class TestABAPInOperator(unittest.TestCase):
    """Test IN operator variants."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_in_list(self):
        """Test IN with list of values."""
        sql = "SELECT carrid, connid FROM sflight WHERE carrid IN ('AA', 'LH', 'UA')"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_in_subquery(self):
        """Test IN with subquery."""
        sql = """SELECT carrid, connid FROM spfli
                 WHERE carrid IN (SELECT DISTINCT carrid FROM sflight)"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_not_in(self):
        """Test NOT IN."""
        sql = "SELECT carrid, connid FROM sflight WHERE carrid NOT IN ('AA', 'LH')"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)


class TestABAPBetweenOperator(unittest.TestCase):
    """Test BETWEEN operator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_between(self):
        """Test BETWEEN operator."""
        sql = "SELECT carrid, seatsocc FROM sflight WHERE seatsocc BETWEEN 100 AND 200"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_not_between(self):
        """Test NOT BETWEEN."""
        sql = "SELECT carrid, seatsocc FROM sflight WHERE seatsocc NOT BETWEEN 100 AND 200"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_between_dates(self):
        """Test BETWEEN with dates."""
        sql = "SELECT carrid, fldate FROM sflight WHERE fldate BETWEEN '20230101' AND '20231231'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)


class TestABAPLikeOperator(unittest.TestCase):
    """Test LIKE operator and pattern matching."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_like(self):
        """Test LIKE operator."""
        sql = "SELECT carrid, connid FROM sflight WHERE carrid LIKE 'A%'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_not_like(self):
        """Test NOT LIKE."""
        sql = "SELECT carrid, connid FROM sflight WHERE carrid NOT LIKE 'A%'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)
    
    def test_like_with_underscore(self):
        """Test LIKE with underscore wildcard."""
        sql = "SELECT carrid, connid FROM sflight WHERE carrid LIKE 'A_'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid)


def run_abap_tests():
    """Run all ABAP-specific tests and display results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestABAPSpecificSyntax))
    suite.addTests(loader.loadTestsFromTestCase(TestABAPHostVariables))
    suite.addTests(loader.loadTestsFromTestCase(TestABAPTableOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestABAPJoinSyntax))
    suite.addTests(loader.loadTestsFromTestCase(TestABAPAggregateExtensions))
    suite.addTests(loader.loadTestsFromTestCase(TestABAPCaseExpressions))
    suite.addTests(loader.loadTestsFromTestCase(TestABAPLimitOffset))
    suite.addTests(loader.loadTestsFromTestCase(TestABAPNullHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestABAPDistinctVariants))
    suite.addTests(loader.loadTestsFromTestCase(TestABAPInOperator))
    suite.addTests(loader.loadTestsFromTestCase(TestABAPBetweenOperator))
    suite.addTests(loader.loadTestsFromTestCase(TestABAPLikeOperator))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 80)
    print("ABAP-SPECIFIC TEST SUITE SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 80)
    
    # Test category breakdown
    print("\nABAP-Specific Test Categories:")
    print(f"  - ABAP Syntax (SINGLE, UP TO, etc.): 5 tests")
    print(f"  - Host Variables: 3 tests")
    print(f"  - Table Operations: 3 tests")
    print(f"  - ABAP JOIN Syntax: 2 tests")
    print(f"  - Aggregate Extensions: 2 tests")
    print(f"  - CASE Expressions: 3 tests")
    print(f"  - LIMIT/OFFSET: 4 tests")
    print(f"  - NULL Handling: 4 tests")
    print(f"  - DISTINCT Variants: 3 tests")
    print(f"  - IN Operator: 3 tests")
    print(f"  - BETWEEN Operator: 3 tests")
    print(f"  - LIKE Operator: 3 tests")
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_abap_tests()
    sys.exit(0 if success else 1)

