from loguru import logger
from logger_serialize import serialize
from services.expose_api_service import ApiService


logger.remove(0)
logger.add(serialize)

if __name__ == '__main__':
    logger.info('start aplication')
    ApiService().run()
