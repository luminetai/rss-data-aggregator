import asyncio
import ollama
from concurrent.futures import ThreadPoolExecutor

class Analyzer:
    def __init__(self, model_name: str = "deepseek"):
        self.model_name = model_name
        self.executor = ThreadPoolExecutor()

    async def analyze(self, text: str) -> dict:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self._sync_analyze, text)

    def _sync_analyze(self, text: str) -> dict:
        return ollama.chat(model=self.model_name, messages=[{"role": "user", "content": text}])