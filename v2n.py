import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.utils import make_chunks
import openai

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def video_to_notes(video_path):
    def extract_audio(video_path, audio_path):
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)

    audio_path = "output_audio.wav"
    extract_audio(video_path, audio_path)

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
    print("transcribing audio")
    transcript = split_and_transcribe_audio(audio_path)
    print("transcription complete")
    print(transcript)

    def generate_notes(text, temperature=0.5):
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Create detailed notes from the following text: {text}"}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content

    notes = generate_notes(transcript)
    print(notes)

respose = video_to_notes("C:\\Users\\Prakhar Agrawal\\PycharmProjects\\AI_Assistant\\How Harvard Decides Who To Reject in 30 Seconds.mp4")