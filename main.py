import logging
import asyncio

import config
from app import setup_logger, Settings, Service

settings = Settings.from_config(config.CONFIG)

setup_logger(settings)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting app...")

    service = Service(settings, config.FEEDS, config.PROMTS)

    try:
        # async with asyncio.TaskGroup() as tg:
        #     tg.create_task(service.run())
        await service.run()
    except* Exception as e:
        logger.critical(f"Service crashed: {e}", exc_info=True)
    finally:
        try:
            await service.shutdown()
        except Exception as e:
            logger.error(f"Error during shutdown: {e}", exc_info=True)
        logger.info("App complete!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)