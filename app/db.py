from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from .models import Base, Feed, Model, Prompt

class Database:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url)
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def create_table(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def insert_record(self, model_cls, data: dict):
        async with self.async_session() as session:
            try:
                session.add(model_cls(**data))
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise
            except Exception:
                await session.rollback()
                raise

    async def initialize_data(self):
            feeds_data = [
                {
                    "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
                    "filter_data": "b",
                    "field_mapping": "b",
                    "model_saved": "a",
                    "prompt_request": "a",
                    "timeout": 360
                }
            ]

            model_data = [
                {"text": "a"},
            ]

            prompt_data = [
                {"text": "a"},
            ]

            # Сначала добавляем модели
            for model in model_data:
                await self.insert_record(Model, model)

            # Затем добавляем промпты
            for prompt in prompt_data:
                await self.insert_record(Prompt, prompt)

            # Теперь добавляем записи в таблицу Feed, связывая их с моделью и промптом
            for feed in feeds_data:
                model = await self.get_model_by_text(feed["model_saved"])
                prompt = await self.get_prompt_by_text(feed["prompt_request"])

                feed_data = {
                    "url": feed["url"],
                    "filter_data": feed["filter_data"],
                    "field_mapping": feed["field_mapping"],
                    "model_saved": model.id,
                    "prompt_request": prompt.id,
                    "timeout": feed["timeout"]
                }
                print(feed_data, flush=True)
                await self.insert_record(Feed, feed_data)

    async def get_model_by_text(self, text: str):
        async with self.async_session() as session:
            result = await session.execute(select(Model).filter(Model.text == text))
            return result.scalars().first()  # Получаем первый результат или None

    async def get_prompt_by_text(self, text: str):
        async with self.async_session() as session:
            result = await session.execute(select(Prompt).filter(Prompt.text == text))
            return result.scalars().first()  # Получаем первый результат или None

    async def get_all_feeds(self):
        async with self.async_session() as session:
            query = (
                select(Feed)
                .options(
                    joinedload(Feed.model_saved)
                    .joinedload(Model)
                    .joinedload(Feed.prompt_request)
                    .joinedload(Prompt)
                )
            )
            result = await session.execute(query)
            feeds = result.scalars().all()
            return feeds

    async def close(self):
        await self.engine.dispose()