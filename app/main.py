from fastapi import FastAPI
from app.api.routes import include_routers

app = FastAPI(
    title="Bynder lottery service",
    description="Service handling a lottery system",
    version="1.0.0",
    # Uncomment to disable
    # docs_url=None,
    # redoc_url=None,
    # openapi_url=None,
)

# Use the function to include all routers
include_routers(app)
