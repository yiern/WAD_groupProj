document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file-upload");
    const label = document.getElementById("file-label");

    if (fileInput && label) {
        fileInput.addEventListener("change", () => {
            const fileName = fileInput.files[0]?.name || "No file chosen";
            label.innerText = `Selected file: ${fileName}`;
        });
    }
});

