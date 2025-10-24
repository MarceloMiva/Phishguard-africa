#!/usr/bin/env python3
import json
import sys
import argparse
from typing import List
from colorama import Fore, Style, init

from .detector import PhishingDetector
from .analyzer import ThreatAnalyzer

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def cmd_check(args):
    """Check a single message for phishing attempts"""
    detector = PhishingDetector()
    analysis = detector.analyze_message(args.message, args.sender)

    if args.json_output:
        print(json.dumps(analysis, indent=2))
    else:
        display_analysis(analysis, args.message)


def cmd_batch(args):
    """Check multiple messages from a file (JSON format)"""
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            messages = json.load(f)
    except (json.JSONDecodeError, OSError):
        print(f"{Fore.RED}Error: Invalid JSON file or cannot open file")
        sys.exit(1)

    detector = PhishingDetector()
    results = detector.check_multiple_messages(messages)

    if args.json_output:
        print(json.dumps(results, indent=2))
    else:
        display_batch_results(results)


def cmd_stats(_args):
    """Show threat statistics and analysis"""
    analyzer = ThreatAnalyzer()
    report = analyzer.generate_report()

    print(f"{Fore.CYAN}📊 PhishGuard Africa - Threat Report")
    print("=" * 50)

    summary = report.get('summary', {})
    print(f"{Fore.YELLOW}Last 30 Days Summary:")
    print(f"  Total Messages: {summary.get('total_messages', 0)}")
    print(f"  Phishing Detected: {summary.get('phishing_messages', 0)}")
    print(f"  Phishing Rate: {summary.get('phishing_rate', 0)}%")
    print(f"  High Risk Messages: {summary.get('high_risk_messages', 0)}")

    print(f"\n{Fore.YELLOW}Top Threat Patterns:")
    for pattern in report.get('top_threat_patterns', [])[:5]:
        reasons = ', '.join(pattern.get('reasons', []))
        print(f"  {pattern.get('count', 0)}x - {reasons}")

    print(f"\n{Fore.GREEN}Security Recommendations:")
    for rec in report.get('recommendations', [])[:3]:
        print(f"  • {rec}")


def cmd_demo(args):
    """Run demonstration with sample messages"""
    sample_messages = [
        {
            "sender": "+27123456789",
            "content": "URGENT: Your ABSA account has been suspended. Click here to verify: http://bit.ly/absa-secure-now"
        },
        {
            "sender": "MTN",
            "content": "Congratulations! You won R50,000 from MTN. Claim your prize: http://tinyurl.com/mtn-win-2024"
        },
        {
            "sender": "Mom",
            "content": "Hi, can you please send me some airtime when you get a chance?"
        },
        {
            "sender": "+441234567890",
            "content": "Security Alert: Unusual login detected on your account. Verify now: http://security-update-africa.com"
        }
    ]

    detector = PhishingDetector()

    print(f"{Fore.CYAN}🔍 PhishGuard Africa - Demo Mode")
    print("=" * 50)

    for i, msg in enumerate(sample_messages, 1):
        analysis = detector.analyze_message(msg['content'], msg['sender'])

        print(f"\n{Fore.WHITE}Message {i}:")
        print(f"From: {msg['sender']}")
        print(f"Content: {msg['content']}")
        display_analysis(analysis, msg['content'])

        if args.interactive and i < len(sample_messages):
            resp = input("Continue to next message? [Y/n]: ").strip().lower()
            if resp not in ("", "y", "yes"):
                break


def display_analysis(analysis: dict, original_message: str):
    """Display analysis results in a user-friendly format"""
    threat_level = analysis.get('threat_level', 'low')
    confidence = analysis.get('confidence', 0)
    reasons = analysis.get('reasons', [])

    # Color coding based on threat level
    if threat_level == 'high':
        color = Fore.RED
        icon = "🚨"
    elif threat_level == 'medium':
        color = Fore.YELLOW
        icon = "⚠"
    else:
        color = Fore.GREEN
        icon = "✅"

    print(f"\n{color}{icon} Threat Level: {threat_level.upper()}")
    print(f"{color}Confidence: {confidence}%")

    if reasons:
        print(f"{color}Reasons: {', '.join(reasons)}")

    if analysis.get('is_phishing'):
        print(f"{Fore.RED}🚫 This message appears to be PHISHING!")
    else:
        print(f"{Fore.GREEN}✅ This message appears to be safe.")


def display_batch_results(results: dict):
    """Display batch analysis results"""
    print(f"{Fore.CYAN}📊 Batch Analysis Results")
    print("=" * 50)
    print(f"Total Messages: {results.get('total_messages', 0)}")
    print(f"Phishing Detected: {results.get('phishing_count', 0)}")
    print(f"High Risk: {results.get('high_risk_count', 0)}")
    print(f"Medium Risk: {results.get('medium_risk_count', 0)}")
    print(f"Low Risk: {results.get('low_risk_count', 0)}")

    total = results.get('total_messages', 0)
    phishing_count = results.get('phishing_count', 0)
    phishing_rate = (phishing_count / total * 100) if total > 0 else 0
    print(f"Phishing Rate: {phishing_rate:.1f}%")


def build_parser():
    parser = argparse.ArgumentParser(prog="phishguard", description="PhishGuard Africa - SMS Phishing Detection System")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # check
    p_check = subparsers.add_parser("check", help="Check a single message for phishing attempts")
    p_check.add_argument("message", help="Message content")
    p_check.add_argument("--sender", "-s", default="Unknown", help="Message sender")
    p_check.add_argument("--json-output", "-j", action="store_true", help="Output in JSON format")
    p_check.set_defaults(func=cmd_check)

    # batch
    p_batch = subparsers.add_parser("batch", help="Check multiple messages from a file (JSON format)")
    p_batch.add_argument("file", help="Path to JSON file containing messages")
    p_batch.add_argument("--json-output", "-j", action="store_true", help="Output in JSON format")
    p_batch.set_defaults(func=cmd_batch)

    # stats
    p_stats = subparsers.add_parser("stats", help="Show threat statistics and analysis")
    p_stats.set_defaults(func=cmd_stats)

    # demo
    p_demo = subparsers.add_parser("demo", help="Run demonstration with sample messages")
    p_demo.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    p_demo.set_defaults(func=cmd_demo)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()