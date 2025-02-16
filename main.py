from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydub import AudioSegment
from pydub.utils import make_chunks
import openai
import yt_dlp
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()

# Define a Pydantic model for the request body
class YouTubeURLRequest(BaseModel):
    youtube_url: str

def download_youtube_audio(url, audio_path):
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best available audio quality
        'outtmpl': audio_path.replace('.wav', ''),  # Remove .wav extension from outtmpl
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Extract audio using FFmpeg
            'preferredcodec': 'wav',  # Convert to WAV format
            'preferredquality': '192',  # Set audio quality
        }],
        'quiet': True,  # Suppress output logs
        'cookiefile': 'cookies.txt'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_audio_chunk(audio_chunk, chunk_number):
    chunk_path = f"chunk{chunk_number}.wav"  # Ensure the file has a .wav extension
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
        audio_path = "output_audio.wav"

        # Download the YouTube audio
        print("Downloading audio...")
        download_youtube_audio(youtube_url, audio_path)
        print("Audio downloaded.")

        # Transcribe the audio
        print("Transcribing audio...")
        transcript = split_and_transcribe_audio(audio_path)
        print("Transcription complete.")

        # Generate notes from the transcription
        print("Generating notes...")
        notes = generate_notes(transcript)
        print("Notes generated.")

        # Clean up temporary files
        os.remove(audio_path)

        return {"notes": notes}

    except Exception as e:
        # Clean up the temporary file in case of an error
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0")