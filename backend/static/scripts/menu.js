function cargarInstituciones(idOperador) {
    console.log(`ID Operador recibido en JS: ${idOperador}`);  // Depuración
    const institucionesSelect = document.querySelector('.institucion-select');
    const sedesContainer = document.querySelector('.checkbox-group');

    // Limpiar el select de instituciones y el contenedor de sedes
    institucionesSelect.innerHTML = '<option value="">Seleccione una institución</option>';
    sedesContainer.innerHTML = '<p>Seleccione una institución para ver sus sedes.</p>';

    // Si no hay un ID de operador, mostrar un mensaje y salir
    if (!idOperador) {
        console.log("No se proporcionó un ID de operador.");  // Depuración
        institucionesSelect.innerHTML = '<option value="">Seleccione un operador primero</option>';
        return;
    }

    // Hacer la solicitud al servidor para obtener las instituciones
    fetch(`/instituciones/${idOperador}`)
        .then(response => {
            if (!response.ok) throw new Error('Error en la red');
            return response.json();
        })
        .then(instituciones => {
            console.log("Instituciones recibidas:", instituciones);  // Depuración
            // Verificar si se recibieron instituciones
            if (!instituciones || instituciones.length === 0) {
                console.log("No hay instituciones disponibles.");  // Depuración
                institucionesSelect.innerHTML = '<option value="">No hay instituciones disponibles</option>';
                return;
            }

            // Llenar el select con las instituciones recibidas
            instituciones.forEach(institucion => {
                const option = document.createElement('option');
                option.value = institucion.id_institucion;
                option.textContent = institucion.sede_educativa;
                institucionesSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error cargando instituciones:', error);
            institucionesSelect.innerHTML = '<option value="">Error cargando instituciones</option>';
        });
}

// Cargar sedes según la institución seleccionada
function cargarSedes(selectElement) {
    const institucionId = selectElement.value;
    const sedesContainer = selectElement.closest('.institucion-seccion').querySelector('.checkbox-group');

    if (!institucionId) {
        sedesContainer.innerHTML = '<p>Seleccione una institución primero.</p>';
        return;
    }

    fetch(`/sedes/${institucionId}`)
        .then(response => {
            if (!response.ok) throw new Error('Error en la red');
            return response.json();
        })
        .then(sedes => {
            console.log(`Sedes cargadas para la institución ${institucionId}:`, sedes);
            sedesContainer.innerHTML = ''; // Limpiar opciones existentes
            sedes.forEach(sede => {
                const checkbox = document.createElement('div');
                checkbox.className = 'form-check';
                checkbox.innerHTML = `
                    <input class="form-check-input" type="checkbox" id="sede-${sede.id_sede}" name="sedes_${institucionId}[]" value="${sede.id_sede}">
                    <label class="form-check-label" for="sede-${sede.id_sede}">
                        ${sede.nombre_sede}
                    </label>
                `;
                sedesContainer.appendChild(checkbox);
            });
        })
        .catch(error => {
            console.error('Error cargando sedes:', error);
            sedesContainer.innerHTML = '<p>Error cargando sedes. Inténtelo de nuevo más tarde.</p>';
        });
}

// Añadir una nueva sección de institución y sede
function añadirInstitucion() {
    const container = document.getElementById('instituciones-container');
    const seccionExistente = container.querySelector('.institucion-seccion');

    if (!seccionExistente) {
        console.error('No se encontró una sección de institución existente para clonar.');
        return;
    }

    // Clonamos la sección existente
    const nuevaSeccion = seccionExistente.cloneNode(true);

    // Limpiamos los campos para la nueva sección (no perderemos datos de las anteriores)
    nuevaSeccion.querySelector('.institucion-select').value = '';
    nuevaSeccion.querySelector('.checkbox-group').innerHTML = '';

    // Asignamos un ID único a cada nuevo select e input
    const uniqueId = Date.now();
    const institucionSelect = nuevaSeccion.querySelector('.institucion-select');
    institucionSelect.setAttribute('id', `institucion-select-${uniqueId}`);

    const checkboxes = nuevaSeccion.querySelectorAll('.form-check-input');
    checkboxes.forEach(checkbox => {
        checkbox.setAttribute('id', `sede-${uniqueId}-${checkbox.value}`);
        checkbox.setAttribute('name', `sedes_${uniqueId}[]`);
    });

    // Añadimos la nueva sección al contenedor
    container.appendChild(nuevaSeccion);
}

// Eliminar una sección de institución y sede
function eliminarInstitucion(boton) {
    const seccion = boton.closest('.institucion-seccion'); // Encontramos la sección correspondiente
    seccion.remove(); // Eliminamos esa sección
}
