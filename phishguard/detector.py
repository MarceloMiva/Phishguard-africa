import re
import json
from typing import Dict, List, Tuple
from datetime import datetime

class PhishingDetector:
    def _init_(self):
        self.african_banks = [
            'absa', 'standard bank', 'fnb', 'nedbank', 'capitec',
            'ecobank', 'uba', 'zenith', 'access bank', 'gtbank',
            'first bank', 'union bank', 'fidelity', 'polaris'
        ]
        
        self.telecom_companies = [
            'mtn', 'vodacom', 'safaricom', 'airtel', 'orange',
            'telkom', 'cell c', 'mpesa', 'mobile money'
        ]
        
        self.suspicious_keywords = [
            'urgent', 'immediately', 'account suspended', 'verify now',
            'click here', 'limited time', 'winner', 'prize', 'lottery',
            'bank alert', 'security update', 'password expired',
            'unauthorized login', 'confirm your account', 'free money',
            'bonus', 'reward', 'congratulations', 'you have won'
        ]
        
        self.suspicious_url_patterns = [
            r'bit\.ly/\w+',
            r'tinyurl\.com/\w+',
            r'goo\.gl/\w+',
            r'shorturl\.at/\w+',
            r'http://\d+\.\d+\.\d+\.\d+',
            r'free.*money',
            r'win.*prize',
            r'claim.*reward'
        ]
        
        self.trusted_senders = [
            'MTN', 'VODACOM', 'SAFARICOM', 'AIRTEL', 'ABSABANK'
        ]

    def analyze_message(self, message: str, sender: str = "Unknown") -> Dict:
        """Analyze a message for phishing indicators"""
        analysis = {
            'is_phishing': False,
            'confidence': 0,
            'threat_level': 'low',  # low, medium, high
            'reasons': [],
            'sender_risk': 0,
            'content_risk': 0,
            'url_risk': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        # Analyze sender
        analysis['sender_risk'] = self._analyze_sender(sender)
        
        # Analyze content
        analysis['content_risk'] = self._analyze_content(message)
        
        # Analyze URLs
        analysis['url_risk'] = self._analyze_urls(message)
        
        # Calculate overall risk
        total_risk = analysis['sender_risk'] + analysis['content_risk'] + analysis['url_risk']
        
        # Determine threat level
        if total_risk >= 7:
            analysis['is_phishing'] = True
            analysis['confidence'] = min(95, total_risk * 10)
            analysis['threat_level'] = 'high'
        elif total_risk >= 4:
            analysis['is_phishing'] = True
            analysis['confidence'] = total_risk * 8
            analysis['threat_level'] = 'medium'
        elif total_risk >= 2:
            analysis['confidence'] = total_risk * 5
            analysis['threat_level'] = 'low'
        
        # Generate reasons
        if analysis['sender_risk'] > 0:
            analysis['reasons'].append('Suspicious sender pattern')
        if analysis['content_risk'] > 0:
            analysis['reasons'].append('Contains phishing keywords')
        if analysis['url_risk'] > 0:
            analysis['reasons'].append('Contains suspicious links')
            
        return analysis

    def _analyze_sender(self, sender: str) -> int:
        """Analyze sender for risk factors"""
        risk = 0
        
        # Check if sender is in trusted list
        sender_upper = sender.upper()
        if any(trusted in sender_upper for trusted in self.trusted_senders):
            risk -= 1
        
        # Check for short codes (usually legitimate)
        if re.match(r'^\d{3,6}$', sender):
            risk -= 1
        
        # Check for international numbers
        if sender.startswith('+') and not any(code in sender for code in ['+27', '+234', '+254', '+233']):
            risk += 2
        
        # Check for suspicious sender names
        suspicious_sender_terms = ['bank', 'security', 'alert', 'update']
        if any(term in sender.lower() for term in suspicious_sender_terms):
            risk += 1
            
        return max(0, risk)

    def _analyze_content(self, content: str) -> int:
        """Analyze message content for phishing indicators"""
        risk = 0
        content_lower = content.lower()
        
        # Check for urgency keywords
        for keyword in self.suspicious_keywords:
            if keyword in content_lower:
                risk += 1
        
        # Check for bank mentions with urgency
        for bank in self.african_banks:
            if bank in content_lower:
                if any(urgent in content_lower for urgent in ['urgent', 'verify', 'suspended', 'update']):
                    risk += 2
        
        # Check for telecom scams
        for telecom in self.telecom_companies:
            if telecom in content_lower:
                if any(scam in content_lower for scam in ['win', 'prize', 'free', 'bonus']):
                    risk += 2
        
        # Check for monetary amounts with urgency
        amount_pattern = r'(R\s?\d+|₦\s?\d+|KSh\s?\d+|GHS\s?\d+|USD\s?\d+|ZAR\s?\d+)'
        if re.search(amount_pattern, content, re.IGNORECASE):
            if any(word in content_lower for word in ['win', 'won', 'prize', 'reward']):
                risk += 2
        
        return min(5, risk)

    def _analyze_urls(self, content: str) -> int:
        """Analyze URLs in message content"""
        risk = 0
        
        # Find all URLs
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, content)
        
        for url in urls:
            url_lower = url.lower()
            
            # Check for URL shorteners
            if any(shortener in url_lower for shortener in ['bit.ly', 'tinyurl', 'goo.gl', 'shorturl']):
                risk += 2
            
            # Check for IP addresses in URLs
            ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            if re.search(ip_pattern, url):
                risk += 3
            
            # Check for suspicious keywords in URLs
            suspicious_url_terms = ['free', 'win', 'prize', 'reward', 'bonus', 'claim']
            if any(term in url_lower for term in suspicious_url_terms):
                risk += 2
        
        return risk

    def check_multiple_messages(self, messages: List[Dict]) -> Dict:
        """Analyze multiple messages and provide summary"""
        results = {
            'total_messages': len(messages),
            'phishing_count': 0,
            'high_risk_count': 0,
            'medium_risk_count': 0,
            'low_risk_count': 0,
            'analyses': []
        }
        
        for msg in messages:
            analysis = self.analyze_message(msg.get('content', ''), msg.get('sender', 'Unknown'))
            results['analyses'].append(analysis)
            
            if analysis['is_phishing']:
                results['phishing_count'] += 1
            
            if analysis['threat_level'] == 'high':
                results['high_risk_count'] += 1
            elif analysis['threat_level'] == 'medium':
                results['medium_risk_count'] += 1
            else:
                results['low_risk_count'] += 1
        
        return results