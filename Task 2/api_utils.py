import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class OpenRouterAPI:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def generate_response(self, prompt, max_tokens=200):
        """Generate response using OpenRouter API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"API Error: {e}")
            return "AI response generation failed. Please try again."
    
    def generate_user_response(self, rating, review):
        """Generate AI response for user's review"""
        prompt = f"""You are a customer service AI. Respond to this {rating}-star review:

Review: "{review}"

Write a polite, helpful response (2-3 sentences). Be appreciative for positive reviews and empathetic for negative ones."""
        
        return self.generate_response(prompt)
    
    def generate_summary(self, rating, review):
        """Generate summary of the review for admin dashboard"""
        prompt = f"""Summarize this {rating}-star review in one concise sentence:

Review: "{review}"

Provide only the summary, no additional text."""
        
        return self.generate_response(prompt, max_tokens=100)
    
    def generate_recommended_actions(self, rating, review):
        """Generate recommended actions for admin dashboard"""
        prompt = f"""Based on this {rating}-star review, suggest 2-3 actionable steps:

Review: "{review}"

Format as bullet points. Be specific and practical."""
        
        return self.generate_response(prompt, max_tokens=150)