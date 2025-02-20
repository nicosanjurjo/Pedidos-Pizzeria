$(document).ready(function() {

    window.vaciarCarrito = function(){
        localStorage.clear()
        alert("Se eliminaron todos los productos del pedido, puedes volver a seleccionar");
        actualizarTotalCarrito(); // Actualizar el total después de vaciar el carrito
    }

    function confirmacionagregar(categoria, nombre, precio) {
        // Mostrar una confirmación
        let confirmacion = document.createElement('div');
        confirmacion.classList.add('confirmacion-agregado');
        confirmacion.textContent = `${categoria} ${nombre} agregado al pedido`;
     
        // Añadir la confirmación al body
        document.body.appendChild(confirmacion);
     
        // Remover la confirmación después de 2 segundos
        setTimeout(() => {
           confirmacion.remove();
        }, 2000);
     }

    window.agregarProducto = function(id, nombre, precio, categoria) {
    
        // Obtener los productos existentes del Local Storage
        let productos = JSON.parse(localStorage.getItem('productos')) || [];
        
        // Crear un nuevo objeto de producto
        let nuevoProducto = {
            id: id,
            nombre: nombre,
            precio: precio,
            categoria: categoria
        };

        // Agregar el nuevo producto a la lista
        productos.push(nuevoProducto);
    
        // Guardar la lista actualizada en el Local Storage
        localStorage.setItem('productos', JSON.stringify(productos));
    
        confirmacionagregar(categoria, nombre);
        actualizarTotalCarrito(); // Actualizar el total después de agregar un producto

    }

    function desplazarIzquierda(categoriaId) {
        document.getElementById('fila-' + categoriaId).scrollBy({ left: -300, behavior: 'smooth' });
    }
    function desplazarDerecha(categoriaId) {
        document.getElementById('fila-' + categoriaId).scrollBy({ left: 300, behavior: 'smooth' });
    }

     // Función para calcular el total del carrito
     function calcularTotalCarrito() {
        let productos = JSON.parse(localStorage.getItem('productos')) || [];
        let total = productos.reduce((sum, producto) => sum + parseFloat(producto.precio), 0);
        return total.toFixed(2); // Retorna el total con dos decimales
    }

    // Función para actualizar el texto del total del carrito
    function actualizarTotalCarrito() {
        let total = calcularTotalCarrito();
        if (total > 0) {
            $('#estado-carrito').fadeIn(); // Mostrar el contenedor si hay productos
            $('#total-carrito').text('Total: $' + total); // Actualizar el valor del total
        } else {
            $('#estado-carrito').fadeOut(); // Ocultar si el carrito está vacío
        }
    }

    // Inicializar el total del carrito al cargar la página
    actualizarTotalCarrito();

    $('#consultarEstado').click(function(event) {
        event.preventDefault();  // Evita que el formulario se envíe de la manera tradicional
        var telefono = $('#telefono').val();  
        console.log(telefono);
    
        $.ajax({
            url: '/pedido/' + telefono + '/',
            method: 'GET',
            success: function(data) {
                let pedidosHtml = '';
                data.pedidos.forEach(pedido => {
                    const fechaISO = pedido.fechayhora;
                    const fechaObj = new Date(fechaISO);
    
                    // Formatea la fecha a "dd/mm hh:mm" en hora local
                    const fechaFormateada = fechaObj.toLocaleString("es-AR", {
                        day: "2-digit",
                        month: "2-digit",
                        hour: "2-digit",
                        minute: "2-digit",
                        hour12: false
                    }).replace(',', ''); // Elimina la coma que separa la fecha de la hora
    
                    pedidosHtml += `
                        <div class="pedido">
                            <p><strong>Ingresado el:</strong> ${fechaFormateada}</p>
                            <p><strong>Estado:</strong> ${pedido.estado}</p>
                            <p><strong>Nombre:</strong> ${pedido.nombre}</p>
                            <p><strong>Teléfono:</strong> ${pedido.telefono}</p>
                            <p><strong>Detalles:</strong> ${pedido.detalles}</p>
                            <p><strong>Monto:</strong> $${pedido.monto}</p>
                            ${pedido.horario ? `<p><strong>Horario:</strong> ${pedido.horario}</p>` : ''}
                            <p><strong>Medio de Pago:</strong> ${pedido.medio_pago}</p>
                            <p><strong>Método de Entrega:</strong> ${pedido.metodo_entrega}</p>
                            ${pedido.direccion ? `<p><strong>Dirección:</strong> ${pedido.direccion}</p>` : ''}
                            ${pedido.observaciones ? `<p><strong>Observaciones:</strong> ${pedido.observaciones}</p>` : ''}
                            <hr>
                        </div>
                    `;
                });
                $('#modalBody').html(pedidosHtml);
                $('#estadoPedidoModal').modal('show'); // Muestra el modal
            },
            error: function(error) {
                alert('Error: ' + error.responseJSON.error);
            }
        });
    });
    

});
