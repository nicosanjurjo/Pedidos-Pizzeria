from django.shortcuts import render, get_object_or_404, redirect
from .forms import FormZona, FormZonaEdit
from .models import Zona
def zonas(request):
    zonas = Zona.objects.all()
    return render(request, 'zonas/zonas.html', {'zonas': zonas})

def form_zonas(request):

    if request.method == 'POST':
        formulario=FormZona(request.POST)

        if formulario.is_valid():
            data_form=formulario.cleaned_data

            nueva_zona = Zona(
                nombre_zona=data_form['nombre_zona'],
                descripcion_zona=data_form['descripcion_zona'],
                costo=data_form['costo'],
                disponible=data_form['disponible']
                )

            # Guardar en la base de datos
            nueva_zona.save()

            return redirect('Zonas')

    else:
        formulario = FormZona()

    return render(request, 'zonas/form_zonas.html', {'form': formulario})


def update_zon(request, pk):
    zona = get_object_or_404(Zona, pk=pk)

    if request.method == 'POST':
        formulario = FormZonaEdit(request.POST, instance=zona)

        if formulario.is_valid():
            formulario.save()
            return redirect('Zonas')

    else:
        formulario = FormZonaEdit(instance=zona)

    return render(request, 'zonas/form_zonas.html', {'form': formulario})


def delete_zon(request, pk):
    zona = get_object_or_404(Zona, pk=pk)

    if request.method == 'POST':
        zona.delete()
        return redirect('Zonas')

    return render(request, 'zonas/confirmar_eliminar.html', {'zona': zona})