import abc
import asyncio
from typing import Any, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class BaseAgent(abc.ABC):
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self._logger = self._setup_logging()

    def _setup_logging(self):
        # Professional-grade logging setup
        import logging
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        return logger

    @abc.abstractmethod
    async def run(self, input_data: Any) -> Any:
        """The main logic for the agent's capability."""
        pass

    def log(self, message: str):
        self._logger.info(f"[{self.name}] {message}")

    def error(self, message: str):
        self._logger.error(f"[{self.name}] ERROR: {message}")
