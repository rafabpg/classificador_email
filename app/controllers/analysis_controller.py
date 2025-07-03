class AnalysisController:
    def __init__(self, analysis_service):
        self.analysis_service = analysis_service

    async def analyze_text(self, text: str = None, file=None):
      """
      Analyzes the given text or file and returns the classification and suggested response.

      Args:
          text (str): The text to be analyzed. If this is provided, the file parameter is ignored.
          file: The file to be analyzed. If this is provided, the text parameter is ignored.

      Returns:
          dict: A dictionary with the keys "classification" and "suggested_response".
      """
      try:
        return await self.analysis_service.analyze_text(text=text, file=file) 
      except Exception as e:
          print(f"Erro ao analisar texto: {e}")
          return e