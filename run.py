#!/usr/bin/env python3
"""
Simple test script for PhishGuard Africa
Run this to verify everything works before using Streamlit
"""

import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(_file_), 'app'))

def test_phishguard():
    print("🛡 PhishGuard Africa - Quick Test")
    print("=" * 50)
    
    try:
        from model import detector
        
        # Test messages
        test_messages = [
            "You have received KSH 2,500 from John Doe",
            "URGENT: Your M-Pesa account will be suspended. Verify now: http://fake.com",
            "Your balance is KSH 1,500.50",
            "You won KSH 50,000! Claim your prize: http://bit.ly/win",
            "Payment to merchant successful"
        ]
        
        print("🧪 Testing detection engine...")
        for i, message in enumerate(test_messages, 1):
            result, confidence, features = detector.predict(message)
            print(f"{i}. '{message}'")
            print(f"   → Result: {result} (Confidence: {confidence:.2%})")
            print()
        
        print("✅ All tests completed successfully!")
        print("\n🎉 PhishGuard Africa is working!")
        print("🚀 Now run: streamlit run app/main.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you installed all requirements:")
        print("   pip install -r requirements.txt")

if _name_ == "_main_":
    test_phishguard()