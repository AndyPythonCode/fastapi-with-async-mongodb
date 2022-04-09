from pydantic import BaseSettings
from functools import cached_property
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

"""
__________________________BaseSettings__________________________

Create a clearly-defined, type-hinted application configuration class

URL: https://pydantic-docs.helpmanual.io/usage/settings/
"""


class APISettings(BaseSettings):
    """
    You can customize several metadata configurations in your FastAPI application.

    URL: https://fastapi.tiangolo.com/tutorial/metadata/?h=docs_url#docs-urls
    """

    TITLE: str = "FASTAPI-ASYNC-MONGODB"
    DESCRIPTION: str = "Mongodb simple CRUD project"
    VERSION: str = "1.0.0"
    DOCS_URL: str = "/"


class ServerSettings(BaseSettings):
    """
    Uvicorn is an ASGI web server implementation for Python.

    URL: https://www.uvicorn.org/
    """

    APP: str = "main:app"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True


class CORSSettings(BaseSettings):
    """
    For security reasons, browsers restrict cross-origin HTTP requests initiated from scripts.

    URL: https://fastapi.tiangolo.com/tutorial/cors/?h=cors
    """

    ALLOWED_HOSTS: list[str] = []
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: str = "*"
    ALLOW_HEADERS: str = "*"


class DatabaseSettings(BaseSettings):
    """
    These environment variables are commonly placed in a file .env

    URL: https://fastapi.tiangolo.com/advanced/settings/#reading-a-env-file
    """

    DB_URL: str
    DB_NAME: str

    class Config:
        env_file = ".env"
        keep_untouched = (
            # Model's default values that should not be changed during model creation
            cached_property,
        )


class Settings(APISettings, ServerSettings, CORSSettings, DatabaseSettings):
    """
    Python's property() is the Pythonic way to avoid formal getter and setter methods in your code.
    """

    @property
    def API_METADATA(self) -> dict[str]:
        return {
            "title": self.TITLE,
            "description": self.DESCRIPTION,
            "version": self.VERSION,
            "docs_url": self.DOCS_URL,
        }

    @property
    def CORS_MIDDLEWARE(self) -> dict:
        return {
            "middleware_class": CORSMiddleware,
            "allow_origins": self.ALLOWED_HOSTS or ["*"],
            "allow_credentials": self.ALLOW_CREDENTIALS,
            "allow_methods": self.ALLOW_METHODS,
            "allow_headers": self.ALLOW_HEADERS,
        }

    @property
    def SERVER_CONFIG(self) -> dict[str]:
        return {
            "app": self.APP,
            "host": self.HOST,
            "port": self.PORT,
            "reload": self.RELOAD,
        }

    """
    Python's @cached_property transform a method of a class into a property whose value is computed once
    and then cached as a normal attribute for the life of the instance. Similar to property(), with 
    the addition of caching. 

    WHY DO I USE IT?
    * It will return the same object that was returned on the first call, again and again.
    * Lets you avoid reading the dotenv file again and again for each request
    """

    @cached_property
    def MONGODB_CLIENT(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(self.DB_URL)

    @cached_property
    def MONGODB(self) -> AsyncIOMotorDatabase:
        return self.MONGODB_CLIENT[self.DB_NAME]


settings = Settings()
