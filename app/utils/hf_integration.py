import requests
# from functools import lru_cache
from app.config import HF_API_TOKEN, MODEL_ID, API_URL

class HfIntegration:

    @staticmethod
    async def _post_to_hf(url, payload):
        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()

    @staticmethod
    # @lru_cache(maxsize=128)
    async def classify_email(text: str) -> str:
        """
        Classifies an email as 'Produtivo' or 'Improdutivo' using the Hugging Face API.

        This method sends a request to the Hugging Face API with a system prompt that defines
        the criteria for classifying emails. The API analyzes the provided email text and 
        returns one of the two classifications based on the specified criteria.

        Args:
            text (str): The email text to be classified.

        Returns:
            str: The classification result, either 'Produtivo' or 'Improdutivo'.

        Raises:
            ValueError: If the API token is not configured, if the API response is empty, 
            or if there's an error during the API request.
        """

        if not HF_API_TOKEN:
            raise ValueError("Token da API Hugging Face não configurado.")
        
        system_prompt = (
            "Analise este e-mail e classifique-o estritamente como 'Produtivo' ou 'Improdutivo'.\n"
            "Critérios para 'Produtivo':\n"
            "- Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualizações sobre casos em aberto, dúvidas sobre o sistema)\n"
            "Critérios para 'Improdutivo':\n"
            "- Emaisl que não necessitam de uma ação imediata (ex.: 'confirmo recebimento', 'agradeço o contato','mensagens de felicitações','agredecimentos')\n"
            "Sua resposta deve ser apenas 'Produtivo' ou 'Improdutivo'."
        )

        payload = {
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Classifique o seguinte e-mail:\n---\n{text}\n---\n"}
            ],
            "max_tokens": 20,
            "temperature": 0.0, 
            "top_p": 0.9
        }

        try:
            result = await HfIntegration._post_to_hf(API_URL, payload)
            print(f"API Response: {result}") 
            choices = result.get('choices', [])
            
            if not choices:
                raise ValueError("Resposta da API vazia")
            classification_text = choices[0].get('message', {}).get('content', '').strip()
            cleaned_classification = classification_text.lower().replace('.', '').replace(',', '').replace('!', '').replace('?', '')
            if 'produtivo' == cleaned_classification:
                return "Produtivo"
            elif 'improdutivo' == cleaned_classification:
                return "Improdutivo"
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Erro ao classificar email: {str(e)}")

    @staticmethod
    async def generate_response(classification: str, original_text: str) -> str:
        """
        Generates a suggested response to an email based on its classification and original content.

        This function uses predefined guidelines to construct an appropriate response
        according to the email's classification ("Produtivo" or "Improdutivo") and tone.
        It employs the Hugging Face API to assist in generating the response.

        Args:
            classification (str): The classification of the email ('Produtivo' or 'Improdutivo').
            original_text (str): The original email content from which the response will be derived.

        Returns:
            str: The generated email response adhering to the specified guidelines.

        Raises:
            ValueError: If the API response is empty or lacks the necessary content.
            requests.exceptions.RequestException: If there's an error during the API request.

        Note:
            The function requires a valid Hugging Face API token to function. If the token
            is not configured, it returns an error message indicating the missing configuration.
        """
        if not HF_API_TOKEN:
            return "Erro: Token da API não configurado."

        system_prompt = (
            "Você é um assistente de e-mails corporativos. Siga estas regras:\n"
            "1. **Tom**:\n"
            "   - Se o e-mail original for formal, seja formal (ex.: 'Prezado Sr. Silva').\n"
            "   - Se for casual, seja direto mas educado (ex.: 'Olá João').\n"
            "   - Se o e-mail expressar frustração, demonstre empatia (ex.: 'Lamentamos pelo inconveniente').\n\n"
            
            "2. **Estrutura**:\n"
            "   - Produtivo: Confirme a solicitação + ação (ex.: 'Vamos analisar seu problema e retornar em 24h').\n"
            "   - Improdutivo: Agradeça ou confirme (ex.: 'Obrigado pelo feedback!').\n\n"
            
            "3. **Detalhes Obrigatórios**:\n"
            "   - Nunca prometa prazos exatos (use 'em breve', 'nas próximas horas').\n"
            "   - Inclua uma chamada para ação se necessário (ex.: 'Por favor, confirme os dados abaixo').\n\n"
            
            "4. **Formato**:\n"
            "   - Máximo de 3 frases.\n"
            "   - Sem saudações repetidas (evite 'Prezado' se já estiver no e-mail original)."
        )

        user_prompt = (
            f"Classificação: {classification}\n"
            f"Tom do e-mail original: {'formal' if 'Prezado' in original_text else 'casual'}\n"
            f"Conteúdo:\n---\n{original_text[:1000]}\n---\n"
            f"Gere uma resposta que siga as regras acima."
        )

        payload = {
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 150,
            "temperature": 0.7, 
            "top_p": 0.9
        }

        try:
            result = await HfIntegration._post_to_hf(API_URL, payload)
            choices = result.get('choices', [])
            
            if not choices:
                raise ValueError("Resposta da API vazia")
                
            message_content = choices[0].get('message', {}).get('content', '').strip()
            
            if not message_content:
                raise ValueError("Conteúdo vazio")
            return message_content
        except requests.exceptions.RequestException as e:
            return f"Erro ao gerar resposta: {str(e)}"

