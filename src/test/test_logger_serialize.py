import pytest
import json
from datetime import datetime, timezone, timedelta
from logger_serialize import serialize

class MockMessage:
    def __init__(self, record):
        self.record = record

def test_serialize(capsys):
    # Cria um registro de log mock
    record = {
        'time': datetime(2023, 10, 10, 12, 0, 0, tzinfo=timezone.utc),
        'level': type('Level', (object,), {'name': 'INFO'}),
        'message': 'Test message'
    }
    message = MockMessage(record)

    # Chama a função serialize
    serialize(message)

    # Captura a saída padrão
    captured = capsys.readouterr()

    # Converte a saída para JSON
    output = json.loads(captured.out.strip())

    # Verifica se os valores estão corretos
    assert output['timestamp'] == '2023-10-10 09:00:00.000000'
    assert output['level'] == 'INFO'
    assert output['message'] == 'Test message'