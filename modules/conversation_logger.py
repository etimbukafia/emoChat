"""
This module handles logging of conversations for analysis and improvement.
"""

import json
import logging
import os
from datetime import datetime
from modules.config import LOGGING_CONFIG

class ConversationLogger:
    def __init__(self):
        """Initialize the conversation logger."""
        self.log_file = LOGGING_CONFIG["log_file"]
        
        # Set up logging
        logging.basicConfig(
            level=getattr(logging, LOGGING_CONFIG["log_level"]),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("PaulsonAI")
        
    def log_interaction(self, user_input, detected_emotion, emotion_scores, response):
        """
        Log a conversation interaction.
        
        Args:
            user_input (str): The user's input text
            detected_emotion (str): The detected emotion
            emotion_scores (dict): Detailed emotion scores
            response (str): The generated response
        """
        # Create log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "detected_emotion": detected_emotion,
            "emotion_scores": emotion_scores,
            "response": response
        }
        
        # Log to file
        try:
            # Create file if it doesn't exist
            if not os.path.exists(self.log_file):
                with open(self.log_file, "w") as f:
                    json.dump([], f)
            
            # Read existing logs
            with open(self.log_file, "r") as f:
                logs = json.load(f)
            
            # Add new log entry
            logs.append(log_entry)
            
            # Write updated logs
            with open(self.log_file, "w") as f:
                json.dump(logs, f, indent=2)
                
            self.logger.info(f"Logged interaction with emotion: {detected_emotion}")
            
        except Exception as e:
            self.logger.error(f"Error logging interaction: {str(e)}")
            
    def get_conversation_analytics(self):
        """
        Get analytics on past conversations.
        
        Returns:
            dict: Analytics data
        """
        try:
            if not os.path.exists(self.log_file):
                return {"total_interactions": 0}
                
            with open(self.log_file, "r") as f:
                logs = json.load(f)
                
            total_interactions = len(logs)
            
            # Count emotions
            emotion_counts = {}
            for log in logs:
                emotion = log.get("detected_emotion", "unknown")
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                
            return {
                "total_interactions": total_interactions,
                "emotion_distribution": emotion_counts
            }
            
        except Exception as e:
            self.logger.error(f"Error getting analytics: {str(e)}")
            return {"total_interactions": 0, "error": str(e)}