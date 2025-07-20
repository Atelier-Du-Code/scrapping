document.addEventListener("DOMContentLoaded", () => {
    const convertBtn = document.getElementById("convert-btn");
    const fileInput = document.getElementById("fileElem");
    const resultText = document.getElementById("result-text");
    const consoleLog = document.getElementById("console-log");
    const copyBtn = document.getElementById("copy-btn");

    function getCSRFToken() {
        let cookieValue = null;
        const name = 'csrftoken';
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function logMessage(message, type = "info") {
        const p = document.createElement("p");
        p.textContent = message;

        if (type === "success") p.style.color = "green";
        else if (type === "error") p.style.color = "red";
        else if (type === "info") p.style.color = "blue";

        consoleLog.appendChild(p);
        consoleLog.scrollTop = consoleLog.scrollHeight;
    }

    convertBtn.addEventListener("click", async () => {
        const file = fileInput.files[0];
        if (!file) {
            logMessage("⚠️ Veuillez sélectionner une image avant de convertir.", "error");
            return;
        }

        // Reset zone résultat et logs
        resultText.textContent = "";
        consoleLog.textContent = "";

        logMessage("📤 Démarrage de la conversion OCR...");

        const formData = new FormData();
        formData.append("image", file);

        try {
            const response = await fetch("/convertir_image/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken()
                },
                body: formData
            });

            if (!response.ok) {
                logMessage(`❌ Erreur HTTP : ${response.status}`, "error");
                return;
            }

            const data = await response.json();

            if (data.success) {
                // Affiche les logs envoyés par le serveur
                if (data.logs && Array.isArray(data.logs)) {
                    data.logs.forEach(log => logMessage(log, "success"));
                }

                resultText.textContent = data.texte;
                logMessage("✅ Texte corrigé affiché.", "success");
            } else {
                logMessage(`❌ Erreur : ${data.message}`, "error");
            }
        } catch (error) {
            console.error(error);
            logMessage("❌ Une erreur est survenue lors de la conversion et correction.", "error");
        }
    });

    copyBtn.addEventListener("click", () => {
        const text = resultText.textContent;
        if (!text) {
            logMessage("⚠️ Rien à copier.", "error");
            return;
        }

        navigator.clipboard.writeText(text).then(() => {
            logMessage("📋 Texte copié dans le presse-papiers !", "success");
        }).catch(() => {
            logMessage("❌ Échec de la copie.", "error");
        });
    });
});
