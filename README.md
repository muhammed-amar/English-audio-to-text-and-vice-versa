# Text to Voice and Voice to Text API

## Contributors

- Muhammad Amar
- [Mahmoud Elnagar](https://github.com/Elnagar74)

A FastAPI-based application that provides two main functionalities:
1. Convert English text to speech
2. Convert speech to text

## Features
- Text to Speech: Convert English text to audio
- Speech to Text: Convert audio to text using OpenAI's Whisper model
- RESTful API endpoints
- Automatic file cleanup
- CORS enabled

## Requirements
- Python 3.8+
- Dependencies listed in requirements.txt

## Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Start the server:
```bash
python main.py
```
2. The server will run on http://localhost:8000

## API Endpoints
- POST `/text-to-speech`: Convert text to speech
  - Form data: `text` (English text)
  - Returns: Audio file (MP3)

- POST `/speech-to-text`: Convert speech to text
  - Form data: `audio_file` (Audio file)
  - Returns: JSON with transcribed text

## Note
This application only supports English language for both text-to-speech and speech-to-text conversion. 