$(document).ready(function () {
    // Inicializar Select2 en los selects
    $('#operador, #institucion, #sede, #tipo_racion').select2({
        placeholder: 'Seleccione una opción',
        width: '100%' // Ajusta el ancho al contenedor
    });

    // Al cambiar el operador, cargar instituciones relacionadas
    $('#operador').change(function () {
        var operadorId = $(this).val(); // Ahora toma el ID del operador
    
        if (operadorId) {
            $.ajax({
                url: '/get_instituciones/' + operadorId,  // Ahora usa el ID en la URL
                type: 'GET',
                success: function (response) {
                    console.log('Instituciones recibidas:', response);
    
                    $('#institucion').empty().append('<option value="">Seleccione una opción</option>');
    
                    if (response.instituciones && response.instituciones.length > 0) {
                        $.each(response.instituciones, function (index, institucion) {
                            $('#institucion').append('<option value="' + institucion.id + '">' + institucion.nombre + '</option>');
                        });
                    } else {
                        alert('No hay instituciones disponibles para este operador.');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error al obtener las instituciones:', status, error);
                    $('#institucion').empty().append('<option value="">Seleccione una opción</option>');
                    alert('Ocurrió un error al cargar las instituciones.');
                }
            });
        } else {
            $('#institucion').empty().append('<option value="">Seleccione una opción</option>');
        }
    });
    
});


$(document).ready(function () {
    // Inicializar Select2 en todos los selects
    $('#operador, #institucion, #sede, #tipo_racion').select2({
        placeholder: 'Seleccione una opción',
        width: '100%' // Ajusta el ancho al contenedor
    });

    // Función para limpiar el dropdown de sedes
    function limpiarSedes() {
        $('#sede').empty().append('<option value="">Seleccione una sede</option>');
    }

    // Función para limpiar los detalles de la sede
    function limpiarDetallesSede() {
        $('#codigo_sede').val('');
        $('#direccion').val('');
        $('#comuna').val('');
        $('#zona').val('');
    }

    // Cuando se cambia la selección de institución
    $('#institucion').change(function () {
        var institucionId = $(this).val();

        if (institucionId) {
            $.ajax({
                url: '/get_sede/' + institucionId,
                type: 'GET',
                success: function (response) {
                    console.log('Respuesta de sedes:', response); // Para verificar la respuesta

                    limpiarSedes(); // Limpiar el dropdown antes de agregar nuevas opciones

                    if (response.sedes && response.sedes.length > 0) {
                        $.each(response.sedes, function (index, sede) {
                            $('#sede').append('<option value="' + sede.id + '">' + sede.nombre + '</option>');
                        });
                    } else {
                        alert('No se encontraron sedes para esta institución.');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error al obtener las sedes:', status, error);
                    limpiarSedes();
                    limpiarDetallesSede();
                    alert('Ocurrió un error al cargar las sedes. Intente nuevamente.');
                }
            });
        } else {
            limpiarSedes();
            limpiarDetallesSede();
        }
    });

    // Cuando se cambia la selección de sede
    $('#sede').change(function () {
        var sedeId = $(this).val();

        if (sedeId) {
            $.ajax({
                url: '/get_sede_details/' + sedeId,
                method: 'GET',
                success: function (data) {
                    console.log('Detalles de la sede:', data); // Para verificar los detalles

                    if (data) {
                        $('#codigo_sede').val(data.codigo || '');
                        $('#direccion').val(data.direccion || '');
                        $('#comuna').val(data.comuna || '');
                        $('#zona').val(data.zona || '');
                    } else {
                        alert('No se encontraron detalles para esta sede.');
                        limpiarDetallesSede();
                    }
                },
                error: function (xhr) {
                    console.error('Error al obtener los detalles de la sede:', xhr.responseText);
                    limpiarDetallesSede();
                    alert('Ocurrió un error al cargar los detalles de la sede. Intente nuevamente.');
                }
            });
        } else {
            limpiarDetallesSede();
        }
    });
});
