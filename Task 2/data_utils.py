import json
import os
from datetime import datetime
import pandas as pd

class DataManager:
    def __init__(self, file_path="reviews.json"):
        self.file_path = file_path
        self.ensure_data_file()
    
    def ensure_data_file(self):
        """Create reviews.json file if it doesn't exist"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def add_review(self, user_rating, user_review, ai_response, ai_summary, ai_actions):
        """Add a new review to the data store"""
        try:
            with open(self.file_path, 'r') as f:
                reviews = json.load(f)
            
            new_review = {
                "id": len(reviews) + 1,
                "timestamp": datetime.now().isoformat(),
                "user_rating": user_rating,
                "user_review": user_review,
                "ai_response": ai_response,
                "ai_summary": ai_summary,
                "ai_actions": ai_actions,
                "status": "pending"
            }
            
            reviews.append(new_review)
            
            with open(self.file_path, 'w') as f:
                json.dump(reviews, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving review: {e}")
            return False
    
    def get_all_reviews(self):
        """Get all reviews from the data store"""
        try:
            with open(self.file_path, 'r') as f:
                reviews = json.load(f)
            return reviews
        except:
            return []
    
    def get_reviews_dataframe(self):
        """Get reviews as pandas DataFrame"""
        reviews = self.get_all_reviews()
        if reviews:
            df = pd.DataFrame(reviews)
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        return pd.DataFrame()
    
    def get_statistics(self):
        """Get statistics about reviews"""
        df = self.get_reviews_dataframe()
        if df.empty:
            return {
                "total_reviews": 0,
                "avg_rating": 0,
                "rating_distribution": {},
                "recent_submissions": 0
            }
        
        # Calculate stats
        stats = {
            "total_reviews": len(df),
            "avg_rating": df['user_rating'].mean(),
            "rating_distribution": df['user_rating'].value_counts().to_dict(),
            "recent_submissions": len(df[df['timestamp'] > pd.Timestamp.now() - pd.Timedelta(hours=24)])
        }
        
        return stats