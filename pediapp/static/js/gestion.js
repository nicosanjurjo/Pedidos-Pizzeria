$(document).ready(function () {
  new DataTable('#myTable', {
    order: [[0, 'desc']]
  });

  $('.habilitar').click(function () {
    var onoff = 'on';
    $.ajax({
      url: 'establecer_stock/',
      method: 'POST',
      data: JSON.stringify(onoff),
      success: function (response) {
        location.reload();
      }
    });
  });

  $('.deshabilitar').click(function () {
    var onoff = 'off';
    $.ajax({
      url: 'establecer_stock/',
      method: 'POST',
      data: JSON.stringify(onoff),
      success: function () {
        location.reload();
      }
    });
  });

  function formatDate(dateString) {
    let date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  $('.ver-editar').click(function () {
    var pedidoId = $(this).data('id');
    $(this).closest('tr').removeClass('nueva-fila');
    $.ajax({
      url: 'obtener_pedido/',
      method: 'GET',
      data: { 'id': pedidoId },
      success: function (response) {
        $('#pedido-id').text(response.id);
        $('#pedido-ingreso').text(formatDate(response.ingreso));
        $('#pedido-nombre').text(response.nombre);
        $('#pedido-telefono').text(response.telefono);
        $('#pedido-detalles').text(response.detalles);
        $('#pedido-monto').text('$ ' + response.monto);
        $('#pedido-medio').text(response.medio);
        $('#pedido-metodo').text(response.metodo);
        $('#pedido-horario').text(response.horario);
        $('#pedido-direccion').text(response.direccion);
        $('#pedido-observaciones').text(response.observaciones);
        $('#pedido-estado').val(response.estado);
        $('#pedidoModal').modal('show');
      },
      error: function (response) {
        alert('Error al obtener los detalles del pedido.');
      }
    });
  });

  $('#cerrarmodal').click(function () {
    location.reload();
  });

  $('.btn-close').click(function () {
    location.reload();
  });

  // Guardar cambios del pedido
  $('#guardar-cambios').click(function () {
    var pedidoId = $('#pedido-id').text();
    var nuevoEstado = $('#pedido-estado').val();
    $.ajax({
      url: 'actualizar_pedido/',
      method: 'POST',
      data: {
        'id': pedidoId,
        'estado': nuevoEstado,
        'csrfmiddlewaretoken': '{{ csrf_token }}'
      },
      success: function (response) {
        location.reload()
      },
      error: function (response) {
        alert('Error al actualizar el pedido.');
      }
    });
  });


    // Mantener un registro de los IDs de los pedidos en la tabla
    let pedidosEnTabla = new Set();

    // Función para comprobar si hay nuevos pedidos cada 5 segundos
    function comprobarNuevosPedidos() {
        $.ajax({
            url: 'comprobar_nuevos_pedidos/', // Cambia esta URL por la que devuelve solo pedidos no vistos
            method: 'GET',
            success: function (data) {
                let nuevosPedidos = data.filter(pedido => !pedidosEnTabla.has(pedido.id)); // Filtra nuevos pedidos que no están en la tabla
                if (nuevosPedidos.length > 0) { // Comprueba si hay nuevos pedidos
                    mostrarBotonNuevosPedidos();
                } else {
                    $('#nuevo-pedido-btn').remove(); // Elimina el botón si no hay nuevos pedidos
                }
            },
            error: function () {
                console.error('Error al comprobar nuevos pedidos.');
            }
        });
    }

  // Mostrar botón "VER NUEVOS PEDIDOS"
  function mostrarBotonNuevosPedidos() {
      if ($('#nuevo-pedido-btn').length === 0) { // Verifica si el botón ya existe
          $('#notificacionpedidos').append('<button id="nuevo-pedido-btn" class="btn">VER NUEVOS PEDIDOS</button>');
          $('#nuevo-pedido-btn').click(function () {
              location.reload(); // Recarga la página al hacer clic
          });
      }
  }

      // Al cargar los pedidos, registra sus IDs en la tabla
      $('#myTable tbody tr').each(function() {
        let pedidoId = $(this).find('td:first').text(); // Suponiendo que el ID es la primera celda
        pedidosEnTabla.add(parseInt(pedidoId));
    });

  // Inicia la comprobación cada 5 segundos
  setInterval(comprobarNuevosPedidos, 5000);
  
  document.getElementById("imprimir").addEventListener("click", async function () {
    // Función para generar una línea solo si el campo tiene contenido
    function generarLinea(label, valor) {
      return valor ? `<p><strong>${label}:</strong> ${valor}</p>` : "";
    }

    // Generar contenido del modal verificando cada campo
    const modalContent = `
      <div style="font-size: 22px; font-family: Verdana, sans-serif">
          ${generarLinea("ID", document.getElementById("pedido-id").textContent)}
          ${generarLinea("Ingreso", document.getElementById("pedido-ingreso").textContent)}
          ${generarLinea("Nombre", document.getElementById("pedido-nombre").textContent)}
          ${generarLinea("Telefono", document.getElementById("pedido-telefono").textContent)}
          ${generarLinea("Cantidad", document.getElementById("pedido-cantidad").textContent)}
          ${generarLinea("Detalles", document.getElementById("pedido-detalles").textContent)}
          ${generarLinea("Monto", document.getElementById("pedido-monto").textContent)}
          ${generarLinea("Medio de pago", document.getElementById("pedido-medio").textContent)}
          ${generarLinea("Horario", document.getElementById("pedido-horario").textContent)}
          ${generarLinea("Direccion", document.getElementById("pedido-direccion").textContent)}
          ${generarLinea("Observaciones", document.getElementById("pedido-observaciones").textContent)}
          ${generarLinea("Estado", document.getElementById("pedido-estado").value)}
      </div>
      <div style="font-size: 18px; font-family: Roboto, sans-serif; font-size: 18px; font-weight: bold; text-align: center; margin-top: 20px;">
          <p>Sistema de pedidos por Desarrollo Criollo</p>
          <p>(Wp: 2657-567000 / Instagram: desarrollocriollo)</p>
          <p>para El Galponcito (2657-584580)</p>
      </div>
  `;

    // Configura el objeto de la solicitud POST para enviar a la impresora
    try {
      const respuestaHttp = await fetch("http://localhost:8000/imprimir", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nombreImpresora: "Global", // Cambia al nombre exacto de la impresora
          serial: "",
          operaciones: [{
            nombre: "Iniciar",
            argumentos: []
          },
          {
            nombre: "GenerarImagenAPartirDeHtmlEImprimir",
            argumentos: [modalContent, 380, 380, 0, false]
          }]
        })
      });

      // Manejando la respuesta de la solicitud de impresión
      if (respuestaHttp.ok) {
        console.log("Solicitud de impresión enviada correctamente.");
      } else {
        console.error("Error al enviar solicitud de impresión:", respuestaHttp.statusText);
      }
    } catch (error) {
      console.error("Error en la conexión con el servicio de impresión:", error);
    }
  });


});