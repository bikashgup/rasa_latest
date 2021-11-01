from loguru import logger

logger.add(
    "{time:dddd MMMM YYYY}.log",
    level="DEBUG",
    format="{time:H:mm} | {level} | {message}",
    rotation="1 days",
)
