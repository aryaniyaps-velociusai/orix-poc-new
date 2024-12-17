from pydantic import BaseSettings


class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str
    AZURE_OPENAI_DEPLOYMENT: str

    AZURE_INFERENCE_ENDPOINT: str
    AZURE_INFERENCE_CREDENTIAL: str

    class Config:
        env_file = ".env"  # Specify the .env file if it's not in the root folder


# Load the settings
settings = Settings()
