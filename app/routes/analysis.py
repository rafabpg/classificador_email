from fastapi import APIRouter, Depends, UploadFile, File, Form
from .dependencies import get_analysis_controller
from app.controllers.analysis_controller import AnalysisController
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["analysis"])

class AnalysisRequest(BaseModel):
    text: str | None = None  
    file: UploadFile | None = None

class AnalysisResult(BaseModel):
    classification: str
    suggested_response: str
    
@router.post("/analyze")
async def analyze(text: str = Form(None),file: UploadFile = File(None), analysis_controller: AnalysisController = Depends(get_analysis_controller))->AnalysisResult:
    """
    Analyze a given text or file and return the classification and suggested response.

    Args:
        text (str): The text to be analyzed. If this is provided, the file parameter is ignored.
        file: The file to be analyzed. If this is provided, the text parameter is ignored.

    Returns:
        AnalysisResult: A dictionary with the keys "classification" and "suggested_response".
    """
    return await analysis_controller.analyze_text(text=text, file=file)