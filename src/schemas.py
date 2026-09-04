from typing import List
from pydantic import BaseModel


class ProductAI(BaseModel):
    """Модель товара, передаваемого из Django в ИИ‑микросервис."""
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True # Позволяет создавать модель из ORM-объектов


class AIConsultRequest(BaseModel):
    """Входной запрос: вопрос пользователя + список товаров."""
    query: str
    products: List[ProductAI]