import asyncio
import time
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models import ArticleInput, ArticleOutput, ErrorResponse, ProcessingStep
from ai_processor import AIProcessor
from demo_processor import DemoAIProcessor
from config import settings

# Initialize FastAPI app
app = FastAPI(
    title="AI Article Rewriter API",
    description="An API that rewrites articles using multiple AI models to bypass AI detection",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI processor
try:
    settings.validate_api_keys()
    ai_processor = AIProcessor()
    demo_mode = False
    print("✅ Real AI processor initialized with API keys")
except ValueError:
    ai_processor = DemoAIProcessor()
    demo_mode = True
    print("🎭 Demo mode enabled - using simulated AI responses")

@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup"""
    global demo_mode
    try:
        settings.validate_api_keys()
        print("✅ All API keys validated successfully")
        demo_mode = False
    except ValueError as e:
        print(f"⚠️  Configuration warning: {e}")
        print("🎭 Running in demo mode with simulated AI responses")
        demo_mode = True

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Article Rewriter API",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "demo_mode": demo_mode,
        "timestamp": datetime.now().isoformat(),
        "api_keys_configured": {
            "openai": bool(settings.OPENAI_API_KEY),
            "anthropic": bool(settings.ANTHROPIC_API_KEY),
            "google": bool(settings.GOOGLE_API_KEY)
        }
    }

@app.post("/rewrite", response_model=ArticleOutput)
async def rewrite_article(article_input: ArticleInput):
    """
    Rewrite an article using the multi-AI pipeline
    
    The process:
    1. ChatGPT performs initial rewrite
    2. Claude humanizes the content
    3. Gemini performs final revision
    
    Note: If API keys are not configured, this runs in demo mode with simulated responses.
    """
    start_time = time.time()
    
    try:
        # Validate input
        if len(article_input.content) > settings.MAX_CONTENT_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Content too long. Maximum {settings.MAX_CONTENT_LENGTH} characters allowed."
            )
        
        if not article_input.content.strip():
            raise HTTPException(
                status_code=400,
                detail="Content cannot be empty"
            )
        
        # Process the article through the AI pipeline
        processing_steps = await ai_processor.process_article(
            content=article_input.content,
            title=article_input.title or "Article",
            style=article_input.target_style
        )
        
        total_processing_time = time.time() - start_time
        
        # Get the final rewritten content
        final_content = processing_steps[-1].output_text
        
        # Create response
        response = ArticleOutput(
            original_content=article_input.content,
            rewritten_content=final_content,
            title=article_input.title or "Rewritten Article",
            processing_steps=processing_steps,
            reference_urls=article_input.source_urls,
            total_processing_time=total_processing_time
        )
        
        # Add demo mode indicator if applicable
        if demo_mode:
            response.ai_detection_confidence = 0.15  # Simulated low detection confidence
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )

@app.post("/rewrite-async")
async def rewrite_article_async(article_input: ArticleInput, background_tasks: BackgroundTasks):
    """
    Start article rewriting process asynchronously
    
    Returns immediately with a task ID for status checking
    """
    # In a production environment, you would implement proper task queue
    # For now, we'll just start the process and return a simple response
    task_id = f"task_{int(time.time())}"
    
    background_tasks.add_task(process_article_background, article_input, task_id)
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": "Article rewriting started. Check back for results.",
        "timestamp": datetime.now().isoformat()
    }

async def process_article_background(article_input: ArticleInput, task_id: str):
    """Background task for processing articles"""
    # This is a simplified implementation
    # In production, you'd use a proper task queue like Celery or similar
    try:
        processing_steps = await ai_processor.process_article(
            content=article_input.content,
            title=article_input.title or "Article",
            style=article_input.target_style
        )
        print(f"Task {task_id} completed successfully")
    except Exception as e:
        print(f"Task {task_id} failed: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            details=str(exc),
            timestamp=datetime.now()
        ).dict()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )