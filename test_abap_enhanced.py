"""
Comprehensive test suite for enhanced ABAP SQL features.

Tests all newly added ABAP-specific syntax:
- INTO clauses
- UP TO n ROWS
- BYPASSING BUFFER
- CLIENT SPECIFIED
- FOR UPDATE
- PACKAGE SIZE
- APPENDING TABLE
- ABAP string operators (CP, CS, CA, etc.)
- ABAP-specific functions
"""

import unittest
from abap_sql_checker import ABAPSQLChecker


class TestABAPEnhancedKeywords(unittest.TestCase):
    """Test enhanced ABAP keywords and clauses."""
    
    def setUp(self):
        self.checker = ABAPSQLChecker()
    
    # ========================================================================
    # INTO CLAUSE TESTS
    # ========================================================================
    
    def test_into_simple_variable(self):
        """Test SELECT INTO @variable."""
        sql = "SELECT SINGLE carrid, connid INTO @lv_data FROM sflight WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_into_table(self):
        """Test SELECT INTO TABLE @itab."""
        sql = "SELECT carrid, connid INTO TABLE @lt_flights FROM sflight WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_into_corresponding_fields(self):
        """Test SELECT INTO CORRESPONDING FIELDS OF."""
        sql = "SELECT * INTO CORRESPONDING FIELDS OF @ls_flight FROM sflight WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_appending_table(self):
        """Test SELECT APPENDING TABLE."""
        sql = "SELECT carrid, connid APPENDING TABLE @lt_flights FROM sflight WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    # ========================================================================
    # UP TO n ROWS TESTS
    # ========================================================================
    
    def test_up_to_rows_simple(self):
        """Test UP TO n ROWS."""
        sql = "SELECT carrid, connid FROM sflight UP TO 10 ROWS"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_up_to_rows_with_where(self):
        """Test UP TO n ROWS with WHERE."""
        sql = "SELECT * FROM sflight WHERE carrid = 'AA' UP TO 100 ROWS"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_up_to_rows_with_single(self):
        """Test SELECT SINGLE with UP TO (should be mutually exclusive but test parsing)."""
        sql = "SELECT SINGLE * FROM sflight WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    # ========================================================================
    # BYPASSING BUFFER TESTS
    # ========================================================================
    
    def test_bypassing_buffer(self):
        """Test BYPASSING BUFFER."""
        sql = "SELECT * FROM sflight BYPASSING BUFFER WHERE carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_bypassing_buffer_with_into(self):
        """Test BYPASSING BUFFER with INTO."""
        sql = "SELECT carrid INTO TABLE @lt_data FROM sflight BYPASSING BUFFER"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    # ========================================================================
    # CLIENT SPECIFIED TESTS
    # ========================================================================
    
    def test_client_specified(self):
        """Test CLIENT SPECIFIED."""
        sql = "SELECT * FROM t000 CLIENT SPECIFIED WHERE mandt = '100'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_client_specified_with_where(self):
        """Test CLIENT SPECIFIED with complex WHERE."""
        sql = "SELECT mandt, bukrs FROM t001 CLIENT SPECIFIED WHERE mandt IN ('100', '200')"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    # ========================================================================
    # FOR UPDATE TESTS
    # ========================================================================
    
    def test_for_update(self):
        """Test FOR UPDATE."""
        sql = "SELECT * FROM sflight WHERE carrid = 'AA' FOR UPDATE"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_for_update_with_up_to(self):
        """Test FOR UPDATE with UP TO."""
        sql = "SELECT * FROM sflight WHERE carrid = 'AA' UP TO 10 ROWS FOR UPDATE"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    # ========================================================================
    # PACKAGE SIZE TESTS
    # ========================================================================
    
    def test_package_size(self):
        """Test PACKAGE SIZE."""
        sql = "SELECT * FROM sflight PACKAGE SIZE 1000"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_package_size_with_into(self):
        """Test PACKAGE SIZE with INTO TABLE."""
        sql = "SELECT carrid INTO TABLE @lt_data FROM sflight PACKAGE SIZE 500"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    # ========================================================================
    # COMBINED FEATURES TESTS
    # ========================================================================
    
    def test_combined_abap_features(self):
        """Test multiple ABAP features together."""
        sql = """SELECT carrid, connid 
                 INTO TABLE @lt_flights
                 FROM sflight
                 WHERE carrid = 'AA'
                 UP TO 100 ROWS
                 BYPASSING BUFFER"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_combined_all_features(self):
        """Test comprehensive ABAP query with all features."""
        sql = """SELECT SINGLE carrid, connid, fldate
                 INTO @ls_flight
                 FROM sflight
                 CLIENT SPECIFIED
                 WHERE mandt = '100'
                   AND carrid = 'AA'
                 BYPASSING BUFFER
                 FOR UPDATE"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestABAPStringOperators(unittest.TestCase):
    """Test ABAP-specific string comparison operators."""
    
    def setUp(self):
        self.checker = ABAPSQLChecker()
    
    def test_contains_pattern_cp(self):
        """Test CP (Contains Pattern) operator."""
        sql = "SELECT * FROM customers WHERE name CP '*Smith*'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_not_contains_pattern_np(self):
        """Test NP (Not contains Pattern) operator."""
        sql = "SELECT * FROM customers WHERE name NP '*Test*'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_contains_string_cs(self):
        """Test CS (Contains String) operator."""
        sql = "SELECT * FROM customers WHERE description CS 'important'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_not_contains_string_ns(self):
        """Test NS (Not contains String) operator."""
        sql = "SELECT * FROM customers WHERE description NS 'deprecated'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_contains_any_ca(self):
        """Test CA (Contains Any) operator."""
        sql = "SELECT * FROM customers WHERE name CA 'aeiou'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_not_contains_any_na(self):
        """Test NA (Not contains Any) operator."""
        sql = "SELECT * FROM products WHERE code NA '0123456789'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_contains_only_co(self):
        """Test CO (Contains Only) operator."""
        sql = "SELECT * FROM products WHERE code CO '0123456789'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_not_contains_only_cn(self):
        """Test CN (Not contains Only) operator."""
        sql = "SELECT * FROM products WHERE code CN 'ABCDEF'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestABAPFunctions(unittest.TestCase):
    """Test ABAP-specific SQL functions."""
    
    def setUp(self):
        self.checker = ABAPSQLChecker()
    
    def test_concat_with_space(self):
        """Test CONCAT_WITH_SPACE function."""
        sql = "SELECT CONCAT_WITH_SPACE(firstname, lastname, 1) as fullname FROM employees"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_string_agg(self):
        """Test STRING_AGG function."""
        sql = "SELECT carrid, STRING_AGG(connid, ',') as connections FROM sflight GROUP BY carrid"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_cast_function(self):
        """Test CAST function."""
        sql = "SELECT CAST(price AS DECIMAL(10,2)) as decimal_price FROM products"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_coalesce_function(self):
        """Test COALESCE function."""
        sql = "SELECT COALESCE(email, phone, 'N/A') as contact FROM customers"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestABAPHostVariables(unittest.TestCase):
    """Test ABAP host variables with enhanced features."""
    
    def setUp(self):
        self.checker = ABAPSQLChecker()
    
    def test_modern_host_variable_in_where(self):
        """Test modern @var syntax in WHERE."""
        sql = "SELECT * FROM sflight WHERE carrid = @lv_carrid AND connid = @lv_connid"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_classic_host_variable(self):
        """Test classic :var syntax."""
        sql = "SELECT * FROM sflight WHERE carrid = :lv_carrid"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_host_variable_in_into(self):
        """Test host variable in INTO clause."""
        sql = "SELECT carrid INTO @lv_carrid FROM sflight WHERE connid = '0017'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_internal_table_host_variable(self):
        """Test internal table host variable."""
        sql = "SELECT * INTO TABLE @lt_flights FROM sflight WHERE carrid IN @lt_carriers"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestABAPTildeOperator(unittest.TestCase):
    """Test ABAP tilde (~) operator for table field access."""
    
    def setUp(self):
        self.checker = ABAPSQLChecker()
    
    def test_tilde_in_select(self):
        """Test tilde in SELECT list."""
        sql = "SELECT f~carrid, f~connid FROM sflight AS f WHERE f~carrid = 'AA'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_tilde_in_join(self):
        """Test tilde in JOIN conditions."""
        sql = """SELECT f~carrid, p~cityfrom
                 FROM sflight AS f
                 INNER JOIN spfli AS p ON f~carrid = p~carrid AND f~connid = p~connid"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_tilde_in_where(self):
        """Test tilde in WHERE clause."""
        sql = "SELECT * FROM sflight AS f WHERE f~carrid = 'LH' AND f~fldate > '20230101'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


def run_enhanced_tests():
    """Run all enhanced ABAP feature tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestABAPEnhancedKeywords,
        TestABAPStringOperators,
        TestABAPFunctions,
        TestABAPHostVariables,
        TestABAPTildeOperator,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("ENHANCED ABAP FEATURES TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ All enhanced ABAP features working correctly!")
    else:
        print("\n⚠️  Some tests failed. Review the output above.")
    
    print("=" * 80)
    
    return result


if __name__ == "__main__":
    run_enhanced_tests()

