"""
Test Real Ariba AQL Queries with Pre-processing

This script tests the AQL checker with real production Ariba queries
that use Ariba-specific syntax like INCLUDE INACTIVE and SUBCLASS NONE.
"""

from aql_sql_checker import AQLSQLChecker, preprocess_ariba_aql

# Real Ariba AQL queries from production
REAL_ARIBA_QUERIES = [
    "SELECT cr FROM ariba.sourcing.rfx.RFXDocument AS cr INCLUDE INACTIVE WHERE cr IN (BaseId(:PARAM), BaseId(:PARAM), BaseId(:PARAM), BaseId(:PARAM), BaseId(:PARAM))",
    
    'SELECT g FROM ariba."user".core."Group" AS g WHERE g.Users = BaseId(:PARAM) AND g.IsGlobal = :BOOLEAN',
    
    "SELECT RFXBid FROM ariba.sourcing.rfx.RFXBid AS RFXBid SUBCLASS NONE WHERE RFXBid.ContentDocumentReference.DocumentId = BaseId(:PARAM) AND RFXBid.ContentDocumentReference.DocumentVersion = :NUM AND SubmitFor IN (BaseId(:PARAM)) AND RFXBid.AlternativeStatus = :NUM ORDER BY RFXBid.SubmissionDate DESC",
    
    "SELECT RFXDocument, RFXDocument.Title, RFXDocument.InternalId FROM ariba.sourcing.rfx.RFXDocument AS RFXDocument WHERE RFXDocument.NextVersion IS :NULL AND RFXDocument.Owner = BaseId(:PARAM) ORDER BY RFXDocument.CreateDate DESC",
    
    "SELECT Alternative FROM ariba.sourcing.\"content\".Alternative AS Alternative SUBCLASS NONE WHERE Alternative.ContentDocumentReference.DocumentId = BaseId(:PARAM) AND Alternative.ContentDocumentReference.DocumentVersion = :NUM AND Alternative.AlternativeStatus = :NUM ORDER BY Alternative.SubmissionDate DESC",
]


def test_preprocessing():
    """Test the pre-processing function."""
    print("="*80)
    print("TESTING ARIBA AQL PRE-PROCESSING")
    print("="*80)
    
    test_cases = [
        ("SELECT * FROM table AS t INCLUDE INACTIVE", 
         "SELECT * FROM table AS t"),
        
        ("SELECT * FROM table AS t SUBCLASS NONE WHERE x = 1",
         "SELECT * FROM table AS t WHERE x = 1"),
         
        ("SELECT * FROM table AS t INCLUDE INACTIVE WHERE x = 1",
         "SELECT * FROM table AS t WHERE x = 1"),
    ]
    
    for original, expected in test_cases:
        result = preprocess_ariba_aql(original)
        status = "✅" if result == expected else "❌"
        print(f"\n{status} Test:")
        print(f"  Original: {original}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")


def test_real_queries():
    """Test real Ariba queries."""
    print("\n" + "="*80)
    print("TESTING REAL ARIBA AQL QUERIES")
    print("="*80)
    
    checker = AQLSQLChecker()
    
    for i, sql in enumerate(REAL_ARIBA_QUERIES, 1):
        print(f"\n{'─'*80}")
        print(f"Query #{i}")
        print(f"{'─'*80}")
        print(f"Original: {sql[:100]}...")
        
        # Show what pre-processing does
        clean_sql = preprocess_ariba_aql(sql)
        if clean_sql != sql:
            print(f"Cleaned:  {clean_sql[:100]}...")
        
        # Test with pre-processing (default)
        is_valid, ast, errors = checker.check_syntax(sql, preprocess=True)
        
        if is_valid:
            print(f"✅ VALID (with pre-processing)")
            if ast:
                print(f"   Statement Type: {ast.__class__.__name__}")
                # Try to get table info
                try:
                    tables = [str(t.this) for t in ast.find_all(exp.Table)]
                    if tables:
                        print(f"   Tables: {', '.join(tables[:3])}...")
                except:
                    pass
        else:
            print(f"❌ INVALID")
            for error in errors:
                print(f"   Error: {error}")


def main():
    """Main test runner."""
    print("\n" + "🚀"*40)
    print("ARIBA AQL PRE-PROCESSING TEST SUITE")
    print("🚀"*40 + "\n")
    
    # Test pre-processing function
    test_preprocessing()
    
    # Test real queries
    test_real_queries()
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total Real Ariba Queries Tested: {len(REAL_ARIBA_QUERIES)}")
    print("Pre-processing enabled by default")
    print("Ariba-specific clauses (INCLUDE INACTIVE, SUBCLASS NONE) are stripped")
    print("="*80 + "\n")


if __name__ == "__main__":
    from sqlglot import exp
    main()

