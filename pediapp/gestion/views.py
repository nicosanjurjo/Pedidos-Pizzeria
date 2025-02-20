from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from cliente.models import Pedido, Turno
from .models import Estado
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

def gestion(request):
    pedidos = Pedido.objects.all()
    pedidos = Pedido.objects.all().order_by('-id')
    stock_general = Estado.objects.first()
    return render(request, 'gestion/gestion.html', {'pedidos': pedidos, 'stock_general': stock_general})


def comprobar_nuevos_pedidos(request):
    if request.method == 'GET':
        nuevos_pedidos = Pedido.objects.filter(visto=False)
        nuevos_pedidos_data = [{'id': pedido.id} for pedido in nuevos_pedidos]
        return JsonResponse(nuevos_pedidos_data, safe=False)

@csrf_exempt
def establecer_stock(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        estado = Estado.objects.first()
        print(data)

        if estado is None:
            estado = Estado.objects.create(estado=False, pedidosdespachados=0)

        if data == 'off':
            Turno.objects.all().update(pedidos_actuales=0)
            pedidos = Pedido.objects.all()
            for pedido in pedidos:
                pedido.visto=True
                pedido.save()
            estado.estado=False
            estado.save()
            return JsonResponse({'status': 'success'}, status=200)

        if data == 'on':
            estado.estado = True
            estado.pedidosdespachados = 0
            estado.save()
            
            return JsonResponse({'status': 'succes'}, status=200)


@csrf_exempt
def obtener_pedido(request):
    if request.method == 'GET':
        print('holamundo')
        pedido_id = request.GET.get('id')
        pedido = get_object_or_404(Pedido, id=pedido_id)
        print(pedido.visto)
        pedido.visto=True
        pedido.save()
        print(pedido.visto)
        pedido_data = {
            'id': pedido.id,
            'ingreso': pedido.created_at,
            'nombre': pedido.nombre,
            'telefono': pedido.telefono,
            'detalles': pedido.detalles,
            'monto': pedido.monto,
            'medio': pedido.medio_pago,
            'metodo': pedido.metodo_entrega,
            'horario': pedido.horario,
            'direccion': pedido.direccion,
            'observaciones': pedido.observaciones,
            'estado': pedido.estado,
        }
        return JsonResponse(pedido_data)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def actualizar_pedido(request):
    if request.method == 'POST':
        pedido_id = request.POST.get('id')
        nuevo_estado = request.POST.get('estado')
        pedido = get_object_or_404(Pedido, id=pedido_id)
        pedido.estado = nuevo_estado
        pedido.save()
        return JsonResponse({'success': 'Pedido actualizado correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

