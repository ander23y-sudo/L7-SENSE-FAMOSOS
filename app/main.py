from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from urllib.parse import urlparse
import httpx

app = FastAPI(title="L7 SENSE FAMOSOS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TikTokRequest(BaseModel):
    url: HttpUrl
    device: str = "Não informado"

@app.get("/")
def home():
    return {
        "app": "L7 SENSE FAMOSOS",
        "status": "online"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/analisar-tiktok")
async def analisar_tiktok(payload: TikTokRequest):
    host = (urlparse(str(payload.url)).hostname or "").lower()

    if not (
        host == "tiktok.com"
        or host.endswith(".tiktok.com")
    ):
        raise HTTPException(
            status_code=400,
            detail="Link inválido do TikTok"
        )

    metadata = None

    try:
        async with httpx.AsyncClient(
            timeout=15,
            follow_redirects=True
        ) as client:
            response = await client.get(
                "https://www.tiktok.com/oembed",
                params={"url": str(payload.url)}
            )
            response.raise_for_status()
            metadata = response.json()
    except Exception:
        pass

    return {
        "status": "metadata_only",
        "device": payload.device,
        "creator": metadata.get("author_name") if metadata else None,
        "video_title": metadata.get("title") if metadata else None,
        "message": (
            "Link recebido. Os metadados públicos do TikTok "
            "não permitem descobrir a sensibilidade do jogador. "
            "É necessária uma análise autorizada das imagens do vídeo."
        )
  }
