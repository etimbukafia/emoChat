"""
Main Streamlit application for the Paulson & Partners AI Assistant.
"""

import streamlit as st
from modules.emotion_detector import EmotionDetector
from modules.response_generator import ResponseGenerator
from modules.conversation_logger import ConversationLogger
import whisper
import tempfile

# Set page configuration
st.set_page_config(
    page_title="Paulson & Partners AI Assistant",
    page_icon="💼",
    layout="centered" 
)

# Initialize components
@st.cache_resource
def load_emotion_detector():
    return EmotionDetector()

@st.cache_resource
def load_whisper():
    model = whisper.load_model("turbo")
    return model

# Function to get emotion color
def get_emotion_color(emotion):
    emotion_colors = {
        "anger": "#e74c3c",     # Red
        "disgust": "#8e44ad",   # Purple
        "fear": "#f39c12",      # Orange
        "joy": "#76b852",       # Green
        "neutral": "#95a5a6",   # Gray
        "sadness": "#3498db",   # Blue
        "surprise": "#f1c40f"   # Yellow
    }
    return emotion_colors.get(emotion, "#95a5a6")  # Default to gray


def main():
    # Initializing components
    emotion_detector = load_emotion_detector()
    response_generator = ResponseGenerator()
    conversation_logger = ConversationLogger()
    whisper_model = load_whisper()

    # Page header
    st.title("Paulson & Partners AI Assistant")
    st.subheader("Your Private Financial Consultation Partner")

    # Initialize session state for conversation history
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    # Sidebar with information
    with st.sidebar:
        st.header("About Us")
        st.write("""
        Paulson & Partners specializes in comprehensive wealth management, 
        tax planning, and corporate solutions tailored to your unique needs.
        """)
        
        st.header("How to Use")
        st.write("""
        Simply type your question in the chat box below and our AI assistant 
        will provide you with personalized guidance for your financial needs.
        """)

        if st.button("Reset Conversation"):
            st.session_state.conversation = []
            st.experimental_rerun()
        
        # Analytics section in sidebar
        st.header("Conversation Analytics")
        analytics = conversation_logger.get_conversation_analytics()
        st.write(f"Total Interactions: {analytics['total_interactions']}")
        
        if "emotion_distribution" in analytics and analytics["total_interactions"] > 0:
            st.subheader("Emotion Distribution")
            for emotion, count in analytics["emotion_distribution"].items():
                percentage = (count / analytics["total_interactions"]) * 100
                st.write(f"{emotion.capitalize()}: {percentage:.1f}%")

    # Display conversation history
    for message in st.session_state.conversation:
        role = message["role"]
        content = message["content"]

        if role == "user":
            st.chat_message("user").write(content)
        else:
            #something looks wrong here
            emotion = message.get("emotion", "neutral")
            emotion_color = get_emotion_color(emotion)
            with st.chat_message("consultant"):
                st.markdown(f"<div style='background-color: {emotion_color}; padding: 10px; border-radius: 5px;'>{content}</div>", unsafe_allow_html=True)
                st.caption(f"Detected emotion: {emotion.capitalize()}")



    # Chat input
    user_input = st.chat_input("Type your message here...")
    # Accepting Audio Input
    audio_file = st.audio_input("Let us hear you out...")

    if audio_file:
        st.audio(audio_file)
        audio = whisper_model.transcribe(audio_file)
        user_input = audio["text"]

    if user_input:
        # Add user message to conversation
        st.session_state.conversation.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        # Detect emotion
        with st.spinner("Analyzing..."):
            detected_emotion = emotion_detector.detect_emotion(user_input)
            emotion_scores = emotion_detector.get_emotion_score(user_input)
        
        # Generate response
        with st.spinner("Generating response..."):
            response = response_generator.generate_response(user_input, detected_emotion)
        
        try:
            # Log interaction
            conversation_logger.log_interaction(user_input, detected_emotion, emotion_scores, response)
        except Exception as e:
            st.error(f"Error logging interaction: {e}")
        
        # Add assistant message to conversation
        st.session_state.conversation.append({
            "role": "assistant", 
            "content": response,
            "emotion": detected_emotion
        })
        
        # Display assistant response
        emotion_color = get_emotion_color(detected_emotion)  
        with st.chat_message("assistant"):
            st.markdown(f"<div style='background-color: {emotion_color}; padding: 10px; border-radius: 5px;'>{response}</div>", unsafe_allow_html=True)
            st.caption(f"Detected emotion: {detected_emotion.capitalize()}")
        
        # Auto-scroll to the bottom
        st.rerun()

if __name__ == "__main__":
    main()  
