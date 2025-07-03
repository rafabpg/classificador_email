    /**
     * Inicializa o listener de clique para o bot o de analise de email.
     * Quando o bot o   clicado, ele verifica se o usuario digitou um texto
     * no campo de texto ou enviou um arquivo. Se não houver nenhum dos dois,
     *   exibida uma mensagem de alerta. Caso contrário, o bot é desativado,
     *   exibida uma animação de loading e enviado um pedido para a API
     *   para analisar o email. Se a API retornar um erro,   exibida uma
     *   mensagem de erro para o usuáro. Caso a API retorne um resultado
     *   valido,   atualizado o conteudo do do container de resultado com a
     *   classificaçãoo e a sugestão de resposta.
     */
export function initEmailAnalyzer() {
    const analyzeBtn = document.getElementById("analyze-btn");
    const emailText = document.getElementById("email-text");
    const fileInput = document.getElementById("file-input");
    const resultContainer = document.getElementById("result-container");
    const categoryBadge = document.getElementById("category-badge");
    const suggestionText = document.getElementById("suggestion-text");

    analyzeBtn.addEventListener("click", async function () {
        const text = emailText.value.trim();
        const file = fileInput.files[0];
        if (!text && !file) {
            alert("Por favor, insira o texto do email ou envie um arquivo");
            return;
        }

        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML =
            '<i class="fas fa-spinner fa-spin"></i> Analisando...';
        resultContainer.style.display = "none";
        try {
            const formData = new FormData();
            if (text) formData.append("text", text);;
            if (file) formData.append("file", file);
            const response = await fetch("/api/analyze", {
                method: "POST",
                body: formData,
            });
            
            if (!response.ok) {
                throw new Error("Erro na análise");
            }

            const data = await response.json();
            categoryBadge.textContent = data.classification || "Improdutivo";
            categoryBadge.className =
            "badge " +
                (data.classification === "Produtivo" ? "productive" : "unproductive");
            suggestionText.textContent = data.suggested_response || "Nenhuma sugestão disponível";
            resultContainer.style.display = "block";
        } catch (error) {
            alert("Ocorreu um erro ao analisar o email. Por favor, tente novamente mais tarde.");
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fas fa-robot"></i> Analisar Email';
        }
    });
}