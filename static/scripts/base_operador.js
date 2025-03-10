document.addEventListener("DOMContentLoaded", () => {
    const notificationContainer = document.getElementById('notification-container');

    // Verificar si el concepto ya ha sido leído
    const isRead = localStorage.getItem('concept-read');

    // Supongamos que este dato llega desde el servidor o alguna lógica de front-end
    const concepto = "{{ intercambio.datos[12] }}"; // Simula los datos dinámicos

    if (!isRead && (concepto === "Aprobado" || concepto === "Negado" || concepto === "Modificado")) {
        showNotification(concepto);
        localStorage.setItem('concept-read', 'true'); // Marcar como leído
    }
});

function showNotification(concepto) {
    const notificationContainer = document.getElementById('notification-container');
    const notification = document.createElement('div');
    notification.classList.add('notification');

    if (concepto === "Aprobado") {
        notification.classList.add('success');
        notification.textContent = "El estado del concepto es 'Aprobado'.";
    } else if (concepto === "Negado") {
        notification.classList.add('warning');
        notification.textContent = "El estado del concepto es 'Negado'.";
    } else if (concepto === "Modificado") {
        notification.classList.add('warning');
        notification.textContent = "El estado del concepto es 'Modificado'.";
    }

    notificationContainer.appendChild(notification);

    // Eliminar notificación automáticamente después de 5 segundos
    setTimeout(() => {
        notificationContainer.removeChild(notification);
    }, 5000);
}