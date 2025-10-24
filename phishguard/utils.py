import re
import json
from datetime import datetime
from typing import List, Dict

def validate_phone_number(phone: str) -> bool:
    """Validate African phone number formats"""
    patterns = [
        r'^\+27\d{9}$',      # South Africa
        r'^\+234\d{10}$',    # Nigeria
        r'^\+254\d{9}$',     # Kenya
        r'^\+233\d{9}$',     # Ghana
        r'^0\d{9}$',         # Local format
    ]
    
    return any(re.match(pattern, phone) for pattern in patterns)

def extract_urls(text: str) -> List[str]:
    """Extract all URLs from text"""
    url_pattern = r'https?://[^\s]+'
    return re.findall(url_pattern, text)

def save_to_file(data: Dict, filename: str = "phishguard_analysis.json"):
    """Save analysis results to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_messages_from_file(filename: str) -> List[Dict]:
    """Load messages from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Error loading messages from {filename}: {str(e)}")

def format_threat_level(level: str) -> str:
    """Format threat level with emoji"""
    levels = {
        'high': '🔴 HIGH',
        'medium': '🟡 MEDIUM', 
        'low': '🟢 LOW'
    }
    return levels.get(level, '⚪ UNKNOWN')