from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import List, Optional
from datetime import datetime

class ProcessingStep(BaseModel):
    """Model for tracking each step in the processing pipeline"""
    model_config = ConfigDict(protected_namespaces=())
    
    step_name: str
    model_used: str
    timestamp: datetime
    input_text: str
    output_text: str
    processing_time: float

class ArticleInput(BaseModel):
    """Input model for article rewriting request"""
    content: str
    source_urls: List[HttpUrl]
    title: Optional[str] = None
    target_style: Optional[str] = "professional"  # professional, casual, academic, etc.

class ArticleOutput(BaseModel):
    """Output model for the rewritten article"""
    original_content: str
    rewritten_content: str
    title: str
    processing_steps: List[ProcessingStep]
    reference_urls: List[HttpUrl]
    total_processing_time: float
    ai_detection_confidence: Optional[float] = None

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    details: Optional[str] = None
    timestamp: datetime