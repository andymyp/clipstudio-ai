"""Configuration foundation tests."""

from pathlib import Path

from backend.app.core.config import Settings


def test_settings_load_from_yaml(tmp_path: Path) -> None:
    (tmp_path / "app.yaml").write_text(
        "name: Test App\nversion: 9.9.9\nenvironment: testing\n", encoding="utf-8"
    )

    settings = Settings.load(tmp_path)

    assert settings.app.name == "Test App"
    assert settings.app.version == "9.9.9"
    assert settings.app.environment == "testing"


def test_public_config_does_not_expose_database_url() -> None:
    settings = Settings()

    public = settings.public_dict()

    assert "url" not in public["database"]
    assert "driver" in public["database"]
