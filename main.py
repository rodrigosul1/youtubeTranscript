from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, VideoUnavailable

app = FastAPI()

# Adicionar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos os domínios (você pode restringir conforme necessário)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_video_id(video_url: str) -> str:
    if "v=" in video_url:
        return video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
        return video_url.split("youtu.be/")[1]
    else:
        raise ValueError("URL inválida")

def generate_transcript(video_id: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'pt'])
        full_text = " ".join([t['text'] for t in transcript])
        return full_text
    except (NoTranscriptFound, VideoUnavailable) as e:
        return {"error": str(e)}

@app.get("/get-transcript/")
def get_transcript(url: str):
    try:
        video_id = extract_video_id(url)
        transcript = generate_transcript(video_id)
        return {"transcript": transcript}
    except ValueError as e:
        return {"error": str(e)}
