"""
Extended Unit Tests for ABAP SQL Checker
Comprehensive coverage of all major SQL variants

Run with: python test_checker_extended.py
"""

import unittest
from abap_sql_checker import ABAPSQLChecker


class TestJoinVariants(unittest.TestCase):
    """Test all JOIN types."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_inner_join(self):
        """Test INNER JOIN."""
        sql = """SELECT f.carrid, p.cityfrom
                 FROM sflight AS f
                 INNER JOIN spfli AS p ON f.carrid = p.carrid"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"INNER JOIN failed: {errors}")
    
    def test_left_join(self):
        """Test LEFT JOIN / LEFT OUTER JOIN."""
        sql = """SELECT c.name, b.customid
                 FROM scustom AS c
                 LEFT JOIN sbook AS b ON c.id = b.customid"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"LEFT JOIN failed: {errors}")
    
    def test_left_outer_join(self):
        """Test explicit LEFT OUTER JOIN."""
        sql = """SELECT c.name, b.customid
                 FROM scustom AS c
                 LEFT OUTER JOIN sbook AS b ON c.id = b.customid"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"LEFT OUTER JOIN failed: {errors}")
    
    def test_right_join(self):
        """Test RIGHT JOIN."""
        sql = """SELECT c.name, b.customid
                 FROM scustom AS c
                 RIGHT JOIN sbook AS b ON c.id = b.customid"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"RIGHT JOIN failed: {errors}")
    
    def test_right_outer_join(self):
        """Test explicit RIGHT OUTER JOIN."""
        sql = """SELECT c.name, b.customid
                 FROM scustom AS c
                 RIGHT OUTER JOIN sbook AS b ON c.id = b.customid"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"RIGHT OUTER JOIN failed: {errors}")
    
    def test_full_outer_join(self):
        """Test FULL OUTER JOIN."""
        sql = """SELECT c.name, b.customid
                 FROM scustom AS c
                 FULL OUTER JOIN sbook AS b ON c.id = b.customid"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"FULL OUTER JOIN failed: {errors}")
    
    def test_cross_join(self):
        """Test CROSS JOIN."""
        sql = """SELECT c.name, s.carrid
                 FROM scustom AS c
                 CROSS JOIN scarr AS s"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"CROSS JOIN failed: {errors}")
    
    def test_multiple_joins(self):
        """Test multiple JOINs in one query."""
        sql = """SELECT f.carrid, p.cityfrom, c.name
                 FROM sflight AS f
                 INNER JOIN spfli AS p ON f.carrid = p.carrid
                 LEFT JOIN sbook AS b ON f.carrid = b.carrid
                 LEFT JOIN scustom AS c ON b.customid = c.id"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Multiple JOINs failed: {errors}")
    
    def test_self_join(self):
        """Test self JOIN."""
        sql = """SELECT e1.name as employee, e2.name as manager
                 FROM employees AS e1
                 LEFT JOIN employees AS e2 ON e1.manager_id = e2.id"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Self JOIN failed: {errors}")


class TestAggregateFunctions(unittest.TestCase):
    """Test aggregate functions and GROUP BY."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_count(self):
        """Test COUNT aggregate."""
        sql = "SELECT carrid, COUNT(*) as cnt FROM sflight GROUP BY carrid"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"COUNT failed: {errors}")
    
    def test_count_distinct(self):
        """Test COUNT DISTINCT."""
        sql = "SELECT COUNT(DISTINCT carrid) as unique_carriers FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"COUNT DISTINCT failed: {errors}")
    
    def test_sum(self):
        """Test SUM aggregate."""
        sql = "SELECT carrid, SUM(seatsocc) as total_seats FROM sflight GROUP BY carrid"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"SUM failed: {errors}")
    
    def test_avg(self):
        """Test AVG aggregate."""
        sql = "SELECT carrid, AVG(seatsocc) as avg_seats FROM sflight GROUP BY carrid"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"AVG failed: {errors}")
    
    def test_min(self):
        """Test MIN aggregate."""
        sql = "SELECT carrid, MIN(seatsocc) as min_seats FROM sflight GROUP BY carrid"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"MIN failed: {errors}")
    
    def test_max(self):
        """Test MAX aggregate."""
        sql = "SELECT carrid, MAX(seatsocc) as max_seats FROM sflight GROUP BY carrid"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"MAX failed: {errors}")
    
    def test_multiple_aggregates(self):
        """Test multiple aggregate functions."""
        sql = """SELECT carrid,
                        COUNT(*) as flight_count,
                        SUM(seatsocc) as total_seats,
                        AVG(seatsocc) as avg_seats,
                        MIN(seatsocc) as min_seats,
                        MAX(seatsocc) as max_seats
                 FROM sflight
                 GROUP BY carrid"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Multiple aggregates failed: {errors}")
    
    def test_group_by_multiple_columns(self):
        """Test GROUP BY with multiple columns."""
        sql = """SELECT carrid, connid, COUNT(*) as cnt
                 FROM sflight
                 GROUP BY carrid, connid"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Multiple GROUP BY failed: {errors}")
    
    def test_having_clause(self):
        """Test HAVING clause with aggregates."""
        sql = """SELECT carrid, COUNT(*) as cnt
                 FROM sflight
                 GROUP BY carrid
                 HAVING COUNT(*) > 10"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"HAVING clause failed: {errors}")
    
    def test_having_with_multiple_conditions(self):
        """Test HAVING with multiple conditions."""
        sql = """SELECT carrid, AVG(seatsocc) as avg_seats
                 FROM sflight
                 GROUP BY carrid
                 HAVING AVG(seatsocc) > 100 AND COUNT(*) > 5"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Multiple HAVING conditions failed: {errors}")


class TestWindowFunctions(unittest.TestCase):
    """Test window functions and partitions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_row_number(self):
        """Test ROW_NUMBER window function."""
        sql = """SELECT carrid, connid, fldate,
                        ROW_NUMBER() OVER (ORDER BY fldate) as row_num
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"ROW_NUMBER failed: {errors}")
    
    def test_row_number_partition(self):
        """Test ROW_NUMBER with PARTITION BY."""
        sql = """SELECT carrid, connid, fldate,
                        ROW_NUMBER() OVER (PARTITION BY carrid ORDER BY fldate) as row_num
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"ROW_NUMBER with PARTITION failed: {errors}")
    
    def test_rank(self):
        """Test RANK window function."""
        sql = """SELECT carrid, seatsocc,
                        RANK() OVER (ORDER BY seatsocc DESC) as rank
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"RANK failed: {errors}")
    
    def test_dense_rank(self):
        """Test DENSE_RANK window function."""
        sql = """SELECT carrid, seatsocc,
                        DENSE_RANK() OVER (ORDER BY seatsocc DESC) as dense_rank
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"DENSE_RANK failed: {errors}")
    
    def test_lag(self):
        """Test LAG window function."""
        sql = """SELECT carrid, fldate, seatsocc,
                        LAG(seatsocc, 1) OVER (PARTITION BY carrid ORDER BY fldate) as prev_seats
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"LAG failed: {errors}")
    
    def test_lead(self):
        """Test LEAD window function."""
        sql = """SELECT carrid, fldate, seatsocc,
                        LEAD(seatsocc, 1) OVER (PARTITION BY carrid ORDER BY fldate) as next_seats
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"LEAD failed: {errors}")
    
    def test_sum_over(self):
        """Test SUM with OVER clause."""
        sql = """SELECT carrid, seatsocc,
                        SUM(seatsocc) OVER (PARTITION BY carrid) as total_by_carrier
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"SUM OVER failed: {errors}")
    
    def test_avg_over(self):
        """Test AVG with OVER clause."""
        sql = """SELECT carrid, seatsocc,
                        AVG(seatsocc) OVER (PARTITION BY carrid) as avg_by_carrier
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"AVG OVER failed: {errors}")
    
    def test_first_value(self):
        """Test FIRST_VALUE window function."""
        sql = """SELECT carrid, fldate, seatsocc,
                        FIRST_VALUE(seatsocc) OVER (PARTITION BY carrid ORDER BY fldate) as first_seats
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"FIRST_VALUE failed: {errors}")
    
    def test_last_value(self):
        """Test LAST_VALUE window function."""
        sql = """SELECT carrid, fldate, seatsocc,
                        LAST_VALUE(seatsocc) OVER (PARTITION BY carrid ORDER BY fldate
                                                   ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_seats
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"LAST_VALUE failed: {errors}")


class TestDateTimeFunctions(unittest.TestCase):
    """Test date and time functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_current_date(self):
        """Test CURRENT_DATE function."""
        sql = "SELECT carrid, CURRENT_DATE as today FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"CURRENT_DATE failed: {errors}")
    
    def test_current_timestamp(self):
        """Test CURRENT_TIMESTAMP function."""
        sql = "SELECT carrid, CURRENT_TIMESTAMP as now FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"CURRENT_TIMESTAMP failed: {errors}")
    
    def test_date_trunc(self):
        """Test DATE_TRUNC function."""
        sql = "SELECT DATE_TRUNC('month', fldate) as month, COUNT(*) FROM sflight GROUP BY DATE_TRUNC('month', fldate)"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"DATE_TRUNC failed: {errors}")
    
    def test_extract(self):
        """Test EXTRACT function."""
        sql = "SELECT EXTRACT(YEAR FROM fldate) as year, COUNT(*) FROM sflight GROUP BY EXTRACT(YEAR FROM fldate)"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"EXTRACT failed: {errors}")
    
    def test_date_add(self):
        """Test date arithmetic."""
        sql = "SELECT carrid, fldate, fldate + INTERVAL '7 days' as next_week FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Date arithmetic failed: {errors}")
    
    def test_date_diff(self):
        """Test DATEDIFF or date subtraction."""
        sql = "SELECT carrid, fldate - CURRENT_DATE as days_until FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Date difference failed: {errors}")


class TestStringFunctions(unittest.TestCase):
    """Test string manipulation functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_concat(self):
        """Test CONCAT function."""
        sql = "SELECT CONCAT(carrid, connid) as route_id FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"CONCAT failed: {errors}")
    
    def test_concat_operator(self):
        """Test concatenation with || operator."""
        sql = "SELECT carrid || '-' || connid as route_id FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"|| operator failed: {errors}")
    
    def test_substring(self):
        """Test SUBSTRING function."""
        sql = "SELECT SUBSTRING(carrid, 1, 2) as carrier_prefix FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"SUBSTRING failed: {errors}")
    
    def test_upper(self):
        """Test UPPER function."""
        sql = "SELECT UPPER(carrid) as carrier_upper FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"UPPER failed: {errors}")
    
    def test_lower(self):
        """Test LOWER function."""
        sql = "SELECT LOWER(carrid) as carrier_lower FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"LOWER failed: {errors}")
    
    def test_trim(self):
        """Test TRIM function."""
        sql = "SELECT TRIM(carrid) as carrier_trimmed FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"TRIM failed: {errors}")
    
    def test_length(self):
        """Test LENGTH function."""
        sql = "SELECT carrid, LENGTH(carrid) as carrier_length FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"LENGTH failed: {errors}")
    
    def test_replace(self):
        """Test REPLACE function."""
        sql = "SELECT REPLACE(carrid, 'A', 'X') as modified FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"REPLACE failed: {errors}")


class TestMathFunctions(unittest.TestCase):
    """Test mathematical functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_round(self):
        """Test ROUND function."""
        sql = "SELECT ROUND(AVG(seatsocc), 2) as avg_seats FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"ROUND failed: {errors}")
    
    def test_ceil(self):
        """Test CEIL function."""
        sql = "SELECT CEIL(AVG(seatsocc)) as ceiling FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"CEIL failed: {errors}")
    
    def test_floor(self):
        """Test FLOOR function."""
        sql = "SELECT FLOOR(AVG(seatsocc)) as floor_val FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"FLOOR failed: {errors}")
    
    def test_abs(self):
        """Test ABS function."""
        sql = "SELECT ABS(seatsocc - 200) as difference FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"ABS failed: {errors}")
    
    def test_mod(self):
        """Test MOD function."""
        sql = "SELECT carrid, MOD(seatsocc, 10) as remainder FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"MOD failed: {errors}")
    
    def test_power(self):
        """Test POWER function."""
        sql = "SELECT POWER(seatsocc, 2) as seats_squared FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"POWER failed: {errors}")
    
    def test_sqrt(self):
        """Test SQRT function."""
        sql = "SELECT SQRT(seatsocc) as seats_sqrt FROM sflight"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"SQRT failed: {errors}")


class TestOrderByVariants(unittest.TestCase):
    """Test ORDER BY variants."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_order_by_single(self):
        """Test ORDER BY single column."""
        sql = "SELECT carrid, connid FROM sflight ORDER BY carrid"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Single ORDER BY failed: {errors}")
    
    def test_order_by_asc(self):
        """Test ORDER BY ASC."""
        sql = "SELECT carrid, connid FROM sflight ORDER BY carrid ASC"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"ORDER BY ASC failed: {errors}")
    
    def test_order_by_desc(self):
        """Test ORDER BY DESC."""
        sql = "SELECT carrid, connid FROM sflight ORDER BY carrid DESC"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"ORDER BY DESC failed: {errors}")
    
    def test_order_by_multiple(self):
        """Test ORDER BY multiple columns."""
        sql = "SELECT carrid, connid FROM sflight ORDER BY carrid ASC, connid DESC"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Multiple ORDER BY failed: {errors}")
    
    def test_order_by_expression(self):
        """Test ORDER BY with expression."""
        sql = "SELECT carrid, seatsocc FROM sflight ORDER BY seatsocc * 2 DESC"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"ORDER BY expression failed: {errors}")
    
    def test_order_by_case(self):
        """Test ORDER BY with CASE."""
        sql = """SELECT carrid, seatsocc FROM sflight
                 ORDER BY CASE WHEN seatsocc > 200 THEN 1 ELSE 2 END"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"ORDER BY CASE failed: {errors}")
    
    def test_order_by_nulls_first(self):
        """Test ORDER BY with NULLS FIRST."""
        sql = "SELECT carrid, seatsocc FROM sflight ORDER BY seatsocc NULLS FIRST"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"ORDER BY NULLS FIRST failed: {errors}")
    
    def test_order_by_nulls_last(self):
        """Test ORDER BY with NULLS LAST."""
        sql = "SELECT carrid, seatsocc FROM sflight ORDER BY seatsocc NULLS LAST"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"ORDER BY NULLS LAST failed: {errors}")


class TestSetOperations(unittest.TestCase):
    """Test set operations (UNION, INTERSECT, EXCEPT)."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_union(self):
        """Test UNION."""
        sql = """SELECT carrid FROM sflight WHERE carrid = 'AA'
                 UNION
                 SELECT carrid FROM sflight WHERE carrid = 'LH'"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"UNION failed: {errors}")
    
    def test_union_all(self):
        """Test UNION ALL."""
        sql = """SELECT carrid FROM sflight WHERE carrid = 'AA'
                 UNION ALL
                 SELECT carrid FROM sflight WHERE carrid = 'LH'"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"UNION ALL failed: {errors}")
    
    def test_intersect(self):
        """Test INTERSECT."""
        sql = """SELECT carrid FROM sflight
                 INTERSECT
                 SELECT carrid FROM spfli"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"INTERSECT failed: {errors}")
    
    def test_except(self):
        """Test EXCEPT."""
        sql = """SELECT carrid FROM sflight
                 EXCEPT
                 SELECT carrid FROM spfli"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"EXCEPT failed: {errors}")


class TestCTEAndSubqueries(unittest.TestCase):
    """Test Common Table Expressions and subqueries."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = ABAPSQLChecker()
    
    def test_simple_cte(self):
        """Test simple CTE."""
        sql = """WITH carrier_stats AS (
                   SELECT carrid, COUNT(*) as cnt FROM sflight GROUP BY carrid
                 )
                 SELECT * FROM carrier_stats WHERE cnt > 10"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Simple CTE failed: {errors}")
    
    def test_multiple_ctes(self):
        """Test multiple CTEs."""
        sql = """WITH carrier_stats AS (
                   SELECT carrid, COUNT(*) as cnt FROM sflight GROUP BY carrid
                 ),
                 route_stats AS (
                   SELECT carrid, connid, AVG(seatsocc) as avg_seats FROM sflight GROUP BY carrid, connid
                 )
                 SELECT c.carrid, c.cnt, r.avg_seats
                 FROM carrier_stats c
                 JOIN route_stats r ON c.carrid = r.carrid"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Multiple CTEs failed: {errors}")
    
    def test_scalar_subquery(self):
        """Test scalar subquery."""
        sql = """SELECT carrid, seatsocc,
                        (SELECT AVG(seatsocc) FROM sflight) as overall_avg
                 FROM sflight"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Scalar subquery failed: {errors}")
    
    def test_subquery_in_from(self):
        """Test subquery in FROM clause."""
        sql = """SELECT * FROM (
                   SELECT carrid, COUNT(*) as cnt FROM sflight GROUP BY carrid
                 ) AS carrier_stats
                 WHERE cnt > 10"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"FROM subquery failed: {errors}")
    
    def test_correlated_subquery(self):
        """Test correlated subquery."""
        sql = """SELECT carrid, seatsocc FROM sflight f1
                 WHERE seatsocc > (SELECT AVG(seatsocc) FROM sflight f2 WHERE f2.carrid = f1.carrid)"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Correlated subquery failed: {errors}")
    
    def test_exists_subquery(self):
        """Test EXISTS subquery."""
        sql = """SELECT carrid FROM spfli p
                 WHERE EXISTS (SELECT 1 FROM sflight f WHERE f.carrid = p.carrid)"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"EXISTS subquery failed: {errors}")
    
    def test_not_exists_subquery(self):
        """Test NOT EXISTS subquery."""
        sql = """SELECT carrid FROM spfli p
                 WHERE NOT EXISTS (SELECT 1 FROM sflight f WHERE f.carrid = p.carrid)"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"NOT EXISTS subquery failed: {errors}")


def run_all_tests():
    """Run all extended tests and display results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestJoinVariants))
    suite.addTests(loader.loadTestsFromTestCase(TestAggregateFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestWindowFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestDateTimeFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestStringFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestMathFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestOrderByVariants))
    suite.addTests(loader.loadTestsFromTestCase(TestSetOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestCTEAndSubqueries))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 80)
    print("EXTENDED TEST SUITE SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 80)
    
    # Test category breakdown
    print("\nTest Categories:")
    print(f"  - JOIN Variants: 9 tests")
    print(f"  - Aggregate Functions: 10 tests")
    print(f"  - Window Functions: 10 tests")
    print(f"  - Date/Time Functions: 6 tests")
    print(f"  - String Functions: 8 tests")
    print(f"  - Math Functions: 7 tests")
    print(f"  - ORDER BY Variants: 8 tests")
    print(f"  - Set Operations: 4 tests")
    print(f"  - CTEs & Subqueries: 7 tests")
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)

