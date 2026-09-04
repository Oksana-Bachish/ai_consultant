import os
from pathlib import Path
from dotenv import load_dotenv

# Базовая директория проекта (для поиска .env)
BASE_DIR = Path(__file__).resolve().parent.parent

# Загрузка переменных окружения
load_dotenv(dotenv_path=BASE_DIR/'.env.dev')

# Настройки доступа к AI‑модели
AI_API_KEY = os.getenv("AI_API_KEY")
AI_BASE_URL = os.getenv("AI_BASE_URL")
