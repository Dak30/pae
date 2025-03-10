// Función para cargar las instituciones
function cargarInstituciones() {
    fetch('/intercambio/instituciones')
        .then(response => response.json())
        .then(data => {
            const institucionSelect = document.getElementById('institucion');
            institucionSelect.innerHTML = '<option value="">Seleccione una institución</option>';
            
            data.forEach(institucion => {
                const option = document.createElement('option');
                option.value = institucion.id_institucion;
                option.textContent = institucion.sede_educativa;
                institucionSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error al cargar instituciones:', error));
}

// Función para cargar sedes según la institución seleccionada
function cargarSedes() {
    const idInstitucion = document.getElementById('institucion').value;
    const sedeSelect = document.getElementById('sede');
    
    if (idInstitucion) {
        fetch(`/intercambio/sedes/${idInstitucion}`)
            .then(response => response.json())
            .then(data => {
                sedeSelect.innerHTML = '<option value="">Seleccione una sede</option>';
                
                data.forEach(sede => {
                    const option = document.createElement('option');
                    option.value = sede.id_sede;
                    option.textContent = sede.nombre_sede;
                    sedeSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error al cargar sedes:', error));
    } else {
        sedeSelect.innerHTML = '<option value="">Seleccione una sede</option>';
    }
}

// Cargar instituciones al cargar la página
document.addEventListener('DOMContentLoaded', cargarInstituciones);
