from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import whisper
import uuid
import os
from typing import Optional
import asyncio

# Initialize FastAPI app
app = FastAPI(title="Text to Voice and Voice to Text API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Whisper model for speech recognition
print("Loading Whisper model...")
whisper_model = whisper.load_model("base")

@app.post("/text-to-speech")
async def text_to_speech(text: str = Form(...)):
    """
    Convert English text to speech and return audio file
    """
    try:
        # Generate unique filename
        filename = f"{uuid.uuid4()}.mp3"
        # Convert text to speech
        tts = gTTS(text=text, lang="en")
        tts.save(filename)
        
        # Cleanup function to remove file after sending
        async def cleanup():
            await asyncio.sleep(1)
            if os.path.exists(filename):
                os.remove(filename)
        
        # Return audio file
        response = FileResponse(
            filename,
            media_type="audio/mpeg",
            filename=filename
        )
        
        # Schedule file cleanup
        asyncio.create_task(cleanup())
        
        return response
    except Exception as e:
        print(f"Error in text-to-speech: {str(e)}")
        if os.path.exists(filename):
            os.remove(filename)
        raise

@app.post("/speech-to-text")
async def speech_to_text(audio_file: UploadFile = File(...)):
    """
    Convert speech to text from uploaded audio file
    """
    temp_filename = None
    try:
        # Save uploaded file
        temp_filename = f"temp_{uuid.uuid4()}.mp3"
        with open(temp_filename, "wb") as buffer:
            content = await audio_file.read()
            buffer.write(content)
        
        # Convert speech to text
        result = whisper_model.transcribe(temp_filename)
        
        return {"text": result["text"]}
    except Exception as e:
        print(f"Error in speech-to-text: {str(e)}")
        raise
    finally:
        # Remove temporary file
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 