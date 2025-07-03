export function initFileUpload() {
    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("file-input");
    const fileInfo = document.getElementById("file-info");
    const emailText = document.getElementById("email-text");
    const analyzeBtn = document.getElementById("analyze-btn");

    // Helper functions
    const preventDefaults = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const highlight = () => dropzone.classList.add("highlight");
    const unhighlight = () => dropzone.classList.remove("highlight");

    // Event listeners
    ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults);
    });

    ["dragenter", "dragover"].forEach(eventName => {
        dropzone.addEventListener(eventName, highlight);
    });

    ["dragleave", "drop"].forEach(eventName => {
        dropzone.addEventListener(eventName, unhighlight);
    });

    dropzone.addEventListener("drop", handleDrop);
    dropzone.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", () => handleFiles(fileInput.files));

    async function handleFiles(files) {
        if (!files || files.length === 0) return;

        const file = files[0];
        const validTypes = ["text/plain", "application/pdf"];

        if (!validTypes.includes(file.type)) {
            alert("Por favor, envie um arquivo .txt ou .pdf");
            return;
        }

        // Show file info
        fileInfo.innerHTML = `
            <p><strong>Arquivo selecionado:</strong> ${file.name}</p>
            <p><strong>Tipo:</strong> ${file.type}</p>
            <p><strong>Tamanho:</strong> ${(file.size / 1024).toFixed(2)} KB</p>
        `;
        fileInfo.style.display = "block";

        try {
            // Process text files immediately
            if (file.type === "text/plain") {
                const text = await file.text();
                emailText.value = text;
            } 
            // For PDFs, just prepare for upload (backend will process)
            else if (file.type === "application/pdf") {
                emailText.value = ""; // Clear any previous text
                alert("O arquivo PDF será processado pelo servidor. Aguarde a análise.");
            }
            
            // Enable analyze button
            analyzeBtn.disabled = false;
            
        } catch (error) {
            console.error("Erro ao processar arquivo:", error);
            alert("Erro ao ler o arquivo. Tente novamente.");
        }
    }

    function handleDrop(e) {
        const files = e.dataTransfer.files;
        handleFiles(files);
    }
}