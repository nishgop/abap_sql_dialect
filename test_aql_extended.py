"""
Extended AQL (Ariba Query Language) SQL Syntax Tests

This module contains extended tests for advanced AQL features including JOINs,
aggregates, date/time functions, string functions, subqueries, and complex patterns.

Author: Generated with Claude
License: MIT
"""

import unittest
from aql_sql_checker import AQLSQLChecker
from sqlglot import exp


class TestAQLJoins(unittest.TestCase):
    """Test JOIN operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_inner_join(self):
        """Test INNER JOIN."""
        sql = """SELECT d.DocumentId, p.ProjectName
                 FROM Document d
                 INNER JOIN Project p ON d.ProjectId = p.ProjectId"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_left_join(self):
        """Test LEFT OUTER JOIN."""
        sql = """SELECT s.Name, i.Amount
                 FROM Supplier s
                 LEFT JOIN Invoice i ON s.SupplierId = i.SupplierId"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_right_join(self):
        """Test RIGHT OUTER JOIN."""
        sql = """SELECT * FROM Document d
                 RIGHT JOIN Project p ON d.ProjectId = p.ProjectId"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_cross_join(self):
        """Test CROSS JOIN (no ON required)."""
        sql = "SELECT * FROM Document CROSS JOIN Project"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_multiple_joins(self):
        """Test multiple JOINs."""
        sql = """SELECT d.DocumentId, p.ProjectName, s.Name
                 FROM Document d
                 INNER JOIN Project p ON d.ProjectId = p.ProjectId
                 INNER JOIN Supplier s ON d.SupplierId = s.SupplierId"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_join_without_on(self):
        """Test that JOIN without ON (except CROSS) is invalid."""
        sql = "SELECT * FROM Document d JOIN Project p"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertFalse(is_valid, "Should be invalid: JOIN without ON")


class TestAQLAggregates(unittest.TestCase):
    """Test aggregate functions and GROUP BY."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_count_all(self):
        """Test COUNT(*)."""
        sql = "SELECT COUNT(*) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_count_distinct(self):
        """Test COUNT DISTINCT."""
        sql = "SELECT COUNT(DISTINCT Supplier.SupplierId) FROM Invoice"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_sum(self):
        """Test SUM aggregate."""
        sql = "SELECT SUM(Invoice.Amount) FROM Invoice"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_avg(self):
        """Test AVG aggregate."""
        sql = "SELECT AVG(Document.Amount) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_min_max(self):
        """Test MIN and MAX aggregates."""
        sql = "SELECT MIN(Amount), MAX(Amount) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_group_by(self):
        """Test GROUP BY clause."""
        sql = "SELECT Status, COUNT(*) FROM Document GROUP BY Status"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_group_by_multiple(self):
        """Test GROUP BY with multiple columns."""
        sql = "SELECT Status, Type, COUNT(*) FROM Document GROUP BY Status, Type"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_having(self):
        """Test HAVING clause."""
        sql = """SELECT Status, COUNT(*) as cnt
                 FROM Document
                 GROUP BY Status
                 HAVING COUNT(*) > 5"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestAQLDateFunctions(unittest.TestCase):
    """Test date and time functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_formatdate(self):
        """Test FORMATDATE function."""
        sql = "SELECT FORMATDATE(Document.CreatedDate, 'yyyy-MM-dd') FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_formattimestamp(self):
        """Test FORMATTIMESTAMP function."""
        sql = "SELECT FORMATTIMESTAMP(Document.CreatedDate, 'yyyy-MM-dd HH:mm:ss') FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_year_month_day(self):
        """Test YEAR, MONTH, DAY functions."""
        sql = """SELECT 
                    YEAR(CreatedDate) as Year,
                    MONTH(CreatedDate) as Month,
                    DAY(CreatedDate) as Day
                 FROM Document"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_adddays(self):
        """Test ADDDAYS function."""
        sql = "SELECT ADDDAYS(Document.CreatedDate, 30) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_addmonths(self):
        """Test ADDMONTHS function."""
        sql = "SELECT ADDMONTHS(Document.CreatedDate, 3) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_datediff(self):
        """Test DATEDIFF function."""
        sql = "SELECT DATEDIFF('day', StartDate, EndDate) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_getdate(self):
        """Test GETDATE function."""
        sql = "SELECT * FROM Document WHERE CreatedDate < GETDATE()"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestAQLStringFunctions(unittest.TestCase):
    """Test string functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_stringconcat(self):
        """Test STRINGCONCAT function."""
        sql = "SELECT STRINGCONCAT(FirstName, ' ', LastName) FROM Supplier"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_substring(self):
        """Test SUBSTRING function."""
        sql = "SELECT SUBSTRING(Title, 1, 50) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_charindex(self):
        """Test CHARINDEX function."""
        sql = "SELECT CHARINDEX('Invoice', Title) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_len(self):
        """Test LEN function."""
        sql = "SELECT LEN(Title) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_replace(self):
        """Test REPLACE function."""
        sql = "SELECT REPLACE(Title, 'Old', 'New') FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_trim(self):
        """Test TRIM function."""
        sql = "SELECT TRIM(Name) FROM Supplier"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_upper_lower(self):
        """Test UPPER and LOWER functions."""
        sql = "SELECT UPPER(Name), LOWER(Name) FROM Supplier"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestAQLMathFunctions(unittest.TestCase):
    """Test math functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_round(self):
        """Test ROUND function."""
        sql = "SELECT ROUND(Amount, 2) FROM Invoice"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_ceiling_floor(self):
        """Test CEILING and FLOOR functions."""
        sql = "SELECT CEILING(Amount), FLOOR(Amount) FROM Invoice"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_abs(self):
        """Test ABS function."""
        sql = "SELECT ABS(Amount) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_power(self):
        """Test POWER function."""
        sql = "SELECT POWER(Amount, 2) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_sqrt(self):
        """Test SQRT function."""
        sql = "SELECT SQRT(Amount) FROM Document WHERE Amount >= 0"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestAQLConditionals(unittest.TestCase):
    """Test conditional expressions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_case_simple(self):
        """Test simple CASE expression."""
        sql = """SELECT 
                    CASE 
                        WHEN Amount > 1000 THEN 'High'
                        ELSE 'Low'
                    END as Category
                 FROM Document"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_case_multiple(self):
        """Test CASE with multiple WHEN clauses."""
        sql = """SELECT 
                    CASE 
                        WHEN Amount > 10000 THEN 'Very High'
                        WHEN Amount > 5000 THEN 'High'
                        WHEN Amount > 1000 THEN 'Medium'
                        ELSE 'Low'
                    END as Category
                 FROM Document"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_iif(self):
        """Test IIF function."""
        sql = "SELECT IIF(Amount > 1000, 'High', 'Low') FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_isnull(self):
        """Test ISNULL function."""
        sql = "SELECT ISNULL(Description, 'No Description') FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_nullif(self):
        """Test NULLIF function."""
        sql = "SELECT NULLIF(Amount, 0) FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestAQLSubqueries(unittest.TestCase):
    """Test subqueries."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_subquery_in_where(self):
        """Test subquery in WHERE clause."""
        sql = """SELECT * FROM Document
                 WHERE Amount > (SELECT AVG(Amount) FROM Document)"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_subquery_with_in(self):
        """Test subquery with IN."""
        sql = """SELECT * FROM Supplier
                 WHERE SupplierId IN (
                     SELECT DISTINCT SupplierId FROM Invoice WHERE Amount > 1000
                 )"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_subquery_in_select(self):
        """Test subquery in SELECT clause."""
        sql = """SELECT 
                    DocumentId,
                    (SELECT COUNT(*) FROM Invoice) as TotalInvoices
                 FROM Document"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_exists(self):
        """Test EXISTS subquery."""
        sql = """SELECT * FROM Supplier
                 WHERE EXISTS (
                     SELECT 1 FROM Invoice WHERE SupplierId = Supplier.SupplierId
                 )"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_not_exists(self):
        """Test NOT EXISTS subquery."""
        sql = """SELECT * FROM Project
                 WHERE NOT EXISTS (
                     SELECT 1 FROM Document WHERE ProjectId = Project.ProjectId
                 )"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestAQLUnion(unittest.TestCase):
    """Test UNION operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_union(self):
        """Test UNION."""
        sql = """SELECT DocumentId as Id FROM Document
                 UNION
                 SELECT InvoiceId as Id FROM Invoice"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_union_all(self):
        """Test UNION ALL."""
        sql = """SELECT Name FROM Supplier WHERE Status = 'Active'
                 UNION ALL
                 SELECT Name FROM Supplier WHERE Status = 'Pending'"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


if __name__ == '__main__':
    unittest.main(verbosity=2)

