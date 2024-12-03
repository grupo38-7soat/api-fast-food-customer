import os
from src.config import Config

def test_get_list_with_value(monkeypatch):
    monkeypatch.setenv('TEST_LIST', "['item1', 'item2']")
    value = os.getenv('TEST_LIST')
    assert value == "['item1', 'item2']"
    assert Config.get_list('TEST_LIST') == ['item1', 'item2']

def test_get_list_without_value(monkeypatch):
    monkeypatch.delenv('TEST_LIST', raising=False)
    value = os.getenv('TEST_LIST')
    assert value is None
    assert Config.get_list('TEST_LIST') == []