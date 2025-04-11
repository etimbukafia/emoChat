"""
This module generates responses based on detected emotions and user queries.
"""

from modules.config import EMOTIONS, COMPANY_INFO
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class ResponseGenerator:
    def __init__(self, api_key=None):
        """Initialize the response generator with company information and emotion settings."""
        self.company_info = COMPANY_INFO
        self.emotion_tones = EMOTIONS

        # Get the API key from the user
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")

        # Initialize the client if we have an API key
        self.client = None
        if self.api_key:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )
        
    def generate_response(self, user_input, detected_emotion):
        """
            Generate a response based on the user's input and detected emotion.
            
            Args:
                user_input (str): The user's input text
                detected_emotion (str): The detected emotion from the user's input

            Returns:
                str: The generated response
        """
        if not self.client:
            return "API client not initialized. Please provide an API key."
        
        # Get the tone  for the detected emotion
        tone = self.emotion_tones[detected_emotion]["tone"]
        style = ", ".join(self.emotion_tones[detected_emotion]["style_modifiers"])
        company_name = self.company_info["name"]
        company_expertise = ", ".join(self.company_info["expertise"])
        company_values = ", ".join(self.company_info["values"])


        # using the tone, style, and openRouter api to generate a response
        completion = self.client.chat.completions.create(
            extra_headers={},
            extra_body={},
            model="meta-llama/llama-4-scout:free",
            messages=[
                {"role": "system", 
                "content": [
                    {
                        "type": "text", 
                        "text": f"""
                        You are a helpful consultant assitant for {company_name}.
                        You are an expert in {company_expertise}, if the user doesn't ask about your expertise, reply with, "I'm sorry, I can only help with {company_expertise}."
                        The company's values are {company_values} and you should always maintain these values in your responses.
                        You will use the tone: {tone} and style: {style} to respond to the user.
                        Be dynamic but helpful.
                        """
                    }
                ]
                },
                {"role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": user_input
                    }
                ]
                }
            ]
        )

        response = completion.choices[0].message.content

        return response