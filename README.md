# EmoChat

EmoChat is an AI-powered chatbot designed to detect emotions in conversations and adapt its tone accordingly. It leverages advanced natural language processing techniques to provide empathetic and context-aware responses.

## Features
- **Emotion Detection**: Identifies the emotional tone of user messages.
- **Adaptive Responses**: Generates replies that match the detected emotion.
- **Conversation Logging**: Stores chat history for analysis and improvement.
- **Streamlit Integration**: Provides an interactive web interface for users.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd emoChat
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables:
   - Create a `.env` file in the root directory.
   - Add your OpenRouter API key:
     ```
     OPENROUTER_API_KEY=your_api_key_here
     ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open the app in your browser at `http://localhost:8501`.

3. Start chatting with the bot and experience emotion-aware responses.

## Project Structure
- `app.py`: Main entry point for the Streamlit app.
- `modules/`: Contains core modules for emotion detection, response generation, and logging.
- `conversation_logs.json`: Stores chat history.
- `requirements.txt`: Lists project dependencies.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Built with [Streamlit](https://streamlit.io/).
- Emotion detection powered by advanced NLP models.
