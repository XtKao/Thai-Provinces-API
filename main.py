from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api.routes import router
from app.models import HealthResponse

app = FastAPI(title="Thai Provinces API", version="1.0.0", summary="Thai provinces, districts, subdistricts, and postal codes.", description="An offline REST API backed by validated Thai address data.", contact={"name": "Thai Provinces API", "url": "https://github.com/XtKao/Thai-Provinces-API"}, license_info={"name": "MIT", "identifier": "MIT"}, docs_url=None)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=False)
app.include_router(router, prefix="/api")


@app.get("/docs", include_in_schema=False, response_class=HTMLResponse)
def custom_docs() -> str:
        return """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Thai Provinces API | Docs</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
    <style>
        :root { --ink: #17252d; --muted: #65747a; --paper: #f5f7f4; --line: #dce4df; --teal: #087f78; --coral: #ef775f; --white: #fff; }
        * { box-sizing: border-box; }
        body { margin: 0; color: var(--ink); background: var(--paper); font-family: Manrope, sans-serif; }
        .topbar { background: var(--ink); color: var(--white); padding: 30px clamp(20px, 6vw, 92px) 38px; position: relative; overflow: hidden; }
        .topbar::after { content: ""; position: absolute; width: 260px; height: 260px; right: 8%; top: -170px; border: 46px solid var(--coral); border-radius: 50%; opacity: .9; }
        .nav { max-width: 1180px; margin: auto; display: flex; align-items: center; justify-content: space-between; gap: 20px; position: relative; z-index: 1; }
        .brand { display: flex; align-items: center; gap: 12px; font-weight: 800; letter-spacing: -.02em; }
        .mark { width: 36px; height: 36px; display: grid; place-items: center; background: var(--coral); color: var(--ink); border-radius: 10px; font-weight: 800; }
        .nav a { color: #d7e4df; text-decoration: none; font-size: 13px; font-weight: 700; }
        .hero { max-width: 1180px; margin: 58px auto 0; position: relative; z-index: 1; }
        .eyebrow { color: #82d5c8; font: 500 12px 'DM Mono', monospace; text-transform: uppercase; letter-spacing: .12em; }
        h1 { max-width: 700px; margin: 12px 0 12px; font-size: clamp(34px, 5vw, 62px); line-height: 1.03; letter-spacing: -.055em; }
        .intro { color: #b8cbc7; max-width: 610px; margin: 0; font-size: 16px; line-height: 1.7; }
        .metrics { max-width: 1180px; margin: 28px auto 0; display: flex; flex-wrap: wrap; gap: 10px; position: relative; z-index: 1; }
        .metric { min-width: 142px; padding: 13px 16px; background: rgba(255,255,255,.1); border: 1px solid rgba(255,255,255,.16); border-radius: 8px; }
        .metric strong { display: block; color: #fff; font-size: 21px; }
        .metric span { color: #a9c1bc; font-size: 11px; }
        .content { max-width: 1180px; margin: 0 auto; padding: 28px clamp(16px, 4vw, 36px) 80px; }
        .toolbar { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 18px; }
        .toolbar h2 { font-size: 18px; margin: 0; letter-spacing: -.03em; }
        .button { color: var(--teal); background: var(--white); border: 1px solid var(--line); border-radius: 7px; padding: 9px 13px; font: 700 12px Manrope, sans-serif; text-decoration: none; }
        #swagger-ui { background: transparent; }
        .swagger-ui .wrapper { max-width: none; padding: 0; }
        .swagger-ui .information-container { display: none; }
        .swagger-ui .opblock-tag { color: var(--ink); border-bottom: 1px solid var(--line); font-size: 18px; padding: 22px 0 12px; }
        .swagger-ui .opblock { border-radius: 8px; box-shadow: 0 2px 8px rgba(23,37,45,.04); border-width: 1px; }
        .swagger-ui .opblock-summary { min-height: 58px; }
        .swagger-ui .opblock-summary-method { border-radius: 6px 0 0 6px; font-family: 'DM Mono', monospace; }
        .swagger-ui .btn { border-radius: 6px; }
        .swagger-ui select, .swagger-ui input[type=text], .swagger-ui textarea { border-radius: 6px; border-color: var(--line); }
        @media (max-width: 640px) { .topbar { padding: 22px 18px 28px; } .hero { margin-top: 42px; } .nav a { display: none; } .content { padding-top: 20px; } .toolbar { align-items: flex-start; flex-direction: column; } .swagger-ui .opblock-summary { flex-wrap: wrap; } }
    </style>
</head>
<body>
    <header class="topbar">
        <nav class="nav"><div class="brand"><span class="mark">TH</span><span>Thai Provinces API</span></div><a href="/redoc">ReDoc view ↗</a></nav>
        <div class="hero"><div class="eyebrow">Developer documentation · v1.0.0</div><h1>Address data for Thailand, ready to use.</h1><p class="intro">Browse provinces, districts, subdistricts, and postal codes through a clean REST API.</p></div>
        <div class="metrics"><div class="metric"><strong>77</strong><span>provinces</span></div><div class="metric"><strong>928</strong><span>districts</span></div><div class="metric"><strong>7,436</strong><span>subdistricts</span></div><div class="metric"><strong>JSON</strong><span>response format</span></div></div>
    </header>
    <main class="content"><div class="toolbar"><h2>Explore the API</h2><a class="button" href="/openapi.json" target="_blank" rel="noreferrer">OpenAPI JSON ↗</a></div><div id="swagger-ui"></div></main>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>window.onload = () => SwaggerUIBundle({ url: '/openapi.json', dom_id: '#swagger-ui', deepLinking: true, displayRequestDuration: true, filter: true, persistAuthorization: true, layout: 'BaseLayout' });</script>
</body>
</html>"""


@app.get("/health", response_model=HealthResponse, tags=["System"], summary="Health check")
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="thai-provinces-api", version="1.0.0")


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=307)