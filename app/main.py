import streamlit as st
import pandas as pd
import plotly.express as px
import time
from model import detector

# Page configuration
st.set_page_config(
    page_title="PhishGuard Africa",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #A23B72;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .phishing-alert {
        background-color: #FFE6E6;
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #FF4444;
        margin: 20px 0;
    }
    .legitimate-alert {
        background-color: #E6FFE6;
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #44FF44;
        margin: 20px 0;
    }
    .feature-box {
        background-color: #F0F8FF;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #2E86AB;
    }
    .stButton button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🛡 PhishGuard Africa</h1>', unsafe_allow_html=True)
    st.markdown("### AI-Powered Mobile Money Phishing Detection")
    st.markdown("Protecting African users from SMS phishing attacks in multiple languages")
    
    # Sidebar
    st.sidebar.title("🌍 Navigation")
    app_mode = st.sidebar.selectbox("Choose Mode", 
        ["Single Message Check", "Batch Analysis", "About Project"])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Quick Tips")
    st.sidebar.info("""
    *Phishing Indicators:*
    - Urgent action required
    - Prize or money claims  
    - Suspicious links
    - PIN or password requests
    - Grammar mistakes
    - Unknown sender numbers
    """)
    
    if app_mode == "Single Message Check":
        single_message_check()
    elif app_mode == "Batch Analysis":
        batch_analysis()
    else:
        about_project()

def single_message_check():
    st.markdown('<div class="sub-header">🔍 Check Single SMS Message</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        input_method = st.radio("Choose input method:", 
            ["Type Message", "Use Example"])
        
        if input_method == "Type Message":
            message = st.text_area("Paste SMS message here:", 
                height=150, 
                placeholder="Enter SMS message to analyze...\nExample: URGENT: Your M-Pesa account will be suspended. Verify now: http://mpesa-verify.com",
                key="message_input")
        else:
            example_messages = {
                "Select Example": "",
                "Phishing Example (English)": "URGENT: Your M-Pesa account will be suspended. Verify now: http://mpesa-verify.com",
                "Phishing Example (Swahili)": "MUHIMU: Akaunti yako imefungwa. Weka PIN yako hapa: http://mpesa-safety.com",
                "Phishing Example (French)": "URGENT: Votre compte Orange Money sera suspendu. Vérifiez: http://orange-secure.com",
                "Legitimate Example": "You have received KSH 2,500 from John Doe. New balance is KSH 3,950.50"
            }
            
            selected_example = st.selectbox("Choose example:", list(example_messages.keys()))
            message = st.text_area("SMS message:", 
                value=example_messages[selected_example], 
                height=150,
                key="example_input")
    
    with col2:
        st.markdown("### 🎯 Detection Features")
        st.markdown("""
        *Phishing Indicators:*
        🔴 Urgency words
        🔴 Prize claims  
        🔴 Suspicious links
        🔴 PIN requests
        🔴 Verification demands
        
        *Legitimate Signs:*
        🟢 Transaction details
        🟢 Balance updates
        🟢 Confirmation messages
        🟢 Official sender IDs
        """)
    
    if st.button("🚀 Analyze Message", type="primary", use_container_width=True):
        if message and message.strip():
            with st.spinner("🔄 Analyzing message for phishing indicators..."):
                time.sleep(1)  # Small delay for better UX
                
                # Get prediction
                result, confidence, features = detector.predict(message)
                
                # Display results
                st.markdown("---")
                st.markdown("## 📊 Analysis Results")
                
                # Result alert
                if result == "PHISHING":
                    st.markdown(f"""
                    <div class="phishing-alert">
                        <h2>🚨 PHISHING ATTEMPT DETECTED</h2>
                        <h3>Confidence: {confidence:.2%}</h3>
                        <p><strong>⚠ Warning:</strong> This message shows strong characteristics of phishing attempts. Do not click any links or provide personal information.</p>
                        <p><strong>🔒 Safety Tips:</strong></p>
                        <ul>
                            <li>Do not click any links in the message</li>
                            <li>Do not provide your PIN or password</li>
                            <li>Contact your mobile money provider directly</li>
                            <li>Delete the message immediately</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                elif result == "LEGITIMATE":
                    st.markdown(f"""
                    <div class="legitimate-alert">
                        <h2>✅ LEGITIMATE MESSAGE</h2>
                        <h3>Confidence: {confidence:.2%}</h3>
                        <p><strong>✓ This message appears to be legitimate.</strong> However, always verify with your mobile money provider if unsure.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Unable to analyze this message. Please check the input.")
                    return
                
                # Confidence visualization
                st.markdown("### Confidence Level")
                progress_color = "red" if result == "PHISHING" else "green"
                
                col_prog1, col_prog2 = st.columns([3, 1])
                with col_prog1:
                    st.progress(confidence)
                with col_prog2:
                    st.metric("Confidence", f"{confidence:.2%}")
                
                # Feature analysis
                st.markdown("### 🔍 Feature Analysis")
                
                # Create feature columns
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("URL Detected", "✅" if features.get('has_url', 0) else "❌")
                    st.metric("Urgency Words", "✅" if features.get('has_urgency_words', 0) else "❌")
                
                with col2:
                    st.metric("Prize Mentions", "✅" if features.get('has_prize_words', 0) else "❌")
                    st.metric("Verification Request", "✅" if features.get('has_verification_words', 0) else "❌")
                
                with col3:
                    st.metric("Suspicious Domain", "✅" if features.get('has_suspicious_domain', 0) else "❌")
                    st.metric("Text Length", features.get('text_length', 0))
                
                with col4:
                    st.metric("Phishing Keywords", features.get('keyword_count', 0))
                    st.metric("Exclamation Marks", features.get('exclamation_count', 0))
        
        else:
            st.warning("Please enter a message to analyze.")

def batch_analysis():
    st.markdown('<div class="sub-header">📊 Batch SMS Analysis</div>', unsafe_allow_html=True)
    
    st.info("""
    *Upload a CSV file* with multiple SMS messages for bulk analysis. 
    Your file should have a column named *'message'* containing the SMS texts.
    
    Don't have a CSV? Use the single message checker above.
    """)
    
    # Sample CSV data for download
    sample_data = pd.DataFrame({
        'message': [
            "You have received KSH 2,500 from John Doe",
            "URGENT: Your account will be suspended. Verify now",
            "Your balance is KSH 1,500.50",
            "You won KSH 50,000! Claim your prize",
            "Payment to merchant successful"
        ]
    })
    
    csv = sample_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Sample CSV",
        data=csv,
        file_name="sample_sms_messages.csv",
        mime="text/csv"
    )
    
    uploaded_file = st.file_uploader("Choose CSV file", type="csv", key="batch_upload")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            if 'message' not in df.columns:
                st.error("❌ CSV file must contain a 'message' column")
                return
            
            st.success(f"✅ Loaded {len(df)} messages successfully!")
            
            # Show sample data
            with st.expander("👀 Preview Uploaded Data"):
                st.dataframe(df.head())
            
            if st.button("🔍 Analyze All Messages", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                results = []
                
                for i, message in enumerate(df['message']):
                    status_text.text(f"Analyzing message {i+1}/{len(df)}...")
                    result, confidence, features = detector.predict(str(message))
                    
                    results.append({
                        'message': message,
                        'prediction': result,
                        'confidence': confidence,
                        'has_url': features.get('has_url', 0),
                        'has_urgency': features.get('has_urgency_words', 0),
                        'has_prize': features.get('has_prize_words', 0),
                        'keyword_count': features.get('keyword_count', 0)
                    })
                    
                    progress_bar.progress((i + 1) / len(df))
                
                status_text.text("✅ Analysis complete!")
                
                results_df = pd.DataFrame(results)
                
                # Display results summary
                st.markdown("## 📈 Results Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                phishing_count = len(results_df[results_df['prediction'] == 'PHISHING'])
                legitimate_count = len(results_df[results_df['prediction'] == 'LEGITIMATE'])
                total_count = len(results_df)
                
                with col1:
                    st.metric("Total Messages", total_count)
                with col2:
                    st.metric("Phishing Detected", phishing_count)
                with col3:
                    st.metric("Legitimate", legitimate_count)
                with col4:
                    if total_count > 0:
                        phishing_percent = (phishing_count / total_count) * 100
                        st.metric("Phishing Rate", f"{phishing_percent:.1f}%")
                    else:
                        st.metric("Phishing Rate", "0%")
                
                # Visualization
                if total_count > 0:
                    col_viz1, col_viz2 = st.columns(2)
                    
                    with col_viz1:
                        # Pie chart
                        fig_pie = px.pie(
                            names=['Phishing', 'Legitimate'],
                            values=[phishing_count, legitimate_count],
                            title="Message Classification Distribution",
                            color=['Phishing', 'Legitimate'],
                            color_discrete_map={'Phishing':'red', 'Legitimate':'green'}
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    with col_viz2:
                        # Confidence distribution
                        fig_hist = px.histogram(
                            results_df, 
                            x='confidence',
                            color='prediction',
                            title='Confidence Score Distribution',
                            color_discrete_map={'PHISHING':'red', 'LEGITIMATE':'green'}
                        )
                        st.plotly_chart(fig_hist, use_container_width=True)
                
                # Show results table
                st.markdown("### 📋 Detailed Results")
                st.dataframe(results_df)
                
                # Download results
                csv_results = results_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv_results,
                    file_name="phishing_analysis_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
        except Exception as e:
            st.error(f"❌ Error processing file: {e}")

def about_project():
    st.markdown('<div class="sub-header">🌍 About PhishGuard Africa</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 The Problem
    
    Mobile money phishing (smishing) is a massive threat across Africa:
    
    *💰 Financial Impact:*
    - Users lose millions annually to SMS scams
    - Erodes trust in digital financial services
    - Hinders financial inclusion efforts
    
    *🌍 Regional Challenges:*
    - Multi-language phishing attacks (English, Swahili, French)
    - Limited cybersecurity awareness
    - Evolving scam techniques
    - Cross-border fraud networks
    """)
    
    st.markdown("""
    ### 💡 Our Solution
    
    *PhishGuard Africa* uses advanced AI to protect users by:
    
    *🔍 Intelligent Detection:*
    - Real-time SMS analysis
    - Multi-language support
    - Context-aware phishing indicators
    - Explainable AI decisions
    
    *🛡 Proactive Protection:*
    - Batch message scanning
    - Confidence scoring
    - Detailed threat analysis
    - Educational insights
    """)
    
    st.markdown("""
    ### 🚀 Technology Stack
    
    *Backend & AI:*
    - Python & Scikit-learn
    - Random Forest Algorithm
    - TF-IDF Vectorization
    - Custom Feature Engineering
    
    *Frontend:*
    - Streamlit Web Framework
    - Plotly Visualizations
    - Responsive Design
    
    *African Context:*
    - Regional mobile money knowledge
    - Local language processing
    - Cultural context integration
    """)
    
    st.markdown("""
    ### 📞 Get Involved
    
    This project is built for *AI Afrihackbox* to address real cybersecurity 
    challenges in Africa's digital finance ecosystem.
    
    *🌐 GitHub:* [Your Repository Link]
    *📧 Contact:* [Your Email]
    *🎯 Hackathon:* AI Afrihackbox Submission
    """)

if _name_ == "_main_":
    main()