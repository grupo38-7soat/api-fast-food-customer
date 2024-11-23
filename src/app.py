from loguru import logger
import sys
from services.expose_api_service import ApiService

logger.remove(0)
logger.add(sys.stdout)
logger.info('start aplication')

if __name__ == '__main__':
    print('teste')
    ApiService().run()
