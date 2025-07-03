export function initCopyHandler() {
    const copyBtn = document.getElementById("copy-btn");
    const suggestionText = document.getElementById("suggestion-text");

    copyBtn.addEventListener("click", function () {
        const textToCopy = suggestionText.textContent;

        if (textToCopy && textToCopy !== "-") {
            navigator.clipboard
                .writeText(textToCopy)
                .then(() => {
                    const originalText = copyBtn.innerHTML;
                    copyBtn.innerHTML = '<i class="fas fa-check"></i> Copiado!';

                    setTimeout(() => {
                        copyBtn.innerHTML = originalText;
                    }, 2000);
                })
                .catch((err) => {
                    console.error("Erro ao copiar:", err);
                    alert("Não foi possível copiar o texto");
                });
        }
    });
}