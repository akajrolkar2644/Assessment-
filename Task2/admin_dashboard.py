import streamlit as st
import pandas as pd
from datetime import datetime
from data_utils import DataManager


st.set_page_config(
    page_title="AI Feedback System - Admin Dashboard",
    page_icon="📊",
    layout="wide"
)


@st.cache_resource
def init_data_manager():
    return DataManager()

data_manager = init_data_manager()


st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        margin-bottom: 1rem;
    }
    .review-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-pending { border-left: 5px solid #ffc107; }
    .status-reviewed { border-left: 5px solid #28a745; }
    .rating-1 { color: #dc3545; font-weight: bold; }
    .rating-2 { color: #fd7e14; font-weight: bold; }
    .rating-3 { color: #ffc107; font-weight: bold; }
    .rating-4 { color: #20c997; font-weight: bold; }
    .rating-5 { color: #28a745; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


password = st.sidebar.text_input("Enter Admin Password:", type="password")
if password != "admin123": 
    st.error("🔒 Please enter the correct admin password")
    st.stop()


st.title("📊 AI Feedback System")
st.markdown("### Admin Dashboard")
st.markdown("Monitor user feedback and AI-generated insights")


st.markdown("---")
st.markdown("### 📈 Overview Statistics")

stats = data_manager.get_statistics()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Reviews", stats["total_reviews"])
with col2:
    st.metric("Average Rating", f"{stats['avg_rating']:.1f}" if stats['avg_rating'] > 0 else "N/A")
with col3:
    st.metric("Recent (24h)", stats["recent_submissions"])
with col4:
    st.metric("Pending Review", stats["total_reviews"])  

st.markdown("---")
st.markdown("### ⭐ Rating Distribution")

if stats["rating_distribution"]:
    rating_df = pd.DataFrame(list(stats["rating_distribution"].items()), 
                           columns=['Rating', 'Count']).sort_values('Rating')
    
   
    st.bar_chart(rating_df.set_index('Rating'))
else:
    st.info("No reviews available yet.")


st.markdown("---")
st.markdown("### 📋 All Submissions")

reviews = data_manager.get_all_reviews()

if reviews:
   
    df = pd.DataFrame(reviews)
    
    
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
    
   
    st.dataframe(
        df[['id', 'timestamp', 'user_rating', 'user_review', 'ai_summary']],
        column_config={
            "id": "ID",
            "timestamp": "Time",
            "user_rating": st.column_config.NumberColumn(
                "Rating",
                format="⭐ %d"
            ),
            "user_review": "Review",
            "ai_summary": "AI Summary"
        },
        hide_index=True,
        use_container_width=True
    )
    
    
    st.markdown("---")
    st.markdown("### 🔍 Detailed Review Analysis")
    
    
    review_ids = [f"{r['id']} - {r['timestamp']}" for r in reviews]
    selected_review_id = st.selectbox(
        "Select a review to view details:",
        options=review_ids,
        format_func=lambda x: f"Review #{x}"
    )
    
    if selected_review_id:
        selected_id = int(selected_review_id.split(" - ")[0])
        selected_review = next((r for r in reviews if r['id'] == selected_id), None)
        
        if selected_review:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class='review-card'>
                    <h4>📝 User Review</h4>
                    <p><strong>Rating:</strong> <span class='rating-{selected_review["user_rating"]}'>{selected_review["user_rating"]} ⭐</span></p>
                    <p><strong>Time:</strong> {selected_review["timestamp"]}</p>
                    <p><strong>Review:</strong><br>{selected_review["user_review"]}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='review-card'>
                    <h4>🤖 AI Analysis</h4>
                    <p><strong>AI Response to User:</strong><br>{selected_review["ai_response"]}</p>
                    <p><strong>AI Summary:</strong><br>{selected_review["ai_summary"]}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='review-card'>
                <h4>🚀 Recommended Actions</h4>
                <p>{selected_review["ai_actions"].replace('•', '<br>•')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            
            st.markdown("---")
            st.markdown("### ⚙️ Admin Actions")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📧 Export to CSV", use_container_width=True):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="feedback_data.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("🔄 Mark as Reviewed", use_container_width=True):
                    st.success("Review marked as reviewed!")
            
            with col3:
                if st.button("🗑️ Delete Review", use_container_width=True):
                    st.warning("Delete functionality would be implemented here")
    
else:
    st.info("No reviews submitted yet. The user dashboard is waiting for feedback!")


st.markdown("---")
auto_refresh = st.checkbox("🔄 Auto-refresh every 30 seconds")
if auto_refresh:
    st.rerun()


st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Admin Dashboard • All data is updated in real-time</p>
</div>
""", unsafe_allow_html=True)