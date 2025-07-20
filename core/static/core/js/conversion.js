document.addEventListener("DOMContentLoaded", () => {
    const convertBtn = document.getElementById("convert-btn");
    const fileInput = document.getElementById("fileElem");
    const resultText = document.getElementById("result-text");
    const consoleLog = document.getElementById("console-log");

    function getCSRFToken() {
        // Récupère le token CSRF depuis les cookies (méthode fiable)
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

        const formData = new FormData();
        formData.append("image", file);

        logMessage("📤 Passage de l'image dans le modèle de récupération des mots...");
         logMessage("📤 ça pourrait être un peu long");

        try {
            const response = await fetch("/convertir/", {
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
                resultText.textContent = data.texte;
                logMessage("✅ Conversion réussie ! Texte OCR affiché.", "success");
            } else {
                logMessage(`❌ Erreur : ${data.message}`, "error");
            }
        } catch (error) {
            console.error(error);
            logMessage("❌ Une erreur est survenue lors de la conversion.", "error");
        }
    });
});
