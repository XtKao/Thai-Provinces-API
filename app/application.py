from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api.routes import router
from app.models import HealthResponse

DOCS_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Thai Provinces API | Docs</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
<style>
:root{--ink:#17252d;--muted:#65747a;--paper:#f5f7f4;--line:#dce4df;--teal:#087f78;--coral:#ef775f;--white:#fff}*{box-sizing:border-box}body{margin:0;color:var(--ink);background:var(--paper);font-family:Manrope,sans-serif}.mast{padding:28px clamp(20px,6vw,92px) 34px;color:#fff;background:var(--ink);position:relative;overflow:hidden}.mast:after{content:"";position:absolute;width:270px;height:270px;right:8%;top:-180px;border:46px solid var(--coral);border-radius:50%}.wrap{max-width:1180px;margin:auto;position:relative;z-index:1}.nav{display:flex;justify-content:space-between;align-items:center}.brand{display:flex;align-items:center;gap:12px;font-weight:800}.mark{width:36px;height:36px;display:grid;place-items:center;background:var(--coral);color:var(--ink);border-radius:10px}.nav a{color:#d7e4df;text-decoration:none;font-size:13px;font-weight:700}.hero{margin-top:56px}.eyebrow{color:#82d5c8;font:500 12px 'DM Mono',monospace;letter-spacing:.12em;text-transform:uppercase}h1{max-width:720px;margin:12px 0;font-size:clamp(36px,5vw,62px);line-height:1.03;letter-spacing:-.055em}.intro{max-width:610px;margin:0;color:#b8cbc7;line-height:1.7}.metrics{display:flex;flex-wrap:wrap;gap:10px;margin-top:28px}.metric{min-width:142px;padding:13px 16px;background:#ffffff1a;border:1px solid #ffffff29;border-radius:8px}.metric strong{display:block;font-size:21px}.metric span{color:#a9c1bc;font-size:11px}.content{max-width:1180px;margin:auto;padding:28px clamp(16px,4vw,36px) 80px}.toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px}.toolbar h2{margin:0;font-size:18px}.button{padding:9px 13px;color:var(--teal);background:#fff;border:1px solid var(--line);border-radius:7px;text-decoration:none;font-size:12px;font-weight:700}.swagger-ui .wrapper{max-width:none;padding:0}.swagger-ui .information-container{display:none}.swagger-ui .opblock-tag{padding:22px 0 12px;color:var(--ink);border-bottom:1px solid var(--line);font-size:18px}.swagger-ui .opblock{border-radius:8px;box-shadow:0 2px 8px #17252d0a}.swagger-ui .opblock-summary{min-height:58px}.swagger-ui .btn,.swagger-ui select,.swagger-ui input[type=text],.swagger-ui textarea{border-radius:6px}@media(max-width:640px){.mast{padding:22px 18px 28px}.hero{margin-top:42px}.nav a{display:none}.toolbar{align-items:flex-start;flex-direction:column;gap:12px}}
</style></head>
<body><header class="mast"><div class="wrap"><nav class="nav"><div class="brand"><span class="mark">TH</span><span>Thai Provinces API</span></div><a href="/redoc">ReDoc view ↗</a></nav><section class="hero"><div class="eyebrow">Developer documentation · v1.0.0</div><h1>Address data for Thailand, ready to use.</h1><p class="intro">Browse provinces, districts, subdistricts, and postal codes through a clean REST API.</p></section><div class="metrics"><div class="metric"><strong>77</strong><span>provinces</span></div><div class="metric"><strong>928</strong><span>districts</span></div><div class="metric"><strong>7,436</strong><span>subdistricts</span></div><div class="metric"><strong>JSON</strong><span>response format</span></div></div></div></header><main class="content"><div class="toolbar"><h2>Explore the API</h2><a class="button" href="/openapi.json" target="_blank" rel="noreferrer">OpenAPI JSON ↗</a></div><div id="swagger-ui"></div></main><script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script><script>window.onload=()=>SwaggerUIBundle({url:'/openapi.json',dom_id:'#swagger-ui',deepLinking:true,displayRequestDuration:true,filter:true,persistAuthorization:true,layout:'BaseLayout'});</script></body></html>"""


def create_app() -> FastAPI:
    application = FastAPI(title="Thai Provinces API", version="1.0.0", summary="Thai provinces, districts, subdistricts, and postal codes.", description="An offline REST API backed by validated Thai address data.", contact={"name": "Thai Provinces API", "url": "https://github.com/XtKao/Thai-Provinces-API"}, license_info={"name": "MIT", "identifier": "MIT"}, docs_url=None)
    application.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=False)
    application.include_router(router, prefix="/api")

    @application.get("/docs", include_in_schema=False, response_class=HTMLResponse)
    def docs() -> str:
        return DOCS_HTML

    @application.get("/health", response_model=HealthResponse, tags=["System"], summary="Health check")
    def health() -> HealthResponse:
        return HealthResponse(status="ok", service="thai-provinces-api", version="1.0.0")

    @application.get("/", include_in_schema=False)
    def root() -> RedirectResponse:
        return RedirectResponse(url="/docs", status_code=307)

    return application
