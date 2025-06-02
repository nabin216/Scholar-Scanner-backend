#!/usr/bin/env python
"""
Security Checker for Scholarship Portal
This script scans the codebase for common security issues and provides recommendations.
"""

import os
import re
import sys
from pathlib import Path
import json
from typing import List, Dict, Any, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("security_checker")

# Define colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def color_print(message: str, color: str):
    """Print colored message to terminal"""
    colors = {
        "header": Colors.HEADER,
        "blue": Colors.BLUE,
        "green": Colors.GREEN,
        "warning": Colors.WARNING,
        "fail": Colors.FAIL,
        "bold": Colors.BOLD,
        "underline": Colors.UNDERLINE
    }
    print(f"{colors.get(color, '')}{message}{Colors.ENDC}")

# Security patterns to check
SECURITY_PATTERNS = {
    "hardcoded_credentials": [
        r"password\s*=\s*['\"][^'\"]+['\"]",
        r"api_?key\s*=\s*['\"][^'\"]+['\"]",
        r"secret\s*=\s*['\"][^'\"]+['\"]",
        r"token\s*=\s*['\"][^'\"]+['\"]",
        r"Authorization:\s*Bearer\s+[a-zA-Z0-9_\-\.]+",
        r"auth_token\s*=\s*['\"][^'\"]+['\"]",
    ],
    "security_risks": [
        r"eval\s*\(",
        r"exec\s*\(",
        r"os\.system\(",
        r"subprocess\.call\(",
        r"\.\.\/",  # Path traversal
        r"__import__\(",
        r"request\.data\s+\|\s+safe",  # Django template XSS
    ],
    "insecure_settings": [
        r"DEBUG\s*=\s*True",
        r"ALLOWED_HOSTS\s*=\s*\[\s*['\"][*]['\"]",  # Wildcard hosts
        r"CORS_ALLOW_ALL_ORIGINS\s*=\s*True",
        r"SECRET_KEY\s*=\s*['\"][^'\"]+['\"]",
        r"X_FRAME_OPTIONS\s*=\s*['\"](ALLOW|ALLOW-FROM)['\"]",
    ],
    "insecure_direct_object_reference": [
        r"\.objects\.get\(id=(?!request\.user)",  # IDOR pattern, exclude user
        r"\.objects\.get\(pk=(?!request\.user)", 
        r"find_by_id\(",
        r"find_one\(\s*{\s*['\"]_id['\"]:",
    ],
    "insecure_url": [
        r"https?://localhost",
        r"https?://127\.0\.0\.1",
        r"https?://0\.0\.0\.0",
        r"https?://192\.168\.",
    ],
}

# Files to skip
SKIP_DIRS = [
    "venv", 
    "env", 
    ".git", 
    "__pycache__", 
    "node_modules",
    "migrations",
    "tests",
    "test_*",
]

# File extensions to check
VALID_EXTENSIONS = [
    ".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".yml", 
    ".yaml", ".html", ".htm", ".env.example", ".txt"
]

def is_valid_file(file_path: str) -> bool:
    """Check if file should be scanned"""
    
    # Skip directories in SKIP_DIRS
    for skip_dir in SKIP_DIRS:
        if skip_dir in file_path.split(os.sep):
            return False
    
    # Only check files with valid extensions
    _, ext = os.path.splitext(file_path)
    if ext not in VALID_EXTENSIONS:
        return False
    
    # Skip test files
    if os.path.basename(file_path).startswith("test_"):
        return False
        
    return True

def scan_line(line: str, line_num: int, patterns: List[str], category: str) -> List[Dict[str, Any]]:
    """Scan a single line for security issues"""
    findings = []
    
    for pattern in patterns:
        matches = re.finditer(pattern, line, re.IGNORECASE)
        for match in matches:
            findings.append({
                "line": line.strip(),
                "line_num": line_num,
                "match": match.group(0),
                "category": category
            })
    return findings

def scan_file(file_path: str) -> List[Dict[str, Any]]:
    """Scan a file for security issues"""
    findings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            
            for line_num, line in enumerate(lines, 1):
                for category, patterns in SECURITY_PATTERNS.items():
                    results = scan_line(line, line_num, patterns, category)
                    for result in results:
                        result["file_path"] = file_path
                        findings.append(result)
    except Exception as e:
        logger.warning(f"Error scanning {file_path}: {e}")
    
    return findings

def scan_directory(directory_path: str) -> List[Dict[str, Any]]:
    """Recursively scan a directory for security issues"""
    all_findings = []
    
    for root, dirs, files in os.walk(directory_path):
        # Skip directories in SKIP_DIRS
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            file_path = os.path.join(root, file)
            if is_valid_file(file_path):
                file_findings = scan_file(file_path)
                all_findings.extend(file_findings)
    
    return all_findings

def analyze_environment_vars(directory_path: str) -> List[Dict[str, Any]]:
    """Check for environment variables best practices"""
    env_findings = []
    env_files = []
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file == ".env" or file.startswith(".env."):
                env_files.append(os.path.join(root, file))
    
    if len(env_files) == 0:
        env_findings.append({
            "file_path": None,
            "line": None,
            "line_num": None,
            "match": "No .env files found",
            "category": "env_files",
            "recommendation": "Create .env files for environment variables and add .env to .gitignore"
        })
    
    # Check .gitignore for .env
    gitignore_path = os.path.join(directory_path, ".gitignore")
    env_ignored = False
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            if ".env" not in content and "*.env" not in content:
                env_findings.append({
                    "file_path": gitignore_path,
                    "line": None,
                    "line_num": None,
                    "match": ".env not in .gitignore",
                    "category": "env_files",
                    "recommendation": "Add .env to .gitignore to prevent committing sensitive information"
                })
            else:
                env_ignored = True
    
    # Check for env.example
    has_example = any(f.endswith(".env.example") for f in env_files)
    if not has_example:
        env_findings.append({
            "file_path": None,
            "line": None, 
            "line_num": None,
            "match": "No .env.example file found",
            "category": "env_files",
            "recommendation": "Create a .env.example file with dummy values as a template for developers"
        })
    
    return env_findings

def check_django_settings(directory_path: str) -> List[Dict[str, Any]]:
    """Check Django settings for security issues"""
    settings_findings = []
    
    # Find Django settings files
    settings_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file == "settings.py":
                settings_files.append(os.path.join(root, file))
    
    for settings_file in settings_files:
        try:
            with open(settings_file, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                
                # Check for critical security settings
                security_checks = [
                    {
                        "pattern": r"SECURE_SSL_REDIRECT\s*=\s*(?!True)",
                        "message": "SECURE_SSL_REDIRECT should be set to True in production",
                        "recommendation": "Set SECURE_SSL_REDIRECT=True in production"
                    },
                    {
                        "pattern": r"SESSION_COOKIE_SECURE\s*=\s*(?!True)",
                        "message": "SESSION_COOKIE_SECURE should be set to True in production",
                        "recommendation": "Set SESSION_COOKIE_SECURE=True in production"
                    },
                    {
                        "pattern": r"CSRF_COOKIE_SECURE\s*=\s*(?!True)",
                        "message": "CSRF_COOKIE_SECURE should be set to True in production",
                        "recommendation": "Set CSRF_COOKIE_SECURE=True in production"
                    },
                    {
                        "pattern": r"SECURE_HSTS_SECONDS\s*=\s*\d+",
                        "message": "SECURE_HSTS_SECONDS should be at least 31536000 (1 year)",
                        "recommendation": "Set SECURE_HSTS_SECONDS=31536000 in production"
                    },
                ]
                
                for check in security_checks:
                    if not re.search(r"if\s+not\s+DEBUG.*?" + check["pattern"], content, re.DOTALL):
                        if re.search(check["pattern"], content):
                            settings_findings.append({
                                "file_path": settings_file,
                                "line": None,
                                "line_num": None, 
                                "match": check["message"],
                                "category": "django_settings",
                                "recommendation": check["recommendation"]
                            })
                
                # Check for DEBUG logic
                if "DEBUG = True" in content and not re.search(r"DEBUG\s*=\s*os\.getenv.*?", content):
                    settings_findings.append({
                        "file_path": settings_file,
                        "line": None,
                        "line_num": None,
                        "match": "DEBUG hardcoded to True",
                        "category": "django_settings",
                        "recommendation": "Use environment variable: DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'"
                    })
                
                # Check for SECRET_KEY
                if re.search(r"SECRET_KEY\s*=\s*['\"][^'\"]+['\"]", content) and not re.search(r"SECRET_KEY\s*=\s*os\.getenv.*?", content):
                    settings_findings.append({
                        "file_path": settings_file,
                        "line": None,
                        "line_num": None,
                        "match": "SECRET_KEY hardcoded",
                        "category": "django_settings",
                        "recommendation": "Use environment variable: SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-only-key')"
                    })
        except Exception as e:
            logger.warning(f"Error checking Django settings in {settings_file}: {e}")
    
    return settings_findings

def check_frontend_security(directory_path: str) -> List[Dict[str, Any]]:
    """Check frontend files for security issues"""
    frontend_findings = []
    
    # Find package.json files
    package_files = []
    for root, dirs, files in os.walk(directory_path):
        if "node_modules" in root:
            continue
            
        if "package.json" in files:
            package_files.append(os.path.join(root, "package.json"))
    
    for package_file in package_files:
        try:
            with open(package_file, 'r', encoding='utf-8') as file:
                package_data = json.load(file)
                
                # Check dependencies for security packages
                has_helmet = False
                has_csp = False
                
                all_deps = {}
                if "dependencies" in package_data:
                    all_deps.update(package_data["dependencies"])
                if "devDependencies" in package_data:
                    all_deps.update(package_data["devDependencies"])
                
                for dep in all_deps:
                    if "helmet" in dep:
                        has_helmet = True
                    if "csp" in dep:
                        has_csp = True
                
                if not has_helmet and not has_csp:
                    frontend_findings.append({
                        "file_path": package_file,
                        "line": None,
                        "line_num": None,
                        "match": "No helmet.js or CSP package found",
                        "category": "frontend_security",
                        "recommendation": "Add helmet.js or a similar package for setting security headers"
                    })
        except Exception as e:
            logger.warning(f"Error checking package.json at {package_file}: {e}")
    
    return frontend_findings

def generate_security_report(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a report from security findings"""
    
    # Group findings by category
    grouped_findings = {}
    for finding in findings:
        category = finding["category"]
        if category not in grouped_findings:
            grouped_findings[category] = []
        grouped_findings[category].append(finding)
    
    # Calculate risk metrics
    total_findings = len(findings)
    high_risk = len([f for f in findings if f["category"] in ["hardcoded_credentials", "security_risks"]])
    medium_risk = len([f for f in findings if f["category"] in ["insecure_settings", "django_settings"]])
    low_risk = total_findings - high_risk - medium_risk
    
    # Generate report
    report = {
        "summary": {
            "total_findings": total_findings,
            "high_risk": high_risk,
            "medium_risk": medium_risk,
            "low_risk": low_risk
        },
        "findings": grouped_findings,
        "recommendations": {
            "hardcoded_credentials": "Replace hardcoded credentials with environment variables",
            "insecure_settings": "Update security settings in Django settings.py",
            "security_risks": "Review and fix security risks in the code",
            "insecure_direct_object_reference": "Add permission checks or use more secure methods",
            "insecure_url": "Replace hardcoded URLs with configurable values",
            "env_files": "Update environment variable configuration",
            "django_settings": "Improve Django security settings",
            "frontend_security": "Add security headers and CSP to frontend"
        }
    }
    
    return report

def print_report(report: Dict[str, Any]):
    """Print the security report to the console"""
    
    summary = report["summary"]
    
    print("\n" + "="*80)
    color_print(" SCHOLARSHIP PORTAL SECURITY SCAN REPORT ", "header")
    print("="*80)
    
    # Print summary metrics
    print(f"\n📊 {Colors.BOLD}FINDINGS SUMMARY:{Colors.ENDC}")
    color_print(f"  Total issues found: {summary['total_findings']}", "bold")
    color_print(f"  🔴 High Risk: {summary['high_risk']}", "fail")
    color_print(f"  🟠 Medium Risk: {summary['medium_risk']}", "warning")
    color_print(f"  🟢 Low Risk: {summary['low_risk']}", "green")
    
    # Print detailed findings
    findings = report["findings"]
    recommendations = report["recommendations"]
    
    risk_levels = {
        "hardcoded_credentials": ("🔴 HIGH RISK", "fail"),
        "security_risks": ("🔴 HIGH RISK", "fail"),
        "insecure_settings": ("🟠 MEDIUM RISK", "warning"),
        "django_settings": ("🟠 MEDIUM RISK", "warning"),
        "insecure_direct_object_reference": ("🟠 MEDIUM RISK", "warning"),
        "insecure_url": ("🟠 MEDIUM RISK", "warning"),
        "env_files": ("🟢 LOW RISK", "green"),
        "frontend_security": ("🟢 LOW RISK", "green"),
    }
    
    # Print findings by category
    for category, category_findings in findings.items():
        risk_text, risk_color = risk_levels.get(category, ("🟠 MEDIUM RISK", "warning"))
        
        print(f"\n{'-'*80}")
        color_print(f" {risk_text}: {category.upper().replace('_', ' ')} ({len(category_findings)} issues)", risk_color)
        print(f"{'-'*80}")
        
        if category in recommendations:
            color_print(f"💡 Recommendation: {recommendations[category]}", "blue")
        
        # Print individual findings
        for i, finding in enumerate(category_findings[:10], 1):
            file_path = finding.get("file_path", "Unknown")
            line_num = finding.get("line_num", "N/A")
            match = finding.get("match", "N/A")
            recommendation = finding.get("recommendation", recommendations.get(category, ""))
            
            print(f"\n{i}. {Colors.BOLD}Issue:{Colors.ENDC} {match}")
            print(f"   {Colors.BOLD}File:{Colors.ENDC} {file_path}")
            if line_num != "N/A":
                print(f"   {Colors.BOLD}Line:{Colors.ENDC} {line_num}")
            if recommendation:
                color_print(f"   💡 {recommendation}", "blue")
        
        # If there are more than 10 findings, show a summary
        if len(category_findings) > 10:
            color_print(f"\n... and {len(category_findings) - 10} more similar issues", "warning")
    
    # Print final recommendations
    print(f"\n{'-'*80}")
    color_print(" SECURITY RECOMMENDATIONS ", "header")
    print(f"{'-'*80}")
    
    print(f"\n1. {Colors.BOLD}Environment Variables:{Colors.ENDC}")
    print("   - Move all hardcoded credentials to .env files")
    print("   - Ensure .env files are in .gitignore")
    print("   - Provide .env.example files for development setup")
    
    print(f"\n2. {Colors.BOLD}Django Security Settings:{Colors.ENDC}")
    print("   - Set DEBUG based on environment: DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'")
    print("   - Use environment variables for SECRET_KEY")
    print("   - Enable security settings conditionally for production environments")
    
    print(f"\n3. {Colors.BOLD}Frontend Security:{Colors.ENDC}")
    print("   - Add security headers using helmet.js or similar package")
    print("   - Implement Content Security Policy (CSP)")
    print("   - Replace hardcoded URLs with environment variables")
    
    print(f"\n4. {Colors.BOLD}Authentication Security:{Colors.ENDC}")
    print("   - Review JWT settings and expirations")
    print("   - Ensure secure cookie settings")
    print("   - Implement rate limiting for login attempts")
    
    print("\n" + "="*80)
    print("")

def main():
    """Main function"""
    # Get the directory to scan
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # Get the project root directory if no argument is provided
        directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if not os.path.exists(directory):
        color_print(f"Error: Directory {directory} not found", "fail")
        sys.exit(1)
    
    color_print(f"\nScanning {directory} for security issues...", "blue")
    
    # Scan the codebase
    code_findings = scan_directory(directory)
    
    # Check environment variables
    env_findings = analyze_environment_vars(directory)
    
    # Check Django settings
    django_findings = check_django_settings(directory)
    
    # Check frontend security
    frontend_findings = check_frontend_security(directory)
    
    # Combine all findings
    all_findings = code_findings + env_findings + django_findings + frontend_findings
    
    # Generate and print report
    report = generate_security_report(all_findings)
    print_report(report)
    
    # Return exit code based on findings
    if report["summary"]["high_risk"] > 0:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
