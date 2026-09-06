from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.routes import router
from app.models import HealthResponse

app = FastAPI(
    title="Thai Provinces API",
    version="1.0.0",
    summary="Thai provinces, districts, subdistricts, and postal codes.",
    description="An offline REST API backed by validated Thai address data.",
    contact={"name": "Thai Provinces API", "url": "https://github.com/XtKao/Thai-Provinces-API"},
    license_info={"name": "MIT", "identifier": "MIT"},
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=False)
app.include_router(router, prefix="/api")


@app.get("/health", response_model=HealthResponse, tags=["System"], summary="Health check")
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="thai-provinces-api", version="1.0.0")


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=307)