document.getElementById("id_operador").addEventListener("change", function() {
    const idOperador = this.value;
    const institucionSelect = document.querySelector(".institucion-select");

    // Limpiar opciones previas
    institucionSelect.innerHTML = '<option value="">Seleccione una institución</option>';

    if (!idOperador) return;

    fetch(`/instituciones/${idOperador}`)
        .then(response => response.json())
        .then(instituciones => {
            if (instituciones.length === 0) {
                institucionSelect.innerHTML += '<option value="">No hay instituciones disponibles</option>';
                return;
            }

            instituciones.forEach(institucion => {
                const option = document.createElement("option");
                option.value = institucion.id_institucion;
                option.textContent = institucion.sede_educativa;
                institucionSelect.appendChild(option);
            });
        })
        .catch(error => console.error("Error al cargar instituciones:", error));
});


function cargarSedes(selectElement) {
    const institucionId = selectElement.value; // Obtener el ID de la institución seleccionada
    const sedesContainer = selectElement.closest('.institucion-seccion').querySelector('.radio-group');

    // Limpiar contenido previo
    sedesContainer.innerHTML = '';

    if (!institucionId) {
        // Si no hay institución seleccionada, mostrar mensaje
        sedesContainer.innerHTML = '<p class="text-muted">Seleccione una institución primero.</p>';
        return;
    }

    // Realizar solicitud para obtener las sedes
    fetch(`/sedes/${institucionId}`)
        .then(response => {
            if (!response.ok) throw new Error('Error al cargar las sedes');
            return response.json();
        })
        .then(sedes => {
            // Limpiar opciones existentes y cargar las nuevas
            if (sedes.length === 0) {
                sedesContainer.innerHTML = '<p class="text-muted">No hay sedes disponibles para esta institución.</p>';
                return;
            }

            sedes.forEach(sede => {
                const radio = document.createElement('div');
                radio.className = 'form-check';
                radio.innerHTML = `
                    <input class="form-check-input" type="radio" id="sede-${sede.id_sede}" name="sede_${institucionId}" value="${sede.id_sede}" required>
                    <label class="form-check-label" for="sede-${sede.id_sede}">
                        ${sede.nombre_sede}
                    </label>
                `;
                sedesContainer.appendChild(radio);
            });
        })
        .catch(error => {
            console.error('Error al cargar sedes:', error);
            sedesContainer.innerHTML = '<p class="text-danger">Error al cargar sedes. Inténtelo de nuevo más tarde.</p>';
        });
}



function añadirInstitucion() {
    const container = document.getElementById('instituciones-container');
    const seccionExistente = container.querySelector('.institucion-seccion');

    if (!seccionExistente) {
        console.error('No se encontró una sección de institución existente para clonar.');
        return;
    }

    const nuevaSeccion = seccionExistente.cloneNode(true);
    nuevaSeccion.querySelector('.institucion-select').value = '';
    nuevaSeccion.querySelector('.checkbox-group').innerHTML = '';

    const uniqueId = Date.now();
    const institucionSelect = nuevaSeccion.querySelector('.institucion-select');
    institucionSelect.setAttribute('id', `institucion-select-${uniqueId}`);
    institucionSelect.setAttribute('name', 'instituciones[]'); // Cambiar a instituciones[]

    container.appendChild(nuevaSeccion);
}
