from  pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = '0.0.0.0'
    DB_PORT: int = 5433
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_DRIVER: str = 'postgresql+psycopg2'
    DB_NAME: str = 'pomodoro'
    CACHE_HOST: str = '0.0.0.0'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    JWT_SECRET_KEY: str = 'secret_key'
    JWT_ENCODE_ALGORITHM: str = 'HS256'
    YANDEX_CLIENT_ID: str = ''
    YANDEX_REDIRECT_URI: str = ''
    YANDEX_SECRET_KEY: str = ''
    YANDEX_TOKEN_URL: str = 'https://oauth.yandex.ru/token'

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def yandex_redirect_url(self) -> str:
        return (
            f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&force_confirm=yes"
        )