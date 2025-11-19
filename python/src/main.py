from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import RedirectResponse
from configs.config_version import __version__
from pathlib import Path
from routers import (
    router_github,
    router_health,
)
import json
import os

CURRENT_PATH = Path(__file__).resolve().parent

description = open(f"{CURRENT_PATH_}/docs/documentation.md", "r")
tags_metadata = open(f"{CURRENT_PATH}/docs/metadata.json", "r")

# Secure environment detection
IS_PRODUCTION = os.getenv("EMODE") == "production"

app = FastAPI(
    title="FastAPI Containerized Build Deploy Example",
    description=description.read(),
    contact={"name": "DevTools"},
    version=__version__,
    # Disable docs in production for security
    docs_url="/docs" if not IS_PRODUCTION else None,
    redoc_url=None,
    servers=[{"url": "/", "description": "Root URL"}],
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    openapi_tags=json.load(tags_metadata),
)

# Secure CORS configuration - specify allowed origins
# For development, use localhost; for production, use actual domains
if IS_PRODUCTION:
    # Replace with your actual production domains
    origins = [
        "https://yourdomain.com",
        "https://www.yourdomain.com",
    ]
else:
    # Development origins
    origins = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8000",
    ]

# Security middleware - order matters!
if IS_PRODUCTION:
    # Enforce HTTPS in production
    app.add_middleware(HTTPSRedirectMiddleware)
    # Restrict trusted hosts in production
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["yourdomain.com", "www.yourdomain.com"]
    )

# CORS configuration with improved security
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,  # Disable credentials for better security
    allow_methods=["GET", "POST"],  # Limit to necessary methods
    allow_headers=[
        "accept",
        "accept-encoding",
        "authorization",
        "content-type",
        "dnt",
        "origin",
        "user-agent",
        "x-csurftoken",
        "x-requested-with",
    ],
)

app.include_router(router_github.router, tags=["GitHub"])
app.include_router(router_health.router, tags=["Health"])


@app.get(
    path="/",
    response_class=RedirectResponse,
    status_code=status.HTTP]“;_TEMPORARY_REDIRECT,
    include_in_schema=False,
)
async def redirect_to_docs():
    response = RedirectResponse(url="/docs")
    return response
