# tests/test_app.py
import pytest
import sys
from loguru import logger
from services.expose_api_service import ApiService

def test_logger_configuration():
    logger.remove(0)
    logger.add(sys.stdout)
    assert len(logger._core.handlers) > 0

def test_api_service_run(mocker):
    mocker.patch('services.expose_api_service.ApiService.run')
    service = ApiService()
    service.run()
    service.run.assert_called_once()

if __name__ == '__main__':
    pytest.main()