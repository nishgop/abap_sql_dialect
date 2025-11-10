"""
Interactive ABAP SQL Syntax Checker

This script provides an interactive command-line interface for checking ABAP SQL syntax.
"""

import sys
from abap_sql_checker import ABAPSQLChecker, print_analysis
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
    print_colored("ABAP SQL Syntax Checker - Interactive Mode", Fore.CYAN if COLORAMA_AVAILABLE else "")
    print("=" * 70)
    print("\nOptions:")
    print("  1. Check SQL syntax")
    print("  2. Format SQL statement")
    print("  3. Load SQL from file")
    print("  4. Run example queries")
    print("  5. Help")
    print("  6. Exit")
    print()


def get_multiline_input(prompt: str = "Enter SQL (end with ';' on a new line):\n") -> str:
    """Get multiline SQL input from user."""
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == ';':
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines)


def check_sql_interactive(checker: ABAPSQLChecker):
    """Interactive SQL checking."""
    sql = get_multiline_input()
    if not sql.strip():
        print_colored("No SQL provided.", Fore.YELLOW if COLORAMA_AVAILABLE else "")
        return
    
    analysis = checker.analyze_query(sql)
    print_analysis(analysis)


def format_sql_interactive(checker: ABAPSQLChecker):
    """Interactive SQL formatting."""
    sql = get_multiline_input("Enter SQL to format (end with ';' on a new line):\n")
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


def load_from_file(checker: ABAPSQLChecker):
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


def run_examples(checker: ABAPSQLChecker):
    """Run example queries."""
    examples = [
        ("Basic SELECT", "SELECT carrid, connid FROM sflight WHERE carrid = 'AA'"),
        ("SELECT with JOIN", """SELECT f.carrid, f.connid, p.cityfrom
                                FROM sflight AS f
                                INNER JOIN spfli AS p ON f.carrid = p.carrid"""),
        ("SELECT with Aggregate", "SELECT carrid, COUNT(*) as cnt FROM sflight GROUP BY carrid"),
        ("Invalid SQL", "SELECT FROM"),
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
    print_colored("HELP - ABAP SQL Syntax Checker", Fore.CYAN if COLORAMA_AVAILABLE else "")
    print("=" * 70)
    print("""
This interactive tool helps you validate and analyze ABAP SQL statements.

FEATURES:
- Syntax validation for ABAP SQL
- Query analysis (tables, columns, clauses)
- SQL formatting and pretty-printing
- Batch processing from files
- Built-in examples

SUPPORTED SQL TYPES:
- SELECT statements with WHERE, JOIN, GROUP BY, HAVING, ORDER BY
- INSERT, UPDATE, DELETE statements
- Subqueries and nested queries
- Aggregate functions (COUNT, SUM, AVG, MIN, MAX)
- CASE expressions

TIPS:
- End multi-line input with a single ';' on a new line
- For file input, separate multiple statements with semicolons
- The checker validates syntax but not database schema

For more information, see README.md
""")
    print("=" * 70 + "\n")


def main():
    """Main interactive loop."""
    checker = ABAPSQLChecker()
    
    print_colored("\n🚀 Welcome to ABAP SQL Syntax Checker!", Fore.MAGENTA if COLORAMA_AVAILABLE else "")
    
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

