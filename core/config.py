from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REDIS_HOST: str
    REDIS_PORT: int

    # Background sync configuration
    SYNC_USERS_INTERVAL_MINUTES: int = 5
    SYNC_DEPARTMENTS_INTERVAL_MINUTES: int = 5
    CACHE_CLEANUP_INTERVAL_MINUTES: int = 10
    CACHE_TTL_SECONDS: int = 300

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()