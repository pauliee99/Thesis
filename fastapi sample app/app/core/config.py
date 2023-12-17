from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "ESN app"
    APP_DESCRIPTION: str = "Your App Description"
    APP_VERSION: str = "1.0.0"
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    DATABASE_URL: str = "mysql+mysqlconnector://root:your_root_password@localhost/your_database_name"


settings = Settings()
