from pathlib import Path
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseModel):
    host: str
    port: int
    name: str

    @property
    def url(self) -> str:
        return f"mongodb://{self.host}:{self.port}"


class SQLiteSettings(BaseModel):
    name: str

    @property
    def url(self) -> str:
        return f"sqlite+aiosqlite:///{self.name}"


class TokenSettings(BaseModel):
    secret: SecretStr
    algorithm: str
    access_token_expires_minutes: int = 15
    refresh_token_expires_days: int = 30


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="cloud_",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    root_path: Path = Path(__file__).parents[3]
    storage_path: Path = root_path / "storage"

    sqlite: SQLiteSettings
    mongo: MongoSettings
    token: TokenSettings


settings = Settings()