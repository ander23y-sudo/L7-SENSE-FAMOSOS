# L7 SENSE FAMOSOS — servidor Python

API inicial em FastAPI para receber links do TikTok.

## Limitação importante
O endpoint público oEmbed do TikTok fornece metadados/embeds, não os frames do vídeo nem as configurações de sensibilidade do Free Fire. Portanto, esta versão valida o link e retorna metadados quando disponíveis, mas **não inventa valores de sensibilidade**.

Para uma estimativa real será necessário implementar uma etapa autorizada de receção/análise de imagens ou frames do vídeo.

## Executar localmente
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Render
Build command:
`pip install -r requirements.txt`

Start command:
`uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Health check:
`/health`
