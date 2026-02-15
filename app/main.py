from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import router
from app.core.logging import logger
from app.agents.graph import graph # Verify graph imports correctly

def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API Router
    app.include_router(router, prefix="") 

    # Mount static files
    from fastapi.staticfiles import StaticFiles
    import os
    
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    os.makedirs(static_dir, exist_ok=True)
    
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/")
    async def root():
        from fastapi.responses import FileResponse
        return FileResponse(os.path.join(static_dir, "index.html"))

    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting up Local RAG Service...")
        # Verify graph is compiled
        if graph:
            logger.info("Multi-Agent Graph loaded successfully.")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down Local RAG Service...")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
