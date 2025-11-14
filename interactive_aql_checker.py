"""
Interactive AQL (Ariba Query Language) SQL Syntax Checker

This script provides an interactive command-line interface for checking AQL SQL syntax.
"""

import sys
from aql_sql_checker import AQLSQLChecker, print_analysis
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


def print_colored(text: str, color: str = ""):
    """Print colored text if colorama is available."""
    if COLORAMA_AVAILABLE and color:
        print(f"{color}{text}{Style.RESET_ALL}")
    else:
        print(text)


def print_menu():
    """Print the interactive menu."""
    print("\n" + "=" * 70)
    print_colored("AQL SQL Syntax Checker - Interactive Mode", Fore.CYAN if COLORAMA_AVAILABLE else "")
    print("=" * 70)
    print("\nOptions:")
    print("  1. Check SQL syntax")
    print("  2. Format SQL statement")
    print("  3. Load SQL from file")
    print("  4. Run example queries")
    print("  5. Help")
    print("  6. Exit")
    print()


def get_multiline_input(prompt: str = "Enter SQL (end with empty line or ';'):\n") -> str:
    """Get multiline SQL input from user."""
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
            # End on empty line or line with just ';'
            if line.strip() == '' or line.strip() == ';':
                break
            lines.append(line)
        except EOFError:
            break
    
    sql = '\n'.join(lines)
    # Remove trailing semicolon if present (we'll add it back if needed)
    sql = sql.rstrip(';').strip()
    return sql


def check_sql_interactive(checker: AQLSQLChecker):
    """Interactive SQL checking."""
    sql = get_multiline_input()
    if not sql.strip():
        print_colored("No SQL provided.", Fore.YELLOW if COLORAMA_AVAILABLE else "")
        return
    
    analysis = checker.analyze_query(sql)
    print_analysis(analysis)


def format_sql_interactive(checker: AQLSQLChecker):
    """Interactive SQL formatting."""
    sql = get_multiline_input("Enter SQL to format (end with empty line or ';'):\n")
    if not sql.strip():
        print_colored("No SQL provided.", Fore.YELLOW if COLORAMA_AVAILABLE else "")
        return
    
    formatted = checker.format_sql(sql, pretty=True)
    if formatted:
        print("\n" + "=" * 70)
        print_colored("FORMATTED SQL:", Fore.GREEN if COLORAMA_AVAILABLE else "")
        print("=" * 70)
        print(formatted)
        print("=" * 70 + "\n")
    else:
        print_colored("Failed to format SQL. Check syntax.", Fore.RED if COLORAMA_AVAILABLE else "")


def load_from_file(checker: AQLSQLChecker):
    """Load and check SQL from a file."""
    filepath = input("Enter file path: ").strip()
    try:
        with open(filepath, 'r') as f:
            sql = f.read()
        
        # Split by semicolons to handle multiple statements
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        
        for i, stmt in enumerate(statements, 1):
            if stmt:
                print(f"\n{'─' * 70}")
                print_colored(f"Statement #{i}", Fore.YELLOW if COLORAMA_AVAILABLE else "")
                print(f"{'─' * 70}")
                analysis = checker.analyze_query(stmt)
                print_analysis(analysis)
    
    except FileNotFoundError:
        print_colored(f"File not found: {filepath}", Fore.RED if COLORAMA_AVAILABLE else "")
    except Exception as e:
        print_colored(f"Error reading file: {e}", Fore.RED if COLORAMA_AVAILABLE else "")


def run_examples(checker: AQLSQLChecker):
    """Run example queries."""
    examples = [
        ("Basic SELECT", 
         "SELECT Document.DocumentId, Document.Title FROM Document WHERE Document.Status = 'Active'"),
        
        ("SELECT with JOIN", 
         """SELECT d.DocumentId, p.ProjectName
            FROM Document d
            INNER JOIN Project p ON d.ProjectId = p.ProjectId"""),
        
        ("SELECT with Aggregate", 
         "SELECT Supplier.Name, COUNT(*) as cnt FROM Invoice GROUP BY Supplier.Name"),
        
        ("Date Function",
         "SELECT Document.DocumentId, FORMATDATE(Document.CreatedDate, 'yyyy-MM-dd') FROM Document"),
        
        ("Invalid SQL", 
         "SELECT FROM"),
    ]
    
    for name, sql in examples:
        print(f"\n{'─' * 70}")
        print_colored(f"Example: {name}", Fore.YELLOW if COLORAMA_AVAILABLE else "")
        print(f"{'─' * 70}")
        analysis = checker.analyze_query(sql)
        print_analysis(analysis)


def show_help():
    """Show help information."""
    print("\n" + "=" * 70)
    print_colored("HELP - AQL SQL Syntax Checker", Fore.CYAN if COLORAMA_AVAILABLE else "")
    print("=" * 70)
    print("""
This interactive tool helps you validate and analyze AQL (Ariba Query Language) statements.

FEATURES:
- Syntax validation for AQL SQL
- Query analysis (tables, columns, clauses, functions)
- SQL formatting and pretty-printing
- Batch processing from files
- Built-in examples

SUPPORTED SQL TYPES:
- SELECT statements with WHERE, JOIN, GROUP BY, HAVING, ORDER BY
- INSERT, UPDATE, DELETE statements
- Subqueries and nested queries
- Aggregate functions (COUNT, SUM, AVG, MIN, MAX)
- AQL date/time functions (FORMATDATE, ADDDAYS, DATEDIFF, etc.)
- AQL string functions (STRINGCONCAT, SUBSTRING, LEN, etc.)
- AQL math functions (ROUND, CEILING, FLOOR, etc.)
- CASE expressions and conditional functions (IIF, ISNULL, NULLIF)

AQL-SPECIFIC FEATURES:
- Ariba object references (Document, Project, Supplier, Invoice, etc.)
- Dot notation for field access (Document.DocumentId, Project.ProjectName)
- Ariba date/time, string, and math functions

TIPS:
- Enter your SQL, then press Enter twice (empty line) to submit
- Or enter ';' on a new line to submit
- For single-line SQL, just type it and press Enter twice
- For file input, separate multiple statements with semicolons
- The checker validates syntax but not database schema

For more information, see AQL_README.md
""")
    print("=" * 70 + "\n")


def main():
    """Main interactive loop."""
    checker = AQLSQLChecker()
    
    print_colored("\n🚀 Welcome to AQL SQL Syntax Checker!", Fore.MAGENTA if COLORAMA_AVAILABLE else "")
    
    while True:
        print_menu()
        choice = input("Select an option (1-6): ").strip()
        
        if choice == '1':
            check_sql_interactive(checker)
        elif choice == '2':
            format_sql_interactive(checker)
        elif choice == '3':
            load_from_file(checker)
        elif choice == '4':
            run_examples(checker)
        elif choice == '5':
            show_help()
        elif choice == '6':
            print_colored("\n👋 Goodbye!", Fore.MAGENTA if COLORAMA_AVAILABLE else "")
            sys.exit(0)
        else:
            print_colored("Invalid option. Please try again.", Fore.RED if COLORAMA_AVAILABLE else "")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n👋 Interrupted by user. Goodbye!", Fore.MAGENTA if COLORAMA_AVAILABLE else "")
        sys.exit(0)

