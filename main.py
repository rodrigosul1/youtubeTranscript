from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

app = FastAPI()

def generate_transcript(video_id):
    try:
        # Tenta obter a transcrição do vídeo
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'pt'])
        full_text = " ".join([t['text'] for t in transcript])
        return full_text
    except Exception as e:
        # Retorna uma mensagem de erro se a transcrição falhar
        return {"error": str(e)}

@app.get("/get-transcript")
async def get_transcript(url: str):
    try:
        # Faz o parse da URL para obter o video_id
        parsed_url = urlparse(url)
        video_id = parse_qs(parsed_url.query).get('v', [None])[0]

        if not video_id:
            return {"error": "Video ID not found in the URL"}

        # Gera a transcrição
        transcript = generate_transcript(video_id)

        # Retorna a transcrição como resposta
        return {"transcript": transcript}
    except Exception as e:
        # Retorna uma mensagem de erro em caso de exceção
        return {"error": str(e)}
