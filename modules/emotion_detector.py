"""
This module handles emotion detection from user input.
"""
from transformers import pipeline
from modules.config import MODEL_CONFIG
import logging


class EmotionDetector:
    """
    Emotion detection model using a pre-trained model.
    """
    def __init__(self):
        """Initialize the emotion detection model."""
        self.model_name = MODEL_CONFIG["emotion_model"]
        self.classifier =  pipeline("text-classification", model=self.model_name, return_all_scores=True)

        # Mapping model outputs to integer labels
        # The model has these labels:
        # ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']
        self.emotion_labels = {
            'anger' : 0,
            'disgust' : 1,
            'fear' : 2,
            'joy' : 3,
            'neutral' : 4,
            'sadness' : 5,
            'surprise' : 6,
        }

    def detect_emotion(self, text):
        """
        Detects the emotion from the user input.

        Args:
            text (str): The user input text.

        Returns:
            str: The detected emotion.
        """
        # Getting the model predictions
        predictions = self.classifier(text)

        # Getting the highest scoring emotion
        emotion = max(predictions[0], key=lambda x: x['score'])['label']

        return emotion
    
    def get_emotion_integer(self, emotion):
        """
        Gets the integer label for the emotion.
        """
        return self.emotion_labels[emotion]
    
    def get_emotion_score(self, text):
        """
        Gets the emotion score from the user input.
        """
        predictions = self.classifier(text)
        return predictions[0]
    
