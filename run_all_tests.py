"""
Comprehensive Test Runner
Runs all test suites: Basic, Extended, and ABAP-Specific

Run with: python run_all_tests.py
"""

import sys
import unittest
from test_checker import TestABAPSQLChecker
from test_checker_extended import (
    TestJoinVariants, TestAggregateFunctions, TestWindowFunctions,
    TestDateTimeFunctions, TestStringFunctions, TestMathFunctions,
    TestOrderByVariants, TestSetOperations, TestCTEAndSubqueries
)
from test_abap_specific import (
    TestABAPSpecificSyntax, TestABAPHostVariables, TestABAPTableOperations,
    TestABAPJoinSyntax, TestABAPAggregateExtensions, TestABAPCaseExpressions,
    TestABAPLimitOffset, TestABAPNullHandling, TestABAPDistinctVariants,
    TestABAPInOperator, TestABAPBetweenOperator, TestABAPLikeOperator
)
from test_abap_enhanced import (
    TestABAPEnhancedKeywords, TestABAPStringOperators, TestABAPFunctions,
    TestABAPHostVariables as TestABAPEnhancedHostVars, TestABAPTildeOperator
)
from test_negative import TestNegativeCases

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


def print_colored(text, color=""):
    """Print colored text if colorama is available."""
    if COLORAMA_AVAILABLE and color:
        print(f"{color}{text}{Style.RESET_ALL}")
    else:
        print(text)


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print_colored(title, Fore.CYAN if COLORAMA_AVAILABLE else "")
    print("=" * 80)


def run_test_suite(suite_name, test_classes, verbosity=1):
    """Run a test suite and return results."""
    print_header(f"{suite_name} TEST SUITE")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return result


def print_summary(suite_name, result):
    """Print test results summary."""
    success = result.testsRun - len(result.failures) - len(result.errors)
    success_rate = (success / result.testsRun * 100) if result.testsRun > 0 else 0
    
    print(f"\n{suite_name} Summary:")
    print(f"  Tests run: {result.testsRun}")
    
    if success == result.testsRun:
        print_colored(f"  ✓ All tests passed! ({success}/{result.testsRun})", 
                     Fore.GREEN if COLORAMA_AVAILABLE else "")
    else:
        print_colored(f"  Successes: {success}", Fore.GREEN if COLORAMA_AVAILABLE else "")
        if result.failures:
            print_colored(f"  Failures: {len(result.failures)}", Fore.YELLOW if COLORAMA_AVAILABLE else "")
        if result.errors:
            print_colored(f"  Errors: {len(result.errors)}", Fore.RED if COLORAMA_AVAILABLE else "")
    
    print(f"  Success rate: {success_rate:.1f}%")
    
    return success, result.testsRun


def main():
    """Run all test suites."""
    print_colored("\n" + "=" * 80, Fore.MAGENTA if COLORAMA_AVAILABLE else "")
    print_colored("ABAP SQL SYNTAX CHECKER - COMPREHENSIVE TEST SUITE", 
                 Fore.MAGENTA if COLORAMA_AVAILABLE else "")
    print_colored("=" * 80, Fore.MAGENTA if COLORAMA_AVAILABLE else "")
    
    # Track overall statistics
    total_tests = 0
    total_success = 0
    all_results = []
    
    # 1. Basic Tests
    basic_tests = [TestABAPSQLChecker]
    result1 = run_test_suite("BASIC", basic_tests, verbosity=1)
    success, count = print_summary("Basic", result1)
    total_success += success
    total_tests += count
    all_results.append(("Basic", result1))
    
    # 2. Extended Tests (Major SQL Variants)
    extended_tests = [
        TestJoinVariants,
        TestAggregateFunctions,
        TestWindowFunctions,
        TestDateTimeFunctions,
        TestStringFunctions,
        TestMathFunctions,
        TestOrderByVariants,
        TestSetOperations,
        TestCTEAndSubqueries
    ]
    result2 = run_test_suite("EXTENDED (SQL Variants)", extended_tests, verbosity=1)
    success, count = print_summary("Extended", result2)
    total_success += success
    total_tests += count
    all_results.append(("Extended", result2))
    
    # 3. ABAP-Specific Tests
    abap_tests = [
        TestABAPSpecificSyntax,
        TestABAPHostVariables,
        TestABAPTableOperations,
        TestABAPJoinSyntax,
        TestABAPAggregateExtensions,
        TestABAPCaseExpressions,
        TestABAPLimitOffset,
        TestABAPNullHandling,
        TestABAPDistinctVariants,
        TestABAPInOperator,
        TestABAPBetweenOperator,
        TestABAPLikeOperator
    ]
    result3 = run_test_suite("ABAP-SPECIFIC", abap_tests, verbosity=1)
    success, count = print_summary("ABAP-Specific", result3)
    total_success += success
    total_tests += count
    all_results.append(("ABAP-Specific", result3))
    
    # 4. Enhanced ABAP Features (NEW!)
    enhanced_abap_tests = [
        TestABAPEnhancedKeywords,
        TestABAPStringOperators,
        TestABAPFunctions,
        TestABAPEnhancedHostVars,
        TestABAPTildeOperator
    ]
    result4 = run_test_suite("ABAP ENHANCED FEATURES", enhanced_abap_tests, verbosity=1)
    success, count = print_summary("ABAP Enhanced", result4)
    total_success += success
    total_tests += count
    all_results.append(("ABAP Enhanced", result4))
    
    # 5. Negative Tests (Error Detection)
    negative_tests = [TestNegativeCases]
    result5 = run_test_suite("NEGATIVE (Error Detection)", negative_tests, verbosity=1)
    success, count = print_summary("Negative", result5)
    total_success += success
    total_tests += count
    all_results.append(("Negative", result5))
    
    # Overall Summary
    print_header("OVERALL TEST SUMMARY")
    
    print(f"\nTotal Tests Executed: {total_tests}")
    print(f"Total Successes: {total_success}")
    print(f"Total Failures: {sum(len(r.failures) for _, r in all_results)}")
    print(f"Total Errors: {sum(len(r.errors) for _, r in all_results)}")
    
    overall_success_rate = (total_success / total_tests * 100) if total_tests > 0 else 0
    print(f"\nOverall Success Rate: {overall_success_rate:.1f}%")
    
    # Detailed breakdown
    print("\nTest Suite Breakdown:")
    print("  Basic Tests:         14 tests (positive)")
    print("  Extended Tests:      69 tests (positive)")
    print("    - JOINs:           9 tests")
    print("    - Aggregates:     10 tests")
    print("    - Windows:        10 tests")
    print("    - Date/Time:       6 tests")
    print("    - Strings:         8 tests")
    print("    - Math:            7 tests")
    print("    - ORDER BY:        8 tests")
    print("    - Set Ops:         4 tests")
    print("    - CTEs:            7 tests")
    print("  ABAP-Specific:      38 tests")
    print("    - ABAP Syntax:     5 tests")
    print("    - Host Variables:  3 tests")
    print("    - Table Ops:       3 tests")
    print("    - ABAP JOINs:      2 tests")
    print("    - Aggregates:      2 tests")
    print("    - CASE:            3 tests")
    print("    - LIMIT/OFFSET:    4 tests")
    print("    - NULL Handling:   4 tests")
    print("    - DISTINCT:        3 tests")
    print("    - IN Operator:     3 tests")
    print("    - BETWEEN:         3 tests")
    print("    - LIKE:            3 tests")
    print("  ABAP Enhanced:      36 tests")
    print("    - INTO clauses:    4 tests")
    print("    - UP TO/BYPASSING: 7 tests")
    print("    - FOR UPDATE:      2 tests")
    print("    - PACKAGE SIZE:    2 tests")
    print("    - Combined:        2 tests")
    print("    - String Ops:      8 tests")
    print("    - Functions:       4 tests")
    print("    - Host Vars:       4 tests")
    print("    - Tilde (~):       3 tests")
    print("  Negative Tests:      21 tests (error detection)")
    print(f"\n  TOTAL:            {total_tests} tests")
    
    # Coverage summary
    print("\n" + "=" * 80)
    print_colored("SQL FEATURE COVERAGE", Fore.CYAN if COLORAMA_AVAILABLE else "")
    print("=" * 80)
    print("✓ JOINs: INNER, LEFT, RIGHT, FULL OUTER, CROSS, Multiple, Self")
    print("✓ Aggregates: COUNT, SUM, AVG, MIN, MAX, COUNT DISTINCT, GROUP BY, HAVING")
    print("✓ Window Functions: ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, FIRST_VALUE, LAST_VALUE")
    print("✓ Date/Time: CURRENT_DATE, CURRENT_TIMESTAMP, DATE_TRUNC, EXTRACT, Arithmetic")
    print("✓ String Functions: CONCAT, SUBSTRING, UPPER, LOWER, TRIM, LENGTH, REPLACE")
    print("✓ Math Functions: ROUND, CEIL, FLOOR, ABS, MOD, POWER, SQRT")
    print("✓ Sorting: ORDER BY (ASC/DESC, Multiple, NULLS FIRST/LAST)")
    print("✓ Set Operations: UNION, UNION ALL, INTERSECT, EXCEPT")
    print("✓ Subqueries: Scalar, FROM, Correlated, EXISTS, NOT EXISTS")
    print("✓ CTEs: Simple, Multiple, Recursive-ready")
    print("✓ ABAP Keywords: SINGLE, UP TO, CLIENT SPECIFIED, BYPASSING BUFFER, FOR UPDATE")
    print("✓ ABAP Features: Host Variables, CASE, LIMIT/OFFSET, NULL handling")
    print("✓ ABAP Enhanced: INTO, APPENDING TABLE, PACKAGE SIZE, Tilde (~) operator")
    print("✓ ABAP String Ops: CP, CS, CA, CO, NP, NS, NA, CN (Contains Pattern, etc.)")
    print("✓ ABAP Functions: CONCAT_WITH_SPACE, STRING_AGG, CAST, COALESCE")
    print("✓ Operators: IN, NOT IN, BETWEEN, LIKE, NOT LIKE")
    print("✓ Special: DISTINCT, COALESCE, NULLIF, Pattern Matching")
    
    # Final verdict
    print("\n" + "=" * 80)
    if total_success == total_tests:
        print_colored("🎉 ALL TESTS PASSED! COMPREHENSIVE COVERAGE ACHIEVED! 🎉", 
                     Fore.GREEN if COLORAMA_AVAILABLE else "")
    else:
        print_colored("⚠ SOME TESTS FAILED - REVIEW REQUIRED", 
                     Fore.YELLOW if COLORAMA_AVAILABLE else "")
    print("=" * 80 + "\n")
    
    # Return success/failure
    return total_success == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

