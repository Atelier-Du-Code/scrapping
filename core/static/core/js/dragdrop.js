console.log("dragdrop.js chargé !");

const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileElem");
const fileSelect = document.getElementById("fileSelect");
const preview = document.getElementById("preview");
const consoleLog = document.getElementById("console-log");

function logMessage(message, type = "info") {
    const p = document.createElement("p");
    p.textContent = message;

    if (type === "success") p.style.color = "green";
    else if (type === "error") p.style.color = "red";
    else if (type === "info") p.style.color = "blue";

    consoleLog.appendChild(p);
    consoleLog.scrollTop = consoleLog.scrollHeight;
}

// Empêcher le comportement par défaut pour drag & drop
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
  }, false);
});

// Highlight du drop area au survol
dropArea.addEventListener("dragover", () => {
    dropArea.classList.add("hover");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("hover");
});

dropArea.addEventListener("drop", (e) => {
    dropArea.classList.remove("hover");

    if (e.dataTransfer.files.length > 0) {
        const file = e.dataTransfer.files[0];
        handleFile(file);

        // Met à jour le file input pour que conversion.js y ait accès
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        logMessage("📥 Fichier glissé-déposé chargé.", "success");
    }
});

// Clic sur bouton "Choisir une image"
fileSelect.addEventListener("click", (e) => {
    e.preventDefault();
    fileInput.click();
});

// Changement de fichier via input
fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        handleFile(fileInput.files[0]);
        logMessage("📂 Fichier sélectionné via le bouton.", "success");
    }
});

// Afficher l'aperçu et vérifier le type
function handleFile(file) {
    if (file && file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.innerHTML = `<img src="${e.target.result}" alt="Image téléchargée" style="max-width: 100%;">`;
            logMessage("📸 Image chargée : prête pour conversion.", "success");
        };
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = "<p style='color:red'>Veuillez sélectionner une image valide.</p>";
        logMessage("❌ Fichier non valide (pas une image).", "error");
        fileInput.value = "";
    }
}
