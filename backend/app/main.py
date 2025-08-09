# app/main.py
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(title="Blog App API", version="1.0.0")

# 1. CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # adjust to your frontend origin(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Logging Middleware
logger = logging.getLogger("uvicorn.access")
logging.basicConfig(level=logging.INFO)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response Status: {response.status_code}")
        return response

app.add_middleware(LoggingMiddleware)

# 3. Trace ID Middleware
class TraceIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id  # store on request state
        response = await call_next(request)
        response.headers["X-Trace-Id"] = trace_id  # send trace id in response headers
        return response

app.add_middleware(TraceIdMiddleware)

# Include your routers here as before
from app.routers import user_router, blog_router, auth_router
app.include_router(user_router.router)
app.include_router(blog_router.router)
app.include_router(auth_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to Blog App API"}



