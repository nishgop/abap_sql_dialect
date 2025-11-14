"""
Unified Test Runner for ABAP and AQL SQL Dialects

This script runs all test suites for both ABAP SQL and AQL (Ariba Query Language) dialects,
providing comprehensive validation and a detailed summary of results.

Author: Generated with Claude
License: MIT
"""

import unittest
import sys
from io import StringIO

# Import ABAP test modules
from test_basic import TestBasicSQLSyntax
from test_extended import (
    TestJoins, TestAggregates, TestWindowFunctions,
    TestSubqueries, TestCase, TestUnion
)
from test_abap_specific import (
    TestABAPSpecificSyntax, TestABAPHostVariables, TestABAPMultipleStatements
)
from test_negative import TestNegativeTests
from test_abap_enhanced import (
    TestABAPEnhancedKeywords, TestABAPStringOperators, TestABAPFunctions,
    TestABAPHostVariables as TestABAPEnhancedHostVars, TestABAPTildeOperator
)

# Import AQL test modules
from test_aql_basic import (
    TestBasicAQLSyntax, TestAQLInsertUpdateDelete, TestAQLOrderBy, TestAQLQueryAnalysis
)
from test_aql_extended import (
    TestAQLJoins, TestAQLAggregates, TestAQLDateFunctions, TestAQLStringFunctions,
    TestAQLMathFunctions, TestAQLConditionals, TestAQLSubqueries, TestAQLUnion
)
from test_aql_specific import (
    TestAQLObjectReferences, TestAQLDotNotation, TestAQLComplexQueries, TestAQLBatchProcessing
)
from test_aql_negative import (
    TestAQLNegativeSyntax, TestAQLNegativeJoins, TestAQLNegativeAggregates,
    TestAQLNegativeDML, TestAQLNegativeFunctions, TestAQLNegativeSubqueries,
    TestAQLNegativeComplexErrors
)


def run_test_suite(name: str, test_classes: list, verbosity: int = 1) -> unittest.TestResult:
    """
    Run a test suite and return the result.
    
    Args:
        name: Name of the test suite
        test_classes: List of test classes to run
        verbosity: Verbosity level (0=quiet, 1=normal, 2=verbose)
        
    Returns:
        TestResult object
    """
    print(f"\n{'='*80}")
    print(f"Running {name}")
    print(f"{'='*80}\n")
    
    suite = unittest.TestSuite()
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return result


def print_summary(name: str, result: unittest.TestResult) -> tuple:
    """
    Print a summary of test results.
    
    Args:
        name: Name of the test suite
        result: TestResult object
        
    Returns:
        Tuple of (passed_count, total_count)
    """
    total = result.testsRun
    failed = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)
    passed = total - failed - errors - skipped
    
    print(f"\n{name}: {passed}/{total} passed", end="")
    if failed > 0:
        print(f", {failed} failed", end="")
    if errors > 0:
        print(f", {errors} errors", end="")
    if skipped > 0:
        print(f", {skipped} skipped", end="")
    print()
    
    return passed, total


def main():
    """Main test runner."""
    print("\n" + "="*80)
    print("SQL DIALECT TEST SUITE - ABAP & AQL")
    print("="*80)
    print("\nRunning comprehensive tests for ABAP SQL and Ariba Query Language (AQL) dialects")
    print(f"{'='*80}\n")
    
    all_results = []
    total_tests = 0
    total_success = 0
    
    # ========================================================================
    # ABAP SQL TESTS
    # ========================================================================
    print("\n" + "▓"*80)
    print("▓" + " "*30 + "ABAP SQL TESTS" + " "*34 + "▓")
    print("▓"*80 + "\n")
    
    # 1. ABAP Basic Tests
    basic_tests = [TestBasicSQLSyntax]
    result1 = run_test_suite("ABAP BASIC SYNTAX", basic_tests, verbosity=1)
    success, count = print_summary("ABAP Basic", result1)
    total_success += success
    total_tests += count
    all_results.append(("ABAP Basic", result1))
    
    # 2. ABAP Extended SQL Tests
    extended_tests = [
        TestJoins,
        TestAggregates,
        TestWindowFunctions,
        TestSubqueries,
        TestCase,
        TestUnion
    ]
    result2 = run_test_suite("ABAP EXTENDED SQL", extended_tests, verbosity=1)
    success, count = print_summary("ABAP Extended", result2)
    total_success += success
    total_tests += count
    all_results.append(("ABAP Extended", result2))
    
    # 3. ABAP-Specific Features
    abap_specific_tests = [
        TestABAPSpecificSyntax,
        TestABAPHostVariables,
        TestABAPMultipleStatements
    ]
    result3 = run_test_suite("ABAP-SPECIFIC FEATURES", abap_specific_tests, verbosity=1)
    success, count = print_summary("ABAP Specific", result3)
    total_success += success
    total_tests += count
    all_results.append(("ABAP Specific", result3))
    
    # 4. ABAP Enhanced Features
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
    
    # 5. ABAP Negative Tests
    negative_tests = [TestNegativeTests]
    result5 = run_test_suite("ABAP NEGATIVE TESTS (Error Detection)", negative_tests, verbosity=1)
    success, count = print_summary("ABAP Negative", result5)
    total_success += success
    total_tests += count
    all_results.append(("ABAP Negative", result5))
    
    # ========================================================================
    # AQL TESTS
    # ========================================================================
    print("\n" + "▓"*80)
    print("▓" + " "*20 + "ARIBA QUERY LANGUAGE (AQL) TESTS" + " "*26 + "▓")
    print("▓"*80 + "\n")
    
    # 6. AQL Basic Tests
    aql_basic_tests = [
        TestBasicAQLSyntax,
        TestAQLInsertUpdateDelete,
        TestAQLOrderBy,
        TestAQLQueryAnalysis
    ]
    result6 = run_test_suite("AQL BASIC SYNTAX", aql_basic_tests, verbosity=1)
    success, count = print_summary("AQL Basic", result6)
    total_success += success
    total_tests += count
    all_results.append(("AQL Basic", result6))
    
    # 7. AQL Extended Tests
    aql_extended_tests = [
        TestAQLJoins,
        TestAQLAggregates,
        TestAQLDateFunctions,
        TestAQLStringFunctions,
        TestAQLMathFunctions,
        TestAQLConditionals,
        TestAQLSubqueries,
        TestAQLUnion
    ]
    result7 = run_test_suite("AQL EXTENDED FEATURES", aql_extended_tests, verbosity=1)
    success, count = print_summary("AQL Extended", result7)
    total_success += success
    total_tests += count
    all_results.append(("AQL Extended", result7))
    
    # 8. AQL-Specific Features
    aql_specific_tests = [
        TestAQLObjectReferences,
        TestAQLDotNotation,
        TestAQLComplexQueries,
        TestAQLBatchProcessing
    ]
    result8 = run_test_suite("AQL-SPECIFIC FEATURES", aql_specific_tests, verbosity=1)
    success, count = print_summary("AQL Specific", result8)
    total_success += success
    total_tests += count
    all_results.append(("AQL Specific", result8))
    
    # 9. AQL Negative Tests
    aql_negative_tests = [
        TestAQLNegativeSyntax,
        TestAQLNegativeJoins,
        TestAQLNegativeAggregates,
        TestAQLNegativeDML,
        TestAQLNegativeFunctions,
        TestAQLNegativeSubqueries,
        TestAQLNegativeComplexErrors
    ]
    result9 = run_test_suite("AQL NEGATIVE TESTS (Error Detection)", aql_negative_tests, verbosity=1)
    success, count = print_summary("AQL Negative", result9)
    total_success += success
    total_tests += count
    all_results.append(("AQL Negative", result9))
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print("\n" + "="*80)
    print("FINAL TEST SUMMARY")
    print("="*80)
    
    print("\nABAP SQL Test Suites:")
    for i in range(5):
        name, result = all_results[i]
        passed, total = print_summary(f"  {name}", result)
    
    print("\nAQL Test Suites:")
    for i in range(5, 9):
        name, result = all_results[i]
        passed, total = print_summary(f"  {name}", result)
    
    print(f"\n{'='*80}")
    print(f"OVERALL: {total_success}/{total_tests} tests passed")
    print(f"Success Rate: {(total_success/total_tests*100):.1f}%")
    print(f"{'='*80}\n")
    
    # Return exit code based on results
    if total_success == total_tests:
        print("✅ ALL TESTS PASSED!")
        return 0
    else:
        print(f"❌ {total_tests - total_success} TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())

