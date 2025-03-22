from abc import ABC, abstractmethod
import numpy as np

class ModelPrediction(ABC):
    @abstractmethod
    def train(self, X, y):
        pass
    
    @abstractmethod
    def predict(self, X):
        pass

class PredictionModel(ModelPrediction):
    def __init__(self):
        self.weights = {
            'gpa': 0.4,
            'attendance': 0.2,
            'credits': 0.15,
            'study_hours': 0.15,
            'extracurricular': 0.05,
            'internship': 0.05
        }
    
    def train(self, X, y):
        # Implement actual training logic here
        pass
    
    def predict(self, features):
        """
        Calculate graduation probability based on weighted features
        """
        score = 0
        
        # Calculate GPA contribution (0-4 scale)
        score += (features['gpa'] / 4.0) * self.weights['gpa']
        
        # Calculate attendance contribution (0-100 scale)
        score += (features['attendance'] / 100) * self.weights['attendance']
        
        # Calculate credits contribution (assuming 120 credits is target)
        score += min(features['credits'] / 120, 1.0) * self.weights['credits']
        
        # Calculate study hours contribution (assuming 40 hours is max)
        score += min(features['study_hours'] / 40, 1.0) * self.weights['study_hours']
        
        # Calculate extracurricular contribution
        extra_scores = {'None': 0, 'Low': 0.3, 'Medium': 0.7, 'High': 1.0}
        score += extra_scores[features['extracurricular']] * self.weights['extracurricular']
        
        # Add internship bonus
        if features['internship']:
            score += self.weights['internship']
        
        return min(score, 1.0)  # Ensure probability doesn't exceed 1.0 