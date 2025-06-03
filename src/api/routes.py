"""
API routes for the Advanced AI Backend.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import Dict, Any, List, Optional
import logging

from src.ai_engine.core import ai_engine
from src.utils.logger import setup_logger
from src.workflows.processor import WorkflowProcessor

# Setup logger
logger = setup_logger(__name__)

# Create router
router = APIRouter()

@router.post("/generate")
async def generate_text(
    request: Dict[str, Any] = Body(...)
):
    """
    Generate text based on prompt and context.
    
    Args:
        request: Request body containing prompt and optional context
        
    Returns:
        Generated text and metadata
    """
    prompt = request.get("prompt")
    context = request.get("context")
    
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt is required"
        )
    
    try:
        response = await ai_engine.generate_text(prompt, context)
        return response
    except Exception as e:
        logger.error(f"Error generating text: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating text: {str(e)}"
        )

@router.post("/execute-code")
async def execute_code(
    request: Dict[str, Any] = Body(...)
):
    """
    Execute code and return results.
    
    Args:
        request: Request body containing code and language
        
    Returns:
        Execution results
    """
    code = request.get("code")
    language = request.get("language", "python")
    
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code is required"
        )
    
    try:
        response = await ai_engine.execute_code(code, language)
        return response
    except Exception as e:
        logger.error(f"Error executing code: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing code: {str(e)}"
        )

@router.post("/analyze-sentiment")
async def analyze_sentiment(
    request: Dict[str, Any] = Body(...)
):
    """
    Analyze sentiment of text.
    
    Args:
        request: Request body containing text
        
    Returns:
        Sentiment analysis results
    """
    text = request.get("text")
    
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text is required"
        )
    
    try:
        response = await ai_engine.analyze_sentiment(text)
        return response
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing sentiment: {str(e)}"
        )

@router.post("/workflow")
async def run_workflow(
    request: Dict[str, Any] = Body(...)
):
    """
    Run a workflow with the specified steps.
    
    Args:
        request: Request body containing workflow configuration
        
    Returns:
        Workflow results
    """
    workflow_type = request.get("workflow_type")
    inputs = request.get("inputs", {})
    
    if not workflow_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workflow type is required"
        )
    
    try:
        processor = WorkflowProcessor()
        response = await processor.run_workflow(workflow_type, inputs)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error running workflow: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running workflow: {str(e)}"
        )

@router.post("/telegram-webhook")
async def telegram_webhook(
    update: Dict[str, Any] = Body(...)
):
    """
    Handle Telegram webhook updates.
    
    Args:
        update: Telegram update object
        
    Returns:
        Response to send back to Telegram
    """
    try:
        # This endpoint will be called by the Telegram bot container
        # It processes the update and returns a response
        # In a real implementation, this would handle the update
        # For this demo, we'll just acknowledge receipt
        
        return {"status": "success", "message": "Update received"}
    except Exception as e:
        logger.error(f"Error handling Telegram webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error handling Telegram webhook: {str(e)}"
        )
