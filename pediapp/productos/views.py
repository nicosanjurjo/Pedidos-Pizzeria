from django.shortcuts import render, get_object_or_404, redirect
from .forms import FormProducto, FormProductoEdit
from .models import Producto

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/productos.html', {'productos': productos})

def form_productos(request):

    if request.method == 'POST':
        formulario=FormProducto(request.POST)

        if formulario.is_valid():
            data_form=formulario.cleaned_data

            nuevo_producto = Producto(
                nombre=data_form['nombre'],
                descripcion=data_form['descripcion'],
                categoria=data_form['categoria'],
                precio=data_form['precio'],
                disponible=data_form['disponible'],
                masasxunidad=data_form['masasxunidad']
                )

            # Guardar en la base de datos
            nuevo_producto.save()

            return redirect('Productos')

    else:
        formulario = FormProducto()

    return render(request, 'productos/form_productos.html', {'form': formulario})


def update_pro(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        formulario = FormProductoEdit(request.POST, instance=producto)

        if formulario.is_valid():
            formulario.save()
            return redirect('Productos')

    else:
        formulario = FormProductoEdit(instance=producto)

    return render(request, 'productos/form_productos.html', {'form': formulario})


def delete_pro(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        producto.delete()
        return redirect('Productos')  # Redirige a la lista de clientes después de la eliminación

    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})