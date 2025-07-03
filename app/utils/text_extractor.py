import io
import re
import unicodedata
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

class TextExtractor:

    @staticmethod
    async def extract_text(file) -> str:
        """
        Asynchronously extracts text content from a given file object.
        Supports PDF and TXT files. For PDF files, it reads the file content,
        extracts text from each page, and concatenates the results. For TXT files,
        it reads and decodes the content as UTF-8. Raises a ValueError if the file
        is missing, has an unsupported format, or if the PDF contains no extractable text.
        Args:
            file: An asynchronous file-like object with a 'filename' attribute and an async 'read' method.
        Returns:
            str: The extracted text content from the file.
        Raises:
            ValueError: If no file is provided, the file format is unsupported, the PDF contains no extractable text,
                        or an error occurs during processing.
        """
        if not file:
            raise ValueError("Nenhum arquivo fornecido")

        filename = secure_filename(file.filename)
        
        try:
            if filename.endswith('.pdf'):
                pdf_bytes = await file.read()
                pdf_stream = io.BytesIO(pdf_bytes)
                reader = PdfReader(pdf_stream)
                
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if not text.strip():
                    raise ValueError("O PDF não contém texto extraível")
                    
                return text.strip()

            elif filename.endswith('.txt'):
                return (await file.read()).decode('utf-8').strip()
                
            else:
                raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf")

        except Exception as e:
            raise ValueError(f"Erro ao processar arquivo: {str(e)}")

    @staticmethod
    def preprocess_text(text: str) -> str:
        """
        Preprocesses a given text by:
        1. Converting it to lower case
        2. Removing non-ASCII characters
        3. Removing non-alphabetic characters
        4. Collapsing multiple spaces into one
        5. Stripping leading and trailing spaces
        """
        text = text.lower()
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        text = re.sub(r'[^a-zA-Z ]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

