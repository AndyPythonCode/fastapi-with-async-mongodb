# Base on: https://www.mongodb.com/developer/how-to/FARM-Stack-FastAPI-React-MongoDB/
# But with some cool setups made for me
import config
import uvicorn
from fastapi import FastAPI


app = FastAPI(**config.settings.API_METADATA)


# CORS (Cross-Origin Resource Sharing)
app.add_middleware(**config.settings.CORS_MIDDLEWARE)

# Include every router
[app.include_router(path) for path in config.URL_PATTERNS]


@app.on_event("startup")
async def startup():
    """
    Before the application starts
    URL: https://fastapi.tiangolo.com/advanced/events/#startup-event
    """
    app.mongodb_client = config.settings.MONGODB_CLIENT
    app.mongodb = config.settings.MONGODB


@app.on_event("shutdown")
async def shutdown_db_client():
    """
    When the application is shutting down
    URL: https://fastapi.tiangolo.com/advanced/events/#shutdown-event"""
    app.mongodb_client.close()


if __name__ == "__main__":
    uvicorn.run(**config.settings.SERVER_CONFIG)
