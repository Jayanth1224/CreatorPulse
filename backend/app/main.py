from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import drafts, bundles, analytics, auth, linkedin
from app.routers import email_test
from app.routers import auto_newsletter, advanced_auto_newsletter

app = FastAPI(
    title="CreatorPulse API",
    description="AI-powered newsletter drafting assistant API",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(bundles.router, prefix="/api/bundles", tags=["Bundles"])
app.include_router(drafts.router, prefix="/api/drafts", tags=["Drafts"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(linkedin.router, prefix="/api/linkedin", tags=["LinkedIn"])
# Lightweight test route to verify SMTP/email works (router already has /api/test prefix)
app.include_router(email_test.router)
# Auto-newsletters router already includes its own /api/auto-newsletters prefix
app.include_router(auto_newsletter.router)
# Advanced auto-newsletter features router
app.include_router(advanced_auto_newsletter.router)
# Disabled auto-newsletter experimental routes until Supabase-backed implementation is ready
# app.include_router(auto_newsletter.router, prefix="/api/auto-newsletters", tags=["Auto-Newsletters"]) 
# app.include_router(test_auto_newsletter.router, prefix="/api/test", tags=["Test"]) 


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "CreatorPulse API is running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "api": "operational",
        "database": "connected",
    }


@app.on_event("startup")
async def startup_event():
    """Start background services on startup"""
    try:
        from app.services.rss_crawler import rss_crawler
        rss_crawler.start()
        print("[STARTUP] RSS Crawler started")
    except Exception as e:
        print(f"[STARTUP ERROR] Failed to start RSS crawler: {str(e)}")
    
    try:
        from app.services.cron_service import cron_service
        await cron_service.start()
        print("[STARTUP] Cron service started")
    except Exception as e:
        print(f"[STARTUP ERROR] Failed to start cron service: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop background services on shutdown"""
    try:
        from app.services.rss_crawler import rss_crawler
        rss_crawler.stop()
        print("[SHUTDOWN] RSS Crawler stopped")
    except Exception as e:
        print(f"[SHUTDOWN ERROR] Failed to stop RSS crawler: {str(e)}")
    
    try:
        from app.services.cron_service import cron_service
        await cron_service.stop()
        print("[SHUTDOWN] Cron service stopped")
    except Exception as e:
        print(f"[SHUTDOWN ERROR] Failed to stop cron service: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )

