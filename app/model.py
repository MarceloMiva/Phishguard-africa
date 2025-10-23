import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib
import re
import nltk
from nltk.corpus import stopwords

# Download NLTK data (it will handle if already downloaded)
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
except:
    pass

class PhishingDetector:
    def _init_(self):
        self.model = None
        self.vectorizer = None
        self.is_trained = False
        self.train_model()
    
    def generate_training_data(self):
        """Generate synthetic training data for African mobile money context"""
        print("🔄 Generating training data...")
        
        # Legitimate messages
        legitimate_messages = [
            "You have received KSH 2,500 from John Doe. New balance is KSH 3,950.50",
            "Your M-Pesa balance is KSH 1,450.50 as of 12/05/2024",
            "Payment of KSH 500 to Merchant XYZ successful. Charge KSH 0.00",
            "Withdrawal of KSH 1,000 at Agent 123456 successful",
            "You sent KSH 300 to +254712345678. New balance 2,200.50",
            "Airtime purchase of KSH 100 successful. Balance KSH 1,500.00",
            "Your loan application has been approved",
            "Safaricom: Your data bundle has been renewed",
            "Welcome to M-Pesa! Your account is now active",
            "Transaction confirmed. Reference number 1234567890",
            "You have received KSH 5,000 from Mary Wambui",
            "Send money to 0722123456 successful. Charge KSH 27",
            "Your M-Pesa statement is ready for download",
            "Bill payment to KPLC successful. Amount KSH 1,200",
            "Cashback of KSH 50 has been added to your account"
        ]
        
        # Phishing messages
        phishing_messages = [
            # English phishing
            "URGENT: Your M-Pesa account will be suspended. Verify now: http://mpesa-verify.com",
            "You won KSH 50,000! Claim your prize: http://bit.ly/mpesa-win-2024",
            "M-PESA: Unusual activity detected. Confirm your PIN: http://mpesa-security.com",
            "Dear Customer, your account needs verification. Click: http://secure-mpesa.com",
            "ALERT: Failed transaction. Re-enter your PIN: http://mpesa-update.com",
            "Congratulations! You won $5,000. Click here: http://tinyurl.com/mpesa-bonus",
            "IMPORTANT: Your account will be deactivated. Update now: http://mpesa-activate.com",
            "SECURITY ALERT: Verify your identity: http://safaricom-security.com",
            
            # Swahili mixed phishing
            "MUHIMU: Akaunti yako imefungwa. Weka PIN yako hapa: http://mpesa-safety.com",
            "UMESHINDWA KSH 100,000! Bofya hapa: http://pesa-taka.com",
            "M-PESA: Tumepata tatizo na akaunti yako. Tafadhali hakikisha: http://mpesa-fix.com",
            "TAARIFA: Akaunti yako imesitishwa. Badilisha PIN: http://mpesa-reset.com",
            
            # French for Francophone Africa
            "URGENT: Votre compte Orange Money sera suspendu. Vérifiez: http://orange-secure.com",
            "Félicitations! Vous avez gagné 50,000 FCFA. Cliquez ici: http://orange-gift.com",
            "ALERTE: Activité suspecte détectée. Confirmez votre PIN: http://orange-verify.com",
            
            # Nigerian context
            "GTBank Alert: Your account has issues. Verify: http://gtbank-secure.com",
            "You won $5,000 from MTN! Click here: http://mtn-rewards.com",
            "URGENT: Your Airtel Money account needs update. Click: http://airtel-verify.com"
        ]
        
        # Generate more samples
        legitimate_samples = legitimate_messages * 3  # 15 * 3 = 45 samples
        phishing_samples = phishing_messages * 2     # 18 * 2 = 36 samples
        
        data = []
        for msg in legitimate_samples:
            data.append({
                'text': msg,
                'label': 0,  # 0 = legitimate
                'type': 'legitimate'
            })
        
        for msg in phishing_samples:
            data.append({
                'text': msg,
                'label': 1,  # 1 = phishing
                'type': 'phishing'
            })
        
        return pd.DataFrame(data)
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep basic ones
        text = re.sub(r'[^a-zA-Z0-9\s\.]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def train_model(self):
        """Train the phishing detection model"""
        try:
            # Generate training data
            df = self.generate_training_data()
            
            # Preprocess text
            df['cleaned_text'] = df['text'].apply(self.preprocess_text)
            
            # Create TF-IDF features
            self.vectorizer = TfidfVectorizer(
                max_features=500,
                stop_words=stopwords.words('english'),
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.9
            )
            
            X = self.vectorizer.fit_transform(df['cleaned_text'])
            y = df['label']
            
            # Train Random Forest model
            self.model = RandomForestClassifier(
                n_estimators=50,
                random_state=42,
                max_depth=10,
                min_samples_split=5,
                class_weight='balanced'
            )
            
            self.model.fit(X, y)
            
            # Calculate training accuracy
            train_accuracy = self.model.score(X, y)
            print(f"✅ Model trained successfully! Accuracy: {train_accuracy:.2%}")
            
            self.is_trained = True
            
            # Save model (optional)
            try:
                import os
                os.makedirs('models', exist_ok=True)
                joblib.dump(self.model, 'models/trained_model.pkl')
                joblib.dump(self.vectorizer, 'models/vectorizer.pkl')
                print("💾 Model saved to disk!")
            except:
                print("⚠ Could not save model, but it's trained and ready!")
            
            return train_accuracy
            
        except Exception as e:
            print(f"❌ Training error: {e}")
            # Fallback to simple rule-based detection
            self.is_trained = False
            return 0
    
    def extract_features(self, text):
        """Extract features for explainability"""
        text_lower = text.lower()
        
        features = {
            'has_url': int('http' in text_lower or 'www.' in text_lower or '.com' in text_lower),
            'has_urgency_words': int(any(word in text_lower for word in ['urgent', 'immediately', 'now', 'muhimu', 'haraka', 'important'])),
            'has_prize_words': int(any(word in text_lower for word in ['won', 'prize', 'reward', 'bonus', 'free', 'shindwa', 'gagné'])),
            'has_verification_words': int(any(word in text_lower for word in ['verify', 'confirm', 'validate', 'hakikisha', 'vérifiez'])),
            'has_suspicious_domain': int(any(domain in text_lower for domain in ['mpesa-verify', 'mpesa-security', 'secure-mpesa', 'bit.ly', 'tinyurl'])),
            'text_length': len(text),
            'keyword_count': sum(1 for keyword in ['verify', 'suspend', 'won', 'prize', 'urgent', 'confirm', 'pin', 'click'] if keyword in text_lower),
            'exclamation_count': text.count('!'),
            'all_caps_ratio': sum(1 for c in text if c.isupper()) / max(1, len(text))
        }
        
        return features
    
    def predict(self, text):
        """Predict if text is phishing"""
        try:
            if not text or not isinstance(text, str) or len(text.strip()) < 5:
                return "INVALID", 0.0, {}
            
            # Preprocess
            cleaned_text = self.preprocess_text(text)
            
            if len(cleaned_text.split()) < 2:
                return "INVALID", 0.0, {}
            
            # Extract features for explanation
            features = self.extract_features(text)
            
            if self.is_trained and self.model is not None:
                # Use ML model
                text_tfidf = self.vectorizer.transform([cleaned_text])
                prediction = self.model.predict(text_tfidf)[0]
                probability = self.model.predict_proba(text_tfidf)[0]
                
                if prediction == 1:
                    result = "PHISHING"
                    confidence = probability[1]
                else:
                    result = "LEGITIMATE"
                    confidence = probability[0]
            else:
                # Fallback to rule-based
                if any(word in cleaned_text for word in ['urgent', 'verify', 'won', 'prize', 'suspend', 'http', 'click']):
                    result = "PHISHING"
                    confidence = 0.85
                else:
                    result = "LEGITIMATE"
                    confidence = 0.90
            
            return result, confidence, features
            
        except Exception as e:
            print(f"Prediction error: {e}")
            # Ultimate fallback
            if 'urgent' in text.lower() or 'verify' in text.lower():
                return "PHISHING", 0.80, {}
            else:
                return "LEGITIMATE", 0.85, {}

# Create global instance
detector = PhishingDetector()