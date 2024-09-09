from escpos.printer import Win32Raw
from escpos.image import EscposImage
from PIL import Image
from pathlib import Path
from django.utils import timezone
from datetime import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
NOMBRE = "ABRAHAM ELIZONDO SANCHEZ"
RFC = "EISA901108852"
DIRECCION = "BLVD. JUAN NAVARRETE 291, RAQUET CLUB, 83204 HERMOSILLO, SON."
SEPARADOR = "================================================"
DESPEDIDA = "GRACIAS POR SU PREFERENCIA"

# caracteres de anchura 48

def imprimirTicketVenta(data):
   
    ruta = f"{BASE_DIR}\menu\static\IMG\logo3.png" 
    imagenPIL = Image.open(ruta)
    max_width = 300
    if imagenPIL.width > max_width:
        imagenPIL = imagenPIL.resize((max_width, int((max_width / imagenPIL.width) * imagenPIL.height)), Image.Resampling.NEAREST)
    

    try:
        # Conexion
        p = Win32Raw("ZKP8008")
        p.open(job_name='python-escpos', raise_not_found=True)
        
        # imagen
        p.set(align='center', custom_size=True, width=1, height=1, font='a')
        p.image(imagenPIL, center=True)
        p.set(align='left', custom_size=True, width=1, height=1, font='a')
        p.ln(count=3)

        # Formato
        p.textln(NOMBRE)
        p.textln(f"RFC: {RFC}")
        p.textln(DIRECCION)
        p.textln("")
        p.textln("================================================")
        p.textln(f"ORDEN NO.: {data['orden']}")
        p.textln(f"FECHA:{obtenerFechaActual()['fecha']}, HORA:{obtenerFechaActual()['hora']}")
        p.textln("")

        p.textln("================================================")
        p.textln("CANT. DESCRIPCION                   IMPORTE     ")
        for pro in data['lista_productos']:
            line = f"{1:<6}{pro[1]:<30}$ {pro[2]:>6}\n"
            p.text(line)
        
        p.ln(count=2)
        p.set(align='right', custom_size=True, width=1, height=2, font='a')
        p.textln(f"   TOTAL: {data['total']}        ")
        p.textln("")
        p.set(align='right', custom_size=True, width=1, height=1, font='a')
        if data['efectivo'] != 0:
            n = float(data['efectivo'])
            p.textln(f"EFECTIVO: ${n:<10}")
        if data['tarjeta'] != 0:
            t = float(data['tarjeta'])
            p.textln(f" TARJETA: ${t:<10}")
        c = float(data['cambio'])
        p.textln(f" CAMBIO: ${c:<10}")
        p.set(align='left', custom_size=True, width=1, height=1, font='a')
        p.ln(count=3)
        p.text(DESPEDIDA)
        p.cut()
        p.close()
    except:
        print("Error de impreción") 


def imprimirCierreTurno(data):
    #Conexion
    p = Win32Raw("ZKP8008")
    p.open(job_name='python-escpos', raise_not_found=True)

    if data['error_code'] == 0:
        orden = int(data['total_ordenes'])
        fondo = float(data['fondo_caja'])
        efectivo = float(data['total_efectivo'])
        tarjeta = float(data['total_tarjeta'])
        totalEfectivo = fondo + efectivo
        totalVenta = efectivo + tarjeta

        # Formato
        p.set(align='left', custom_size=True, width=1, height=2, font='a')
        p.text("Cierre de Turno")
        p.ln(count=2)
        p.set(align='left', custom_size=True, width=1, height=1, font='a')
        p.textln("================================================")
        p.textln(f"FECHA APERTURA: {obtenerFecha(data['fecha_inicio'])['fecha']}, HORA: {obtenerFecha(data['fecha_inicio'])['hora']}")
        p.textln(f"FECHA CIERRE:   {obtenerFecha(data['fecha_cierre'])['fecha']}, HORA: {obtenerFecha(data['fecha_cierre'])['hora']}")
        p.textln("")
        p.textln(f"NUMERO DE ORDENES: {orden}")
        p.textln(f"EFECTIVO INICIAL: ${fondo}")
        p.textln("")
        # total efectivo mas fondo inicial
        p.textln(f"TOTAL EN EFECTIVO: ${totalEfectivo}")
        p.textln(f"TOTAL EN TARJETA:  ${tarjeta}")
        p.textln(f"VENTA EN EFECTIVO: ${efectivo}")
        p.textln(f"VENTA EN TARJETA:  ${tarjeta}")
        p.textln("")
        p.textln("                _________________")
        p.set(align='left', custom_size=True, width=1, height=2, font='a')
        p.textln(f"VENTA TOTAL:       ${totalVenta}") # total efectivo + total tarjeta
        p.ln(count=5)
        p.set(align='center', custom_size=True, width=1, height=1, font='a')
        p.textln("__________________________")
        p.textln("FIRMA")
        p.cut()
        p.close()

    else:
        p.set(align='center', custom_size=True, width=1, height=1, font='a')
        p.ln(count=3)
        p.textln("ERROR AL OBTENER LOS DATOS DEL TURNO.")
        p.ln(count=3)
        p.cut()
        p.close()

    obtenerFecha(data['fecha_inicio'])['fecha']
    obtenerFecha(data['fecha_inicio'])['hora']
    obtenerFecha(data['fecha_cierre'])['fecha']
    obtenerFecha(data['fecha_cierre'])['hora']



def obtenerFechaActual():
    now =  timezone.localtime(timezone.now())
    fecha = now.strftime('%d-%m-%Y')
    hora = now.strftime('%H:%M:%S')
    fecha_hora = {'fecha': fecha, 'hora':hora}
    return fecha_hora


def obtenerFecha(fecha):

    miFechaLocal = timezone.localtime(fecha)

    fecha2 = miFechaLocal.strftime('%d-%m-%Y')
    hora = miFechaLocal.strftime('%H:%M:%S')

    fecha_hora = {'fecha': fecha2, 'hora':hora}
    return fecha_hora