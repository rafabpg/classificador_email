# 📧 Classificador Automático de E-mails com IA

Este projeto é uma aplicação web simples para **automatizar a leitura, classificação e resposta de e-mails** recebidos por uma grande empresa do setor financeiro.  
O objetivo é **economizar tempo da equipe**, que não precisará mais revisar manualmente cada mensagem.


---

## 🧩 Tecnologias utilizadas

- **Python 3.11+**
- **FastAPI** — Framework web para construir APIs rápidas e assíncronas
- **Hugging Face Transformers ** — Consumo de modelos de IA para classificação e geração de resposta
- **HTML/CSS** (em `statics/` ou `templates/`) — Interface web simples para formulário de upload e exibição dos resultados

---

## 🌐 Deploy - Render

[🔗 **Acesse o projeto em produção**](https://classificador-email.onrender.com/)

---

## 📂 Estrutura do Projeto

```plaintext
app/
├── main.py            # Arquivo principal com FastAPI
├── routes/            # Rotas
├── utils/
│   ├── text_extractor.py   # Leitura e pré-processamento dos e-mails
│   ├── hf_integration.py   # Integração com Hugging Face API
├── config.py          # Variáveis de ambiente e tokens de API
├── statics/           # Arquivos estáticos (CSS, JS, imagens)
├── templates/         # HTMLs do formulário e exibição de resultados
mocks/                 # Pasta com arquivos de teste
```

--- 

## 🧠 Guia de configuração do projeto

### 🪟 Windows Setup

1. 🔧 Criar ambiente virtual:  

`` python -m venv env_name ``

2. ▶️ Ative o ambiente:

`` env_name/Scripts/activate ``

3. 📦 Instalar dependências: 

`` pip install -r requirements.txt ``

4. 📄 Crie o arquivo `.env` na raiz do projeto.

5. ✍️ Adicione variáveis ​​ao `.env` conforme `.env_example`:

`` HF_API_TOKEN="token da api" ``  

`` API_URL = "url da api da llm" ``  

`` MODEL_ID = "modelo"' ``  

6. 🚀 Rode o servidor:
  
`` uvicorn app.main:app --reload ``

---

### 💻 Linux

1. 🔧 Criar ambiente virtual: 
  
`` python3 -m venv env_name ``

2. ▶️ Ative o ambiente:

`` source env_name/bin/activate ``

3. 📦 Instalar dependências:

`` pip install -r requirements.txt ``

4. 📄 Crie o arquivo `.env` na raiz do projeto.

5. ✍️ Adicione variáveis ​​ao `.env` conforme `.env_example`: 

`` HF_API_TOKEN="token da api" ``  

`` API_URL = "url da api da llm" ``  

`` MODEL_ID = "modelo"' ``  

6. 🚀 Rode o servidor: 

`` uvicorn app.main:app --reload ``

---
