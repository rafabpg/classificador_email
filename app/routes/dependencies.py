
from fastapi import Depends
from app.services.analysis_service import AnalysisService
from app.controllers.analysis_controller import AnalysisController

def get_analysis_service():
    return  AnalysisService()

def get_analysis_controller(analysis_service=Depends(get_analysis_service)):
    return AnalysisController(analysis_service)

