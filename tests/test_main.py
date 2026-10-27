from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_consult_ai_endpoint_success(mocker):
    mock_get_response = mocker.patch('src.main.get_ai_response', return_value='Вот отличный ноутбук! 💻')

    test_payload = {
        'query': 'Посоветуй ноут',
        'products': [{'id': 1, 'name': 'Ноутбук', 'price': 50000.0}]
    }

    response = client.post('/api/v1/consult', json=test_payload)

    assert response.status_code == 200
    assert response.json()['response'] == 'Вот отличный ноутбук! 💻'

    assert mock_get_response.called

