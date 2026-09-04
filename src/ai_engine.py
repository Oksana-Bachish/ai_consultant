from typing import List
from openai import AsyncOpenAI
import src.config as config
from src.schemas import ProductAI

# Асинхронный клиент OpenAI
client = AsyncOpenAI(
    api_key=config.AI_API_KEY,
    base_url=config.AI_BASE_URL
)

async def get_ai_response(user_query: str, products: List[ProductAI]) -> str:
    """
    Формирует контекст ассортимента и отправляет запрос в GPT‑4o‑mini.
    Возвращает текстовую рекомендацию.
    """
    # Контекст ассортимента для системного промпта
    products_context = ""
    for p in products:
        products_context += f'- [ID: {p.id}] {p.name} - Цена: {p.price:,.2f} руб.\n'

    # Инструкция для ИИ-модели
    system_instruction = (
        "Ты — топовый, дружелюбный и экспертный гаджет-консультант в интернет-магазине электроники.\n"
        "Твоя задача — помочь покупателю выбрать идеальный девайс на основе его запроса.\n\n"
        "🔥 ЖЕСТКИЕ ПРАВИЛА РАБОТЫ:\n"
        "1. Рекомендуй товары СТРОГО из списка доступного ассортимента ниже. Не придумывай другие бренды или модели.\n"
        "2. В ответе обязательно пиши НАЗВАНИЕ товара и его ЦЕНУ.\n"
        "3. Обосновывай свой выбор сочно, но кратко (2-3 предложения), выделяя главные фичи для покупателя.\n"
        "4. Общайся вежливо, используй уместные эмодзи, не будь занудой.\n"
        "5. Если вопрос не связан с техникой, вежливо возвращай клиента к каталогу\n\n"
        f"📋 ДОСТУПНЫЙ АССОРТИМЕНТ ТОВАРОВ В НАШЕМ МАГАЗИНЕ:\n{products_context}"
    )

    try:
        # Асинхронный запрос к ИИ-модели
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {'role': 'system', 'content': system_instruction},
                {'role': 'user', 'content': user_query}
            ],
            temperature=0.7
        )

        choices = response.choices

        # Унифицированное извлечение контента (поддержка разных форматов ответа)
        if isinstance(choices, list) and len(choices) > 0:
            choice = choices[0]
            if isinstance(choice, dict):
                return choice.get('message', {}).get('content', '')
            else:
                return choice.message.content

        return response.choices.message.content

    except Exception as e:
        return f'🤖 Ошибка при обращении к ИИ: {str(e)}'
