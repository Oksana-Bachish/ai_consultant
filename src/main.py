import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.ai_engine import get_ai_response
from src.schemas import AIConsultRequest

# Инициализация FastAPI-приложения
app = FastAPI(title='AI Consultant Microservice')

# CORS для запросов из Django-монолита
allowed_origins_raw = os.getenv(
    "ALLOWED_ORIGINS", "http://127.0.0.1:8000,http://localhost:8000"
)
origins = [origin.strip() for origin in allowed_origins_raw.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/api/v1/consult/')
async def consult_ai(payload: AIConsultRequest):
    """Возвращает рекомендацию от ИИ на основе вопроса и списка товаров."""
    ai_text = await get_ai_response(payload.query, payload.products)
    return {'status': 'success', 'response': ai_text}
