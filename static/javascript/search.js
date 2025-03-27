document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("search-form");
    if (form) {
        form.addEventListener("submit", (e) => {
            const input = document.getElementById("search-input");
            if (input.value.trim() === "") {
                e.preventDefault();
                alert("Please enter something to search!");
            }
        });
    }
});
