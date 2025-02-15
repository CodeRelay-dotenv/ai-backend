from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydub import AudioSegment
from pydub.utils import make_chunks
import openai
import yt_dlp
from dotenv import load_dotenv
import os
import tempfile  # For temporary file handling

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()

# Define a Pydantic model for the request body
class YouTubeURLRequest(BaseModel):
    youtube_url: str

def download_youtube_audio(url, temp_file_path):
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best available audio quality
        'outtmpl': temp_file_path,  # Save the file to the temporary path
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Extract audio using FFmpeg
            'preferredcodec': 'wav',  # Convert to WAV format
            'preferredquality': '192',  # Set audio quality
        }],
        'quiet': True,  # Suppress output logs
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_audio_chunk(audio_chunk, chunk_number):
    chunk_path = f"chunk{chunk_number}.wav"
    audio_chunk.export(chunk_path, format="wav")
    with open(chunk_path, 'rb') as audio_file:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    os.remove(chunk_path)  # Clean up the chunk file after transcribing
    return response.text

def split_and_transcribe_audio(audio_path):
    audio = AudioSegment.from_wav(audio_path)
    chunk_length_ms = 60000  # 1 minute (60,000 ms)
    chunks = make_chunks(audio, chunk_length_ms)

    transcript = ""
    for i, chunk in enumerate(chunks):
        transcript += transcribe_audio_chunk(chunk, i) + " "

    return transcript

def generate_notes(text, temperature=0.5):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Use the correct model name
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Create detailed notes from the following text: {text}"}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content

@app.post("/generate-notes/")
async def generate_notes_from_youtube(request: YouTubeURLRequest):
    try:
        youtube_url = request.youtube_url

        # Create a temporary file for the audio
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file_path = temp_file.name

        # Download the YouTube audio to the temporary file
        print("Downloading audio...")
        download_youtube_audio(youtube_url, temp_file_path)
        print("Audio downloaded.")

        # Transcribe the audio
        print("Transcribing audio...")
        transcript = split_and_transcribe_audio(temp_file_path)
        print("Transcription complete.")

        # Generate notes from the transcription
        print("Generating notes...")
        notes = generate_notes(transcript)
        print("Notes generated.")

        # Clean up the temporary file
        os.remove(temp_file_path)

        return {"notes": notes}

    except Exception as e:
        # Clean up the temporary file in case of an error
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)