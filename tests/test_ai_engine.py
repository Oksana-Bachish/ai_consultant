import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.schemas import ProductAI
from src.ai_engine import get_ai_response

@pytest.fixture
def sample_products():
    return [
        ProductAI(id=1, name='Смартфон Apple Phone 15', price=89990.00),
        ProductAI(id=2, name='Ноутбук MacroBook Air', price=129990.50),
    ]

@pytest.mark.asyncio
@patch('src.ai_engine.client')
async def test_get_ai_response_success(mock_client, sample_products):
    """Проверяем успешный сценарий: контекст собрался, OpenAI ответил"""

    # 1. Настраиваем AsyncMock для имитации ответа от OpenAI
    mock_choice = MagicMock()
    mock_choice.message.content = 'Привет! Рекомендую взять Ноутбук MacroBook Air за 129 990.50 руб. Лэп-топ пушка! 🚀'

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    mock_create = AsyncMock(return_value=mock_response)
    mock_client.chat.completions.create = mock_create


    # 2. Вызываем тестируемую асинхронную функцию
    user_query = 'Посоветуй ноут для работы'
    result = await get_ai_response(user_query, sample_products)

    # 3. Проверяем результат
    assert result == 'Привет! Рекомендую взять Ноутбук MacroBook Air за 129 990.50 руб. Лэп-топ пушка! 🚀'

    # 4. Проверяем, с какими параметрами ушел запрос в OpenAI
    assert mock_create.called
    called_kwargs = mock_create.call_args.kwargs

    assert called_kwargs['model'] == 'gpt-4o-mini'
    assert called_kwargs['temperature'] == 0.7

    # Проверяем, что в системный промпт подставились наши товары
    messages = called_kwargs['messages']
    system_prompt = messages[0]['content']
    user_prompt = messages[1]['content']

    assert user_prompt == user_query
    assert 'Apple Phone 15' in system_prompt
    assert '129,990.50 руб.' in system_prompt


@pytest.mark.asyncio
@patch('src.ai_engine.client.chat.completions.create')
async def test_get_ai_response_api_error(mock_create, sample_products):
    """Проверяем обработку ошибок: если OpenAI бросил исключение"""

    mock_create.side_effect = Exception('Rate limit exceeded')

    result = await get_ai_response('Купить телефон', sample_products)

    assert '🤖 Ошибка при обращении к ИИ: Rate limit exceeded' in result
