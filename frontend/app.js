document.addEventListener("DOMContentLoaded", () => {
    const statusElement = document.getElementById("api-status");

    fetch("http://localhost:8000/health")
        .then(response => response.json())
        .then(data => {
            statusElement.textContent = `État de l'API : ${data.status}`;
            statusElement.style.color = "#4ade80";
        })
        .catch(error => {
            statusElement.textContent = "API non connectée (local en pause)";
            statusElement.style.color = "#f87171";
        });
});
