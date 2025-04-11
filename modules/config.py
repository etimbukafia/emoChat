"""
This file contains configuration settings for the application.
"""

# Emotions that the system can detect and respond to
EMOTIONS = {
    "anger": {
        "tone": "calming",
        "style_modifiers": ["reassuring", "professional", "solution-focused"],
    },
    "disgust": {
        "tone": "concerned",
        "style_modifiers": ["pragmatic", "unbiased", "respectful"],
    },
    "fear": {
        "tone": "soothing",
        "style_modifiers": ["reassuring", "calm", "supportive"],
    },
    "joy": {
        "tone": "enthusiastic",
        "style_modifiers": ["upbeat", "optimistic", "encouraging"],
    },
    "neutral": {

        "tone": "professional",
        "style_modifiers": ["informative", "balanced", "straightforward"],
    },
    "sadness": {
        "tone": "empathetic",
        "style_modifiers": ["compassionate", "supportive", "understanding"],
    },
    "surprise": {
        "tone": "curious",
        "style_modifiers": ["engaging", "inquisitive", "open-minded"],
    }
}

# Company information for context in responses
COMPANY_INFO = {
    "name": "Paulson & Partners",
    "expertise": ["wealth management", "tax planning", "corporate solutions"],
    "values": ["integrity", "client success", "personalized service", "expertise"]
}

# Model settings
MODEL_CONFIG = {
    "emotion_model": "j-hartmann/emotion-english-distilroberta-base",
    "emotion_threshold": 0.5,  # Confidence threshold for emotion detection
}

# Logging configuration
LOGGING_CONFIG = {
    "log_file": "conversation_logs.json",
    "log_level": "INFO",
}
