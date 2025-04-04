import asyncio
import logging

from .client import Client, ClientError
# from .analyzer import Analyzer, AnalyzerError
from .db import Database
from .parse import Parser, ParserError

from .models import Data

logger = logging.getLogger(__name__)

class Service:
    def __init__(self, settings, feeds, promts):
        self.settings = settings
        self.feeds = feeds
        self.promts = promts
        self.client = Client()
        # # self.analyzer = Analyzer()
        self.db = Database(self.settings.DATABASE_URL)
        self.parser = Parser()
        self.tasks = []

    async def _process(self, feed):
        try:
            while True:
                try:
                    xml_data = await self.client.request("get", feed["url"])
                except ClientError as e:
                    logger.error(f"Client error for {feed['url']}: {e}")
                    xml_data = None

                if xml_data:
                    try:
                        parsed_data = self.parser.execute(xml_data, feed["field_mapping"])
                    except ParserError as e:
                        logger.error(f"Parse error for {feed['url']}: {e}")
                        parsed_data = None

                # if parsed_data:
                #     semaphore = asyncio.Semaphore(5)
                #     async with asyncio.TaskGroup() as tg:
                #         for data_item in parsed_data:
                #             try:
                #                 data = await self.analyzer.execute(data_item, self.promts)
                #             except AnalyzerError as e:
                #                 logger.error(f"Analysis error for {feed['url']}: {e}")
                #                 data = None

                #             if data_item:
                #                 try:
                #                     async with semaphore:
                #                         task = tg.create_task(self._save_data(data_item, feed))
                #                         self.tasks.append(task)
                #                 except Exception as e:
                #                     logger.error(f"Error saving data for {feed['url']}: {e}")

                await asyncio.sleep(feed["timeout"])
        except asyncio.CancelledError:
            logger.info(f"Service for {feed['url']} cancelled.")
        except Exception as e:
            logger.exception(f"Unexpected error in service for {feed['url']}: {e}")

    async def _save_data(self, parsed_data, feed):
        domain_name = feed.get("domain")
        
        for item in parsed_data:
            if not item.get("title"):
                logger.warning(f"Missing required fields in item: {item}. Skipping record.")
                continue

            # Данные для добавления в таблицу
            record = {
                "title": item.get("title", ["Unknown"])[0],  # Берем первый элемент из списка заголовков
                "text": ", ".join(item.get("text", [])),  # Объединяем все элементы из списка текстов
            }

            try:
                await self.db.insert_record(Data, record, domain_name)  # Передаем domain_name для поиска или создания домена
                logger.info(f"Saved record: {record}")
            except Exception as e:
                logger.error(f"Failed to save record {record}: {e}")

    async def run(self):
        await self.db.create_table()
        await self.db.initialize_data()
        print(await self.db.get_all_feeds())
        # async with asyncio.TaskGroup() as tg:
        #     for feed in self.feeds:
        #         task = tg.create_task(self._process(feed))
        #         self.tasks.append(task)

    async def shutdown(self):
        logger.info("Shutting down service...")
        for task in self.tasks:
            task.cancel()
        # await self.db.close()
        await self.client.close()
        logger.info("Service shut down complete.")