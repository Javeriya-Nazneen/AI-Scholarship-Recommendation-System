"""
AI-Scholar Recommendation Engine
Content-based and Collaborative Filtering for Scholarship Matching
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import joblib
import os
from datetime import datetime


class ScholarshipRecommender:
    """
    Hybrid recommendation system combining:
    - Content-based filtering (profile-scholarship matching)
    - Collaborative filtering (user behavior patterns)
    """
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self.scaler = MinMaxScaler()
        self.model_dir = os.path.join(os.path.dirname(__file__), 'models')
        os.makedirs(self.model_dir, exist_ok=True)
    
    def prepare_student_vector(self, student_profile):
        """Convert student profile to feature vector"""
        features = {
            'gpa': float(student_profile.gpa or 0) / 4.0,  # Normalize to 0-1
            'degree_level': self._encode_degree(student_profile.current_degree),
            'field_match': 1.0,  # Will be calculated per scholarship
            'income_need': self._calculate_income_need(
                getattr(student_profile, 'family_income', None)
            ),
        }
        return features
    
    def prepare_scholarship_vector(self, scholarship):
        """Convert scholarship to feature vector"""
        features = {
            'min_gpa': float(scholarship.min_gpa or 0) / 4.0 if scholarship.min_gpa else 0,
            'degree_level': self._encode_degree(scholarship.degree_level),
            'amount': float(scholarship.amount) / 100000,  # Normalize
            'deadline_proximity': self._calculate_deadline_proximity(scholarship.deadline),
        }
        return features
    
    def calculate_match_score(self, student_profile, scholarship):
        """
        Calculate match score between student and scholarship
        Returns: score (0-100)
        """
        score_components = []
        
        # 1. GPA Match (30% weight)
        gpa_score = self._calculate_gpa_match(student_profile, scholarship)
        score_components.append(('GPA', gpa_score, 0.30))
        
        # 2. Degree Level Match (20% weight)
        degree_score = self._calculate_degree_match(student_profile, scholarship)
        score_components.append(('Degree', degree_score, 0.20))
        
        # 3. Field of Study Match (25% weight)
        field_score = self._calculate_field_match(student_profile, scholarship)
        score_components.append(('Field', field_score, 0.25))
        
        # 4. Financial Need Match (15% weight)
        financial_score = self._calculate_financial_match(student_profile, scholarship)
        score_components.append(('Financial', financial_score, 0.15))
        
        # 5. Country Match (10% weight)
        country_score = 100 if student_profile.country == scholarship.country else 50
        score_components.append(('Country', country_score, 0.10))
        
        # Calculate weighted score
        total_score = sum(score * weight for _, score, weight in score_components)
        
        return round(total_score, 2), score_components
    
    def _calculate_gpa_match(self, student, scholarship):
        """Calculate GPA compatibility score"""
        if not scholarship.min_gpa:
            return 100  # No GPA requirement
        
        if not student.gpa:
            return 50  # Unknown GPA, neutral score
        
        if float(student.gpa) >= float(scholarship.min_gpa):
            # Exceeds requirement - higher score for higher GPA
            excess = float(student.gpa) - float(scholarship.min_gpa)
            return min(100, 80 + (excess * 20))
        else:
            # Below requirement - lower score
            deficit = float(scholarship.min_gpa) - float(student.gpa)
            return max(0, 50 - (deficit * 25))
    
    def _calculate_degree_match(self, student, scholarship):
        """Calculate degree level match"""
        degree_map = {'HS': 1, 'UG': 2, 'PG': 3, 'PHD': 4, 'ALL': 0}
        
        if scholarship.degree_level == 'ALL':
            return 100
        
        student_level = degree_map.get(student.current_degree, 0)
        scholarship_level = degree_map.get(scholarship.degree_level, 0)
        
        if student_level == scholarship_level:
            return 100
        elif abs(student_level - scholarship_level) == 1:
            return 70
        else:
            return 30
    
    def _calculate_field_match(self, student, scholarship):
        """Calculate field of study match using text similarity"""
        if not scholarship.field_of_study:
            return 100  # No field restriction
        
        if not student.field_of_study:
            return 50  # Unknown field, neutral score
        
        # Simple keyword matching
        student_fields = set(student.field_of_study.lower().split(','))
        scholarship_fields = set(scholarship.field_of_study.lower().split(','))
        
        # Check for overlap
        common_fields = student_fields.intersection(scholarship_fields)
        
        if common_fields:
            return 100
        
        # Check for partial matches
        for s_field in student_fields:
            for sc_field in scholarship_fields:
                if s_field.strip() in sc_field.strip() or sc_field.strip() in s_field.strip():
                    return 80
        
        return 40
    
    def _calculate_financial_match(self, student, scholarship):
        """Calculate financial need match"""
        family_income = getattr(student, 'family_income', None)
        if scholarship.scholarship_type == 'need':
            # Need-based scholarship
            if family_income and float(family_income) < 50000:
                return 100
            elif family_income and float(family_income) < 100000:
                return 70
            else:
                return 30
        elif scholarship.scholarship_type == 'merit':
            # Merit-based - GPA matters more
            return 80
        else:
            return 60  # Neutral for other types
    
    def _calculate_income_need(self, annual_income):
        """Calculate income need score (lower income = higher need)"""
        if not annual_income:
            return 0.5
        
        income = float(annual_income)
        if income < 30000:
            return 1.0
        elif income < 60000:
            return 0.7
        elif income < 100000:
            return 0.4
        else:
            return 0.1
    
    def _calculate_deadline_proximity(self, deadline):
        """Calculate deadline proximity score (closer = higher priority)"""
        from datetime import date
        days_left = (deadline - date.today()).days
        
        if days_left < 7:
            return 1.0
        elif days_left < 30:
            return 0.8
        elif days_left < 90:
            return 0.6
        else:
            return 0.4
    
    def _encode_degree(self, degree):
        """Encode degree level to numeric"""
        degree_map = {'HS': 0.25, 'UG': 0.5, 'PG': 0.75, 'PHD': 1.0, 'ALL': 0.5}
        return degree_map.get(degree, 0.5)
    
    def get_recommendations(self, student_profile, scholarships, top_n=10):
        """
        Get top N scholarship recommendations for a student
        
        Args:
            student_profile: StudentProfile object
            scholarships: QuerySet of Scholarship objects
            top_n: Number of recommendations to return
        
        Returns:
            List of tuples (scholarship, match_score, reasons)
        """
        recommendations = []
        
        for scholarship in scholarships:
            score, components = self.calculate_match_score(student_profile, scholarship)
            
            # Generate explanation
            reasons = [f"{name}: {s:.0f}%" for name, s, _ in components if s > 60]
            
            recommendations.append({
                'scholarship': scholarship,
                'match_score': score,
                'reasons': reasons,
                'components': components
            })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return recommendations[:top_n]
    
    def save_model(self, filename='recommender_model.pkl'):
        """Save the recommendation model"""
        model_path = os.path.join(self.model_dir, filename)
        joblib.dump(self, model_path)
        print(f"Model saved to {model_path}")
    
    @classmethod
    def load_model(cls, filename='recommender_model.pkl'):
        """Load a saved recommendation model"""
        model_dir = os.path.join(os.path.dirname(__file__), 'models')
        model_path = os.path.join(model_dir, filename)
        
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            print("No saved model found. Creating new instance.")
            return cls()


# Singleton instance
_recommender_instance = None

def get_recommender():
    """Get or create recommender instance"""
    global _recommender_instance
    if _recommender_instance is None:
        _recommender_instance = ScholarshipRecommender()
    return _recommender_instance
