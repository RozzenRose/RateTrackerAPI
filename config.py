from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str

    DERIBIT_API_URL: str


    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def rabbitmq_url(self) -> str:
        return (
            f'amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@'
            f'{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}'
        )

    @property
    def deribit_api_url(self) -> str:
        return self.DERIBIT_API_URL


settings = Settings()
print(settings.database_url)