import streamlit as st
import time
from data_utils import DataManager
from api_utils import OpenRouterAPI

# Page configuration
st.set_page_config(
    page_title="AI Feedback System - User Dashboard",
    page_icon="💬",
    layout="centered"
)

# Initialize API and Data Manager
@st.cache_resource
def init_api():
    return OpenRouterAPI()

@st.cache_resource
def init_data_manager():
    return DataManager("reviews.json")  # Directly in same folder

api = init_api()
data_manager = init_data_manager()

# Custom CSS
st.markdown("""
<style>
    .main {
        max-width: 800px;
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .rating-emoji {
        font-size: 2rem;
        margin: 0 0.5rem;
        cursor: pointer;
    }
    .rating-selected {
        transform: scale(1.2);
        transition: transform 0.2s;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("💬 AI Feedback System")
st.markdown("### User Dashboard")
st.markdown("Share your feedback and get an AI-powered response!")

# Initialize session state
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'ai_response' not in st.session_state:
    st.session_state.ai_response = ""
if 'current_rating' not in st.session_state:
    st.session_state.current_rating = 3

# Rating selection
st.markdown("### ⭐ Rate your experience")
st.markdown("Select a rating from 1 (poor) to 5 (excellent):")

# Create 5 columns for rating emojis
cols = st.columns(5)
rating_emojis = ["😠", "🙁", "😐", "🙂", "😄"]
for i, col in enumerate(cols):
    with col:
        rating_value = i + 1
        if st.button(f"{rating_emojis[i]}", key=f"rating_{rating_value}"):
            st.session_state.current_rating = rating_value

# Display selected rating
st.markdown(f"**Selected Rating:** {st.session_state.current_rating} {rating_emojis[st.session_state.current_rating - 1]}")

# Review text input
st.markdown("### 📝 Write your review")
user_review = st.text_area(
    "Share your detailed feedback:",
    placeholder="What did you like or dislike about your experience?",
    height=150,
    max_chars=500
)

# Submit button
if st.button("Submit Feedback", type="primary"):
    if not user_review.strip():
        st.error("Please write a review before submitting.")
    else:
        with st.spinner("🤖 AI is generating a response..."):
            # Generate AI responses
            ai_response = api.generate_user_response(
                st.session_state.current_rating, 
                user_review
            )
            ai_summary = api.generate_summary(
                st.session_state.current_rating, 
                user_review
            )
            ai_actions = api.generate_recommended_actions(
                st.session_state.current_rating, 
                user_review
            )
            
            # Save to database
            success = data_manager.add_review(
                st.session_state.current_rating,
                user_review,
                ai_response,
                ai_summary,
                ai_actions
            )
            
            if success:
                st.session_state.submitted = True
                st.session_state.ai_response = ai_response
                st.success("✅ Feedback submitted successfully!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Failed to save feedback. Please try again.")

# Display AI response after submission
if st.session_state.submitted and st.session_state.ai_response:
    st.markdown("---")
    st.markdown("### 🤖 AI Response")
    
    # Display in a nice container
    st.markdown(f"""
    <div style='
        padding: 1.5rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    '>
        {st.session_state.ai_response}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    
    # Get and display statistics
    stats = data_manager.get_statistics()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Reviews", stats["total_reviews"])
    with col2:
        st.metric("Average Rating", f"{stats['avg_rating']:.1f}")
    with col3:
        st.metric("Recent (24h)", stats["recent_submissions"])
    
    # Reset button
    if st.button("Submit Another Review"):
        st.session_state.submitted = False
        st.session_state.ai_response = ""
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Powered by OpenRouter AI • All feedback is stored in reviews.json</p>
</div>
""", unsafe_allow_html=True)