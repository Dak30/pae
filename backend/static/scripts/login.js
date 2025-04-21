const loginUrl = "/login";  

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    const notification = document.getElementById("notification");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch(loginUrl, {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            showNotification(data.message, data.success ? "success" : "error");

            if (data.success) {
                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 1500);
            }
        })
        .catch(() => {
            showNotification("Error al conectar con el servidor.", "error");
        });

        function showNotification(message, type) {
            notification.textContent = message;
            notification.className = `notification show ${type}`;

            setTimeout(() => {
                notification.classList.remove("show");
            }, 3000);
        }
    });
});
