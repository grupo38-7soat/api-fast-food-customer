import sys
from loguru import logger
from services.expose_api_service import ApiService
from config import Config

logger.remove(0)
logger.add(sys.stdout)

if __name__ == '__main__':
    logger.info('start aplication')
    ApiService().run()
