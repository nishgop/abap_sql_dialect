"""
AQL-Specific Features Tests

This module tests Ariba-specific features that are unique to AQL,
including dot notation for object references, Ariba objects, and
Ariba-specific syntax patterns.

Author: Generated with Claude
License: MIT
"""

import unittest
from aql_sql_checker import AQLSQLChecker
from sqlglot import exp


class TestAQLObjectReferences(unittest.TestCase):
    """Test AQL object reference patterns."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_document_object(self):
        """Test Document object references."""
        sql = """SELECT 
                    Document.DocumentId,
                    Document.Title,
                    Document.Status,
                    Document.Amount
                 FROM Document"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_project_object(self):
        """Test Project object references."""
        sql = """SELECT 
                    Project.ProjectId,
                    Project.ProjectName,
                    Project.Status
                 FROM Project"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_supplier_object(self):
        """Test Supplier object references."""
        sql = """SELECT 
                    Supplier.SupplierId,
                    Supplier.Name,
                    Supplier.Region
                 FROM Supplier"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_invoice_object(self):
        """Test Invoice object references."""
        sql = """SELECT 
                    Invoice.InvoiceId,
                    Invoice.InvoiceNumber,
                    Invoice.Amount,
                    Invoice.Status
                 FROM Invoice"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_contract_object(self):
        """Test Contract object references."""
        sql = """SELECT 
                    Contract.ContractId,
                    Contract.ContractNumber,
                    Contract.ContractAmount
                 FROM Contract"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_requisition_object(self):
        """Test Requisition object references."""
        sql = """SELECT 
                    Requisition.RequisitionId,
                    Requisition.RequisitionNumber,
                    Requisition.TotalAmount
                 FROM Requisition"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_order_object(self):
        """Test Order object references."""
        sql = """SELECT 
                    Order.OrderId,
                    Order.OrderNumber,
                    Order.OrderAmount
                 FROM Order"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestAQLDotNotation(unittest.TestCase):
    """Test AQL dot notation for nested field access."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_simple_dot_notation(self):
        """Test simple dot notation."""
        sql = "SELECT Document.DocumentId FROM Document"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_multiple_dot_fields(self):
        """Test multiple fields with dot notation."""
        sql = """SELECT 
                    Document.DocumentId,
                    Document.Title,
                    Document.Status,
                    Document.Amount,
                    Document.CreatedDate
                 FROM Document"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_dot_notation_in_where(self):
        """Test dot notation in WHERE clause."""
        sql = "SELECT * FROM Document WHERE Document.Status = 'Active'"
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_dot_notation_in_join(self):
        """Test dot notation in JOIN condition."""
        sql = """SELECT * FROM Document d
                 INNER JOIN Project p ON d.ProjectId = p.ProjectId
                 WHERE Document.Status = 'Active'"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestAQLComplexQueries(unittest.TestCase):
    """Test complex AQL query patterns."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_complex_with_all_clauses(self):
        """Test complex query with all major clauses."""
        sql = """SELECT 
                    Project.ProjectName,
                    COUNT(DISTINCT Document.DocumentId) as DocCount,
                    SUM(Document.Amount) as TotalAmount,
                    AVG(Document.Amount) as AvgAmount
                 FROM Project
                 INNER JOIN Document ON Project.ProjectId = Document.ProjectId
                 WHERE Project.Status = 'Active'
                   AND Document.Amount > 1000
                 GROUP BY Project.ProjectName
                 HAVING COUNT(*) > 5
                 ORDER BY TotalAmount DESC"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_nested_aggregates_with_case(self):
        """Test nested aggregates with CASE."""
        sql = """SELECT 
                    Supplier.Region,
                    SUM(CASE WHEN Invoice.Status = 'Paid' THEN Invoice.Amount ELSE 0 END) as PaidAmount,
                    SUM(CASE WHEN Invoice.Status = 'Pending' THEN Invoice.Amount ELSE 0 END) as PendingAmount
                 FROM Invoice
                 GROUP BY Supplier.Region"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")
    
    def test_multiple_joins_with_subquery(self):
        """Test multiple JOINs with subquery."""
        sql = """SELECT 
                    d.DocumentId,
                    p.ProjectName,
                    s.Name
                 FROM Document d
                 INNER JOIN Project p ON d.ProjectId = p.ProjectId
                 INNER JOIN Supplier s ON d.SupplierId = s.SupplierId
                 WHERE d.Amount > (
                     SELECT AVG(Amount) FROM Document WHERE Status = 'Active'
                 )"""
        is_valid, ast, errors = self.checker.check_syntax(sql)
        self.assertTrue(is_valid, f"Should be valid, errors: {errors}")


class TestAQLBatchProcessing(unittest.TestCase):
    """Test batch processing of multiple queries."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = AQLSQLChecker()
    
    def test_batch_check_multiple_queries(self):
        """Test batch checking multiple queries."""
        queries = [
            "SELECT * FROM Document WHERE Status = 'Active'",
            "SELECT COUNT(*) FROM Invoice",
            "SELECT * FROM Supplier WHERE Region = 'US'",
        ]
        results = self.checker.batch_check(queries)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result['is_valid'])
    
    def test_batch_with_valid_and_invalid(self):
        """Test batch with mix of valid and invalid queries."""
        queries = [
            "SELECT * FROM Document WHERE Status = 'Active'",
            "SELECT WHERE Status = 'Active'",  # Invalid: missing FROM
            "SELECT COUNT(*) FROM Invoice",
        ]
        results = self.checker.batch_check(queries)
        
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0]['is_valid'])
        self.assertFalse(results[1]['is_valid'])
        self.assertTrue(results[2]['is_valid'])


if __name__ == '__main__':
    unittest.main(verbosity=2)

