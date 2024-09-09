from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from productos.models import Productos, Categorias
from .models import Turno, Orden, DetalleOrden
from decimal import Decimal
from .impresora import imprimirTicketVenta, imprimirCierreTurno

# Variables globales
# variables de venta
lista_productos = []
iva = 0
numero_orden = 1
subTotal = 0
total = 0

# variables del turno
monto_inicial = 0
id_turno = 0
turno_abierto = False
fecha_inicio = ""

total_efectivo = 0.0
total_tarjeta = 0.0
fecha_final = ""

# variables de control
form_type = ""
error = ""
mensaje_error = ""
first_run = True
turno = None


# Create your views here.
def caja(request):
    
    productos = Productos.objects.all()
    categorias = Categorias.objects.all()
    
    global id_turno
    global turno_abierto
    global subTotal
    global iva
    global total
    global total_efectivo
    global total_tarjeta
    global numero_orden
    global form_type
    global monto_inicial
    global lista_productos
    global error
    global mensaje_error
    global first_run
    global turno

    # Verifica si ya existe un turno abierto, 
    # en caso de que exista un turno abierto lo rescata
    try:
        turno = Turno.objects.filter(turno_abierto = True).first()
        monto_inicial = turno.fondo_caja
        if total_efectivo == 0:
            total_efectivo = monto_inicial
    except:
        turno = None
        error = "aviso"
        mensaje_error = "Excepción al buscar un turno abierto."
    
    # establecemos algunas variables 
    if turno:
        id_turno = turno.id
        turno_abierto = True
        # Rescatamos la cantidad de ordenes de turno presente
        try:
            numero_orden = Orden.objects.filter(id_turno_id = id_turno).count()
            ordenes = Orden.objects.filter(id_turno_id = id_turno)
        except:
            numero_orden = 1
        
        numero_orden += 1 
        total_efectivo = ordenes.aggregate(Sum('efectivo'))['efectivo__sum'] or 0
        total_tarjeta = ordenes.aggregate(Sum('tarjeta'))['tarjeta__sum'] or 0
    else:
        error = "aviso"
        mensaje_error = "No hay un turno abierto."
                

    if request.method == 'POST':
        # Recuperando el form donde se hizo la peticion
        form_type = request.POST.get('form_type') 

        # Productos
        if form_type == 'FormProductos':
            # Recuperamos el producto seleccionado
            id = request.POST['id']
            nombre = request.POST['nombre']
            precio = request.POST['precio']
            categoria = request.POST['categoria']
            
            producto = [id, nombre, precio,categoria]

            # Guardamos los productos en la lista de compra
            lista_productos.append(producto)

            # Calculamos el
            calcularTotal()

        # Lista de productos
        if form_type == 'FormListaProductos':
            id = request.POST['id']
            nombre = request.POST['nombre']
            precio = request.POST['precio']
            categoria = request.POST['categoria']

            for sublista in lista_productos:
                if sublista[0] == id:
                    lista_productos.remove(sublista)
                    break  # Salimos del bucle después de eliminar
            calcularTotal()
        
        # filtros productos
        if form_type == 'FormFiltroProductos':
            id = request.POST['id']
            nombre = request.POST['nombre']
            productos = Productos.objects.filter(categoria = id)
        
        # Filtro: Todos los productos
        elif form_type == 'FormFiltroTodosProductos':
            productos = Productos.objects.all()

        # Apertura del turno
        if form_type == 'FormAbrirTurno':
            try:
                monto = request.POST['monto']
                # Colocar un try
                Turno.objects.create(fondo_caja=monto, fecha_inicio = timezone.now())
                id_turno = Turno.objects.filter(turno_abierto = 1)
                turno_abierto = True
                monto_inicial = monto
            except:
                error = "aviso"
                mensaje_error = "Error al tratar de aperturar un nuevo turno."

        
        # Cierre de turno
        if form_type == 'FormCerrarTurno':
            
            if id_turno != 0:
                # rescatar registro del turno abierto
                turno = Turno.objects.get(pk = id_turno)
                # editar registro
                turno.turno_abierto = False
                turno.numero_ordenes = request.POST.get('numero_orden_p')
                turno.total_efectivo = request.POST.get('total_efectivo_p')
                turno.total_tarjeta = request.POST.get('total_tarjeta_p')
                turno.fecha_cierre = timezone.now()
                # guardar Registro
                turno.save()
                
                # Imprecion ticket cierre turno
                try:
                    TURNO = Turno.objects.last()
                    fecha_inicio_t = TURNO.fecha_inicio
                    fecha_cierre_t = TURNO.fecha_cierre
                    fondo_caja_t = TURNO.fondo_caja
                    total_ordenes_t = TURNO.numero_ordenes
                    total_efectivo_t = TURNO.total_efectivo
                    total_tarjeta_t = TURNO.total_tarjeta


                    datos_turno = {
                        'fecha_inicio': fecha_inicio_t,
                        'fecha_cierre': fecha_cierre_t,
                        'fondo_caja': fondo_caja_t,
                        'total_ordenes': total_ordenes_t,
                        'total_efectivo': total_efectivo_t,
                        'total_tarjeta': total_tarjeta_t,
                        'error_code': 0,
                        }
                    imprimirCierreTurno(datos_turno)
                except:
                    datos_turno = {
                    'error_code': 1,
                    }
                    imprimirCierreTurno(datos_turno)
                pass
                
                # cambiar variables de control
                id_turno = 0
                turno_abierto = False
                numero_orden = 1
                total_efectivo = 0
                total_tarjeta = 0
                pass
            else:
                # mensaje de que no existe un turno que cerrar
                if first_run == True:
                    first_run = False
                else:
                    error = "aviso"
                    mensaje_error = "Actualmente no hay turnos abiertos que se puedan cerrar."
                

        # Pagar orden
        if form_type == 'FormPagarOrden':

            # Rescatar datos del formulario de pagar orden
            montoEfectivo = Decimal(request.POST['monto-efectivo'])
            montoTarjeta = Decimal(request.POST['monto-tarjeta'])
            montoTotal =   Decimal(request.POST.get('monto-total-2'))
            montoCambio =  Decimal(request.POST.get('monto-cambio'))

            # Crear Orden en la base de datos
            try:
                Orden.objects.create(
                    fecha = timezone.now(),
                    total = montoTotal,
                    efectivo = montoEfectivo - montoCambio,
                    tarjeta = montoTarjeta,
                    numero_orden = numero_orden,
                    id_turno = Turno.objects.get(id = id_turno),
                )   
            except NameError:
                # Guradar temporalmente ordenes no guardadas en la base de datos
                print(NameError)
            
            # Acumulamos el total de efectivo y tarjeta

            me2 = Decimal(montoEfectivo)
            mt2 = Decimal(montoTarjeta)
            mc2 = Decimal(montoCambio)

            total_efectivo = total_efectivo + me2 -mc2
            total_tarjeta = total_tarjeta + mt2

            # Rescatar el id de ultima orden para guardar los detalles de la orden
            id_ultima_orden = Orden.objects.latest('id').id
            
            # Registrar detalles orden, pasamos id de orden y la id del producto
            # variables temporales 
            for lp in lista_productos:
                DetalleOrden.objects.create(
                    orden = Orden.objects.latest('id'),
                    producto = Productos.objects.get(id = lp[0]),
                    cantidad = 1,
                    precio_unitario = lp[2]
                )
            
            datos_ticket = {'orden':numero_orden, 'lista_productos':lista_productos, 'total': total, 'efectivo':me2, 'tarjeta': mt2, 'cambio': mc2}

            if total != 0:
                imprimirTicketVenta(datos_ticket)
                pass
            
            # Aumentar número de orden
            numero_orden += 1

            # Setear variables locales
            total = 0
            subTotal = 0
            iva = 0
            lista_productos = []

    
    context = {'productos' : productos, 
                'categorias' : categorias, 
                'lista_productos' : lista_productos, 
                'total' : total, 
                'subtotal' : subTotal,
                'iva' : iva,
                'total_efectivo' : total_efectivo,
                'total_tarjeta' : total_tarjeta,
                'numero_orden' : numero_orden,
                'turno_abierto' : turno_abierto,
                'mensaje_error' : mensaje_error or "",
                'error': error,
               }
    
    return render(request, 'caja.html',context)


def calcularTotal():
    global subTotal
    global iva
    global total

    total = 0.0
    iva = 0
    subTotal = 0
    for p in lista_productos:
        total = total + float(p[2])

    iva =  round(float(total*0.16),2)
    subTotal = float(total - iva)