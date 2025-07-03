from app.utils.text_extractor import TextExtractor
from app.utils.hf_integration import HfIntegration

class AnalysisService:
    def __init__(self):
        pass

    async def analyze_text(self, text: str = None, file = None):
        """
        Analyzes the provided text or file and returns its classification and a suggested response.

        This method first extracts and preprocesses the text content if a file is provided,
        or uses the given text directly. It then classifies the text as either "Produtivo" 
        or "Improdutivo" using HfIntegration. Based on the classification, it generates a 
        suggested response.

        Args:
            text (str, optional): The text to be analyzed. If provided, the file parameter is ignored.
            file (optional): An asynchronous file-like object to be analyzed. If provided, the text parameter is ignored.

        Returns:
            dict: A dictionary containing:
                - "classification" (str): The classification of the text.
                - "suggested_response" (str): The suggested response based on the classification.

        Raises:
            ValueError: If the file is of an unsupported format or no extractable text is found.
            Exception: For any other unexpected errors during processing.
        """

        try:
            if file:
                text_content = await TextExtractor.extract_text(file)  
            elif text:
                text_content = text
            else:
           
                return {
                    "classification": "Erro",
                    "suggested_response": "Nenhum conteúdo (texto ou arquivo) foi fornecido."
                }

            if not text_content.strip():
                return {
                    "classification": "Erro",
                    "suggested_response": "O conteúdo está vazio."
                }
            try:
                preprocessed_text = TextExtractor.preprocess_text(text_content)  
                
                classification =  await HfIntegration.classify_email(preprocessed_text)  
                suggested_response =  await HfIntegration.generate_response(classification, text_content)
                
                return {
                    "classification": classification,
                    "suggested_response": suggested_response,
                }
            except Exception as e:
                return {
                    "classification": "Erro",
                    "suggested_response": f"Falha na classificação: {str(e)}"
                }
            
        except Exception as e:
            return {
                "classification": "Erro",
                "suggested_response": f"Erro inesperado: {str(e)}"
            }

