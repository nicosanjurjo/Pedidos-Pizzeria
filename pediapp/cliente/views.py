from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from productos.models import Producto, Categoria
from gestion.models import Estado
from .models import Pedido, Turno
from zonas.models import Zona
from django.utils import timezone
from datetime import timedelta, datetime

def cliente(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'cliente/cliente.html', {'productos': productos, 'categorias': categorias})

def clienteform(request):
    # Filtrar turnos que tienen menos de 10 pedidos asignados
    turnos = Turno.objects.filter(pedidos_actuales__lt=10)
    medios = Pedido.PAGO_CHOICES
    zonas = Zona.objects.all()
    return render(request, "cliente/form_cliente.html", {"turnos": turnos, "medios": medios, "zonas": zonas})


@csrf_exempt
def crear_pedido(request):
    estado_general=Estado.objects.first()
    if request.method == 'POST' and estado_general.estado == True:
        data = json.loads(request.body.decode('utf-8'))

        horario = None
        if 'horario' in data and data['horario']:
            horario = Turno.objects.get(id=data['horario'])
            horario.pedidos_actuales += 1
            horario.save()
            
        detalles = data['detalles']
            
        if data['metodo_entrega'] == 'envio':
            zona = Zona.objects.get(id=data['zona_id'])
            detalles = detalles + f", {zona.nombre_zona}: ${zona.costo}"
            print(detalles)
            
        # Convertir el horario elegido en un string antes de almacenarlo
        horario_str = horario.horario.strftime("%H:%M") if horario else None

        metodo_entrega = 'Envio a domicilio' if data['metodo_entrega'] == 'envio' else 'Retiro en el local'

        pedido = Pedido(
            nombre=data['nombre'],
            telefono=data['telefono'],
            detalles=detalles,
            monto=data['monto'],
            horario=horario_str,
            medio_pago=data['medio_pago'],
            metodo_entrega=metodo_entrega,
            direccion=data['direccion'] if data['metodo_entrega'] == 'envio' else '',
            observaciones=data['observaciones']
            )
        
    
        estado_general.pedidosdespachados += 1  # reemplaza con el filtro adecuado
        


        estado_general.save()
        pedido.save()
        return JsonResponse({'success': 'Pedido creado exitosamente'}, status=200)


def pedido(request, telefono):
    if request.method == 'GET':
        ahora = datetime.now()
        print(ahora)
        inicio_dia_anterior = (ahora - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        fin_dia_actual = ahora.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Busca todos los pedidos por el número de teléfono
        pedidos = Pedido.objects.filter(
            telefono=telefono,
            created_at__range=(inicio_dia_anterior, fin_dia_actual)
        )
        print(ahora)

        if pedidos.exists():
            # Crear una lista con los detalles de cada pedido
            pedidos_data = []
            for pedido in pedidos:
                data = {
                    'fechayhora': pedido.created_at,
                    'nombre': pedido.nombre,
                    'telefono': pedido.telefono,
                    'detalles': pedido.detalles,
                    'monto': pedido.monto,
                    'estado': pedido.estado,
                    'horario': pedido.horario,
                    'medio_pago': pedido.medio_pago,
                    'metodo_entrega': pedido.metodo_entrega,
                    'direccion': pedido.direccion,
                    'observaciones': pedido.observaciones,
                }
                pedidos_data.append(data)

            return JsonResponse({'pedidos': pedidos_data})
        else:
            return JsonResponse({'error': 'No se encontraron pedidos con ese número de teléfono para el día de hoy.'}, status=404)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)
