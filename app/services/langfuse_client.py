from langfuse import get_client
from loguru import logger


class LangfuseClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = get_client()
            if cls._instance.auth_check():
                logger.info("Langfuse client is authenticated and ready!")
            else:
                logger.error(
                    "Authentication failed. Please check your credentials and host."
                )
        return cls._instance


# Singleton instance
langfuse_client = LangfuseClient()
