CONFIG = {
    "ENV": "dev",
    "APP_NAME": "app",
    "APP_VERSION": "1.0.0",
    "APP_PORT": 8080,
    "LOG_DIR": "./logs",
}
FEEDS = [
    {
        "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "filter_data": [],
        "field_mapping": {"text":["title", "description", "media:description", "category"]},
        "model_saved": "",
        "promt_request": "scins",
        "timeout": 360
    }
]
PROMTS = {
    "scins": {
        "role": "Ассистент, отвечающий на вопросы",
        "response_type": "технический",
        "response_style": "формальный",
        "response_tone": "нейтральный",
        "response_depth": "развернутый",
        "target_audience": "разработчик",
        "response_format": "абзацы",
        "context": "известны базовые термины программирования",
        "language_and_terms": "узкоспециальный",
        "examples": "по необходимости",
        "response_length": "средний",
        "uncertainty_level": "точный ответ",
        "creativity_level": "логичный",
        "information_sources": "не указывается",
        "formatting": "минимальное форматирование"
    },
}
MODELS = {
    "subject": "Компания X",  # Субъект (главная сущность)
    "actions": ["купила доллары", "запустила новый продукт"],  # Действия/Протекания
    "object_of_action": ["доллары", "новый продукт"],  # Объект действия
    "locations": ["Нью-Йорк", "Лондон"],  # Локации
    "positive_or_negative": "положительное"  # Положительное/Отрицательное для субъекта
}