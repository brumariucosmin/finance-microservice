from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.routers.finance import router as finance_router
import app.core.init_db  # creates tables

application = FastAPI(title="Finance Microservice")
instrumentator = Instrumentator()

# attach metrics
instrumentator.instrument(application).expose(application)

application.include_router(finance_router)

@application.get("/health")
def health():
    return {"status": "ok"}
