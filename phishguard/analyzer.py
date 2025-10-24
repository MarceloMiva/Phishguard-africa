import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List
import statistics

class ThreatAnalyzer:
    def _init_(self, db_path: str = "phishguard.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for storing threat data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_content TEXT,
                sender TEXT,
                is_phishing BOOLEAN,
                threat_level TEXT,
                confidence INTEGER,
                reasons TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                total_messages INTEGER,
                phishing_count INTEGER,
                blocked_count INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_analysis(self, analysis: Dict):
        """Save analysis results to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO threats 
            (message_content, sender, is_phishing, threat_level, confidence, reasons)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            analysis.get('message_content', ''),
            analysis.get('sender', 'Unknown'),
            analysis['is_phishing'],
            analysis['threat_level'],
            analysis['confidence'],
            json.dumps(analysis['reasons'])
        ))
        
        conn.commit()
        conn.close()
    
    def get_daily_stats(self, days: int = 7) -> Dict:
        """Get statistics for the last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).date()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_messages,
                SUM(CASE WHEN is_phishing = 1 THEN 1 ELSE 0 END) as phishing_count,
                SUM(CASE WHEN threat_level = 'high' THEN 1 ELSE 0 END) as high_risk_count
            FROM threats 
            WHERE DATE(timestamp) >= ?
        ''', (start_date,))
        
        result = cursor.fetchone()
        
        stats = {
            'period_days': days,
            'total_messages': result[0] if result else 0,
            'phishing_messages': result[1] if result else 0,
            'high_risk_messages': result[2] if result else 0,
            'phishing_rate': round((result[1] / result[0] * 100) if result and result[0] > 0 else 0, 2)
        }
        
        conn.close()
        return stats
    
    def get_top_threat_patterns(self) -> List[Dict]:
        """Get most common threat patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT reasons, COUNT(*) as count
            FROM threats 
            WHERE is_phishing = 1
            GROUP BY reasons
            ORDER BY count DESC
            LIMIT 10
        ''')
        
        patterns = []
        for row in cursor.fetchall():
            patterns.append({
                'reasons': json.loads(row[0]),
                'count': row[1]
            })
        
        conn.close()
        return patterns
    
    def generate_report(self) -> Dict:
        """Generate comprehensive threat report"""
        daily_stats = self.get_daily_stats(30)
        top_patterns = self.get_top_threat_patterns()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': daily_stats,
            'top_threat_patterns': top_patterns,
            'recommendations': self._generate_recommendations(daily_stats, top_patterns)
        }
        
        return report
    
    def _generate_recommendations(self, stats: Dict, patterns: List[Dict]) -> List[str]:
        """Generate security recommendations based on analysis"""
        recommendations = []
        
        if stats['phishing_rate'] > 20:
            recommendations.append("High phishing rate detected. Consider enabling strict mode.")
        
        if any('suspicious links' in str(pattern) for pattern in patterns):
            recommendations.append("Frequent suspicious links detected. Avoid clicking unknown URLs.")
        
        if any('urgency keywords' in str(pattern) for pattern in patterns):
            recommendations.append("Urgency-based scams detected. Be cautious of time-sensitive messages.")
        
        # Always include general recommendations
        recommendations.extend([
            "Never share banking details via SMS",
            "Verify unexpected prize notifications directly with companies",
            "Use official banking apps for account verification",
            "Enable two-factor authentication where available"
        ])
        
        return recommendations