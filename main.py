from fastapi import FastAPI, HTTPException, Query
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, VideoUnavailable

app = FastAPI()

def extract_video_id(video_url: str) -> str:
    # Extrair o ID do vídeo da URL do YouTube
    if "v=" in video_url:
        return video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
        return video_url.split("youtu.be/")[1]
    else:
        raise ValueError("URL inválida")

def generate_transcript(video_id: str):
    try:
        # Obter a transcrição em inglês e português, se disponíveis
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'pt'])
        # Juntar todas as falas em um texto único
        full_text = " ".join([t['text'] for t in transcript])
        return full_text
    except (NoTranscriptFound, VideoUnavailable) as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/get-transcript/")
def get_transcript(url: str = Query(..., description="URL do vídeo do YouTube")):
    try:
        video_id = extract_video_id(url)
        transcript = generate_transcript(video_id)
        return {"transcript": transcript}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

