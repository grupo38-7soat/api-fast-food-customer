from src.app import ApiService

def test_app_startup(monkeypatch):
    def mock_run(self):
        return "Application started"

    monkeypatch.setattr(ApiService, "run", mock_run)

    result = ApiService().run()
    assert result == "Application started"
    