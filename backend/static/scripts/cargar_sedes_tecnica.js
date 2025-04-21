$(document).ready(function() {
    $('#operador, #institucion, #sede, #tipo_racion_tecnica').select2({
        placeholder: 'Seleccione una opción',
        width: '100%'
    });

    // Cuando se selecciona un operador, obtener las instituciones asociadas
    $('#operador').change(function() {
        var operadorId = $(this).val();

        if (operadorId) {
            $.ajax({
                url: '/get_instituciones/' + operadorId,
                type: 'GET',
                success: function(response) {
                    console.log('Instituciones recibidas:', response);
                    
                    var institucionSelect = $('#institucion');
                    institucionSelect.empty();
                    institucionSelect.append('<option value="">Seleccione una institución</option>');

                    $.each(response.instituciones, function(index, institucion) {
                        institucionSelect.append('<option value="' + institucion.id + '">' + institucion.nombre + '</option>');
                    });
                },
                error: function(xhr) {
                    console.error('Error al obtener instituciones:', xhr.responseText);
                    $('#institucion').empty().append('<option value="">Seleccione una institución</option>');
                }
            });
        } else {
            $('#institucion').empty().append('<option value="">Seleccione una institución</option>');
        }
    });

    // Aquí continúa el código para obtener sedes y detalles de la sede...
});


$(document).ready(function() {
    // Inicializar Select2 en todos los selects
    $('#operador, #institucion, #sede, #tipo_racion_tecnica').select2({
        placeholder: 'Seleccione una opción',
        width: '100%' // Ajusta el ancho al contenedor
    });

    // Cuando se cambia la selección de institución
    $('#institucion').change(function() {
        var institucionId = $(this).val();
        if (institucionId) {
            $.ajax({
                url: '/get_sede/' + institucionId,
                type: 'GET',
                success: function(response) {
                    console.log('Respuesta de sedes:', response); // Para verificar la respuesta

                    var sedeSelect = $('#sede');
                    sedeSelect.empty();
                    sedeSelect.append('<option value="">Seleccione una sede</option>');
                    $.each(response.sedes, function(index, sede) {
                        sedeSelect.append('<option value="' + sede.id + '">' + sede.nombre + '</option>');
                    });
                },
                error: function(xhr, status, error) {
                    console.error('Error al obtener las sedes:', status, error);
                    // Limpiar el dropdown de sedes en caso de error
                    $('#sede').empty();
                    $('#sede').append('<option value="">Seleccione una sede</option>');
                    // Limpiar los campos asociados a la sede
                    $('#codigo_sede').val('');
                    $('#direccion').val('');
                    $('#zona').val('');
                }
            });
        } else {
            // Limpiar el dropdown de sedes si no hay institución seleccionada
            $('#sede').empty();
            $('#sede').append('<option value="">Seleccione una sede</option>');
            // Limpiar los campos asociados a la sede
            $('#codigo_sede').val('');
            $('#direccion').val('');
            $('#zona').val('');
        }
    });

    // Cuando se cambia la selección de sede
    $('#sede').change(function() {
        var sedeId = $(this).val();
        
        if (sedeId) {
            $.ajax({
                url: '/get_sede_details/' + sedeId,
                method: 'GET',
                success: function(data) {
                    console.log('Detalles de la sede:', data); // Para verificar los detalles

                    $('#codigo_sede').val(data.codigo || '');
                    $('#direccion').val(data.direccion || '');
                    $('#zona').val(data.zona || '');
                },
                error: function(xhr) {
                    console.log('Error al obtener los detalles de la sede:', xhr.responseText);
                    // Limpiar los campos en caso de error
                    $('#codigo_sede').val('');
                    $('#direccion').val('');
                    $('#zona').val('');
                }
            });
        } else {
            // Limpiar los campos si no se selecciona ninguna sede
            $('#codigo_sede').val('');
            $('#direccion').val('');
            $('#zona').val('');
        }
    });
});
