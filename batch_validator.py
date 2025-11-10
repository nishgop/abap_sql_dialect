"""
Batch SQL Validator - Process multiple SQL files and generate reports

This script demonstrates how to use the ABAP SQL Checker to validate
multiple SQL files in batch and generate comprehensive reports.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from abap_sql_checker import ABAPSQLChecker

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


class SQLBatchValidator:
    """Batch validator for SQL files."""
    
    def __init__(self, output_dir: str = "validation_reports"):
        """Initialize batch validator."""
        self.checker = ABAPSQLChecker()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results: List[Dict] = []
    
    def validate_file(self, filepath: str) -> Dict:
        """
        Validate all SQL statements in a file.
        
        Args:
            filepath: Path to SQL file
            
        Returns:
            Dictionary with validation results
        """
        result = {
            "file": filepath,
            "timestamp": datetime.now().isoformat(),
            "queries": [],
            "summary": {
                "total": 0,
                "valid": 0,
                "invalid": 0,
                "warnings": 0
            }
        }
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Split by semicolons (handle SQL statements)
            # Filter out SQL comments
            lines = content.split('\n')
            clean_lines = []
            for line in lines:
                # Remove single-line comments
                if '--' in line:
                    line = line[:line.index('--')]
                clean_lines.append(line)
            
            clean_content = '\n'.join(clean_lines)
            statements = [s.strip() for s in clean_content.split(';') if s.strip()]
            
            for i, sql in enumerate(statements, 1):
                if not sql:
                    continue
                
                analysis = self.checker.analyze_query(sql)
                
                query_result = {
                    "query_number": i,
                    "sql": sql[:100] + "..." if len(sql) > 100 else sql,
                    "valid": analysis['valid'],
                    "errors": analysis['errors'],
                    "warnings": analysis['warnings'],
                    "query_type": analysis.get('query_type', 'Unknown'),
                    "tables": analysis.get('tables', [])
                }
                
                result["queries"].append(query_result)
                result["summary"]["total"] += 1
                
                if analysis['valid']:
                    result["summary"]["valid"] += 1
                else:
                    result["summary"]["invalid"] += 1
                
                if analysis['warnings']:
                    result["summary"]["warnings"] += len(analysis['warnings'])
        
        except FileNotFoundError:
            result["error"] = f"File not found: {filepath}"
        except Exception as e:
            result["error"] = f"Error processing file: {str(e)}"
        
        return result
    
    def validate_directory(self, dirpath: str, pattern: str = "*.sql") -> List[Dict]:
        """
        Validate all SQL files in a directory.
        
        Args:
            dirpath: Directory path
            pattern: File pattern to match (default: *.sql)
            
        Returns:
            List of validation results
        """
        directory = Path(dirpath)
        sql_files = list(directory.glob(pattern))
        
        print_colored(f"\n📁 Found {len(sql_files)} SQL file(s) in {dirpath}", 
                     Fore.CYAN if COLORAMA_AVAILABLE else "")
        
        results = []
        for sql_file in sql_files:
            print(f"\n⏳ Validating: {sql_file.name}")
            result = self.validate_file(str(sql_file))
            results.append(result)
            
            # Print quick summary
            summary = result["summary"]
            if "error" in result:
                print_colored(f"   ❌ Error: {result['error']}", 
                            Fore.RED if COLORAMA_AVAILABLE else "")
            else:
                status = "✓" if summary["invalid"] == 0 else "✗"
                color = Fore.GREEN if summary["invalid"] == 0 else Fore.YELLOW
                print_colored(f"   {status} {summary['valid']}/{summary['total']} valid, "
                            f"{summary['warnings']} warnings",
                            color if COLORAMA_AVAILABLE else "")
        
        self.results.extend(results)
        return results
    
    def generate_text_report(self, results: List[Dict]) -> str:
        """Generate a text report from results."""
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("SQL VALIDATION BATCH REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Total Files: {len(results)}")
        report_lines.append("")
        
        # Overall summary
        total_queries = sum(r["summary"]["total"] for r in results if "summary" in r)
        total_valid = sum(r["summary"]["valid"] for r in results if "summary" in r)
        total_invalid = sum(r["summary"]["invalid"] for r in results if "summary" in r)
        total_warnings = sum(r["summary"]["warnings"] for r in results if "summary" in r)
        
        report_lines.append("OVERALL SUMMARY")
        report_lines.append("-" * 80)
        report_lines.append(f"Total Queries: {total_queries}")
        report_lines.append(f"Valid: {total_valid} ({100*total_valid/total_queries if total_queries else 0:.1f}%)")
        report_lines.append(f"Invalid: {total_invalid}")
        report_lines.append(f"Total Warnings: {total_warnings}")
        report_lines.append("")
        
        # File-by-file details
        for result in results:
            report_lines.append("=" * 80)
            report_lines.append(f"FILE: {result['file']}")
            report_lines.append("=" * 80)
            
            if "error" in result:
                report_lines.append(f"ERROR: {result['error']}")
                continue
            
            summary = result["summary"]
            report_lines.append(f"Total Queries: {summary['total']}")
            report_lines.append(f"Valid: {summary['valid']}")
            report_lines.append(f"Invalid: {summary['invalid']}")
            report_lines.append(f"Warnings: {summary['warnings']}")
            report_lines.append("")
            
            # List invalid queries
            invalid_queries = [q for q in result["queries"] if not q["valid"]]
            if invalid_queries:
                report_lines.append("INVALID QUERIES:")
                for q in invalid_queries:
                    report_lines.append(f"\n  Query #{q['query_number']}:")
                    report_lines.append(f"  SQL: {q['sql']}")
                    report_lines.append(f"  Errors:")
                    for error in q['errors']:
                        report_lines.append(f"    - {error}")
            
            # List queries with warnings
            warned_queries = [q for q in result["queries"] if q["warnings"]]
            if warned_queries:
                report_lines.append("\nQUERIES WITH WARNINGS:")
                for q in warned_queries:
                    report_lines.append(f"\n  Query #{q['query_number']}:")
                    report_lines.append(f"  SQL: {q['sql']}")
                    report_lines.append(f"  Warnings:")
                    for warning in q['warnings']:
                        report_lines.append(f"    - {warning}")
            
            report_lines.append("")
        
        return '\n'.join(report_lines)
    
    def save_json_report(self, results: List[Dict], filename: str = "validation_report.json"):
        """Save results as JSON."""
        output_path = self.output_dir / filename
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        return output_path
    
    def save_text_report(self, results: List[Dict], filename: str = "validation_report.txt"):
        """Save results as text."""
        output_path = self.output_dir / filename
        report = self.generate_text_report(results)
        with open(output_path, 'w') as f:
            f.write(report)
        return output_path


def main():
    """Main function for batch validation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch SQL Validator for ABAP SQL")
    parser.add_argument("path", help="File or directory path to validate")
    parser.add_argument("-o", "--output", default="validation_reports", 
                       help="Output directory for reports (default: validation_reports)")
    parser.add_argument("-p", "--pattern", default="*.sql", 
                       help="File pattern for directory validation (default: *.sql)")
    parser.add_argument("--json", action="store_true", help="Generate JSON report")
    parser.add_argument("--text", action="store_true", help="Generate text report")
    
    args = parser.parse_args()
    
    # Default to both formats if none specified
    if not args.json and not args.text:
        args.json = True
        args.text = True
    
    validator = SQLBatchValidator(output_dir=args.output)
    
    print_colored("\n🚀 ABAP SQL Batch Validator", Fore.MAGENTA if COLORAMA_AVAILABLE else "")
    print("=" * 80)
    
    # Determine if path is file or directory
    path = Path(args.path)
    
    if path.is_file():
        print(f"Validating file: {path}")
        results = [validator.validate_file(str(path))]
    elif path.is_dir():
        print(f"Validating directory: {path}")
        results = validator.validate_directory(str(path), args.pattern)
    else:
        print_colored(f"❌ Path not found: {path}", Fore.RED if COLORAMA_AVAILABLE else "")
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print_colored("📊 GENERATING REPORTS", Fore.CYAN if COLORAMA_AVAILABLE else "")
    print("=" * 80)
    
    # Generate reports
    if args.json:
        json_path = validator.save_json_report(results)
        print(f"✓ JSON report saved: {json_path}")
    
    if args.text:
        text_path = validator.save_text_report(results)
        print(f"✓ Text report saved: {text_path}")
        
        # Print summary to console
        print("\n" + validator.generate_text_report(results))
    
    print_colored("\n✨ Validation complete!", Fore.MAGENTA if COLORAMA_AVAILABLE else "")


if __name__ == "__main__":
    main()

