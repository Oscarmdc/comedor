const btnPantallaCompleta = document.getElementById('pantallaCompletaBtn');

btnPantallaCompleta.addEventListener('click', (event) => {
    event.preventDefault();
    if (!document.fullscreenElement) {
        // Activar pantalla completa
        document.documentElement.requestFullscreen();
    } else {
        // Salir de pantalla completa
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
})

// ***************************************** ABRIR TURNO *****************************************
// variables botones de abrir turno
const modalAbrirTurno = document.getElementById("modal-abrir-turno");
const btnAbrirModalAT = document.getElementById("btn-abrir-turno");
const btnCancelarAT = document.getElementById("btn-cancelar-abrirTurno");

// Eventos abrir turno 
btnAbrirModalAT.addEventListener('click', ()=>{
    modalAbrirTurno.showModal();
    getFechaActual();
});
btnCancelarAT.addEventListener('click', ()=>{
    modalAbrirTurno.close();
});

//  ***************************************** CERRAR TURNO *****************************************
// variables botones de cerrar turno
const modalCerrarTurno = document.getElementById("modal-cerrar-turno");

const btnAbrirModalCT = document.getElementById("btn-cerrar-turno");
const btnCancelarCT = document.getElementById("btn-cancelar-cerrarTurno");

// Evento cerrar turno
btnAbrirModalCT.addEventListener('click', ()=>{
    modalCerrarTurno.showModal();
    getFechaCierre();
});
btnCancelarCT.addEventListener('click', ()=>{
    modalCerrarTurno.close();
});

 
// ***************************************** ABRIR Y CERRAR MODAL PAGAR ORDEN *****************************************
// variables botones de cerrar turno
const modalPagarOrden = document.getElementById("modal-pagar-orden");
//const btnFormPagarOrden = document.getElementById("btn-form-pagar-orden");
const btnAbrirModalPO = document.getElementById("btn-modal-pagar-orden");
const btnCancelarPO = document.getElementById("btn-cancelar-pagarOrden");

// Evento cerrar turno
btnAbrirModalPO.addEventListener('click', ()=>{
    modalPagarOrden.showModal();
});

btnCancelarPO.addEventListener('click', ()=>{
    modalPagarOrden.close();
});

document.getElementById("btn-cerrar-turno").disabled = true

// ***************************************** VALIDAR BOTONES TURNO *****************************************
// Bloquea el boton si no existe un producto en el carrito
const divTurno = document.getElementById("var-control-turno");
let turno = divTurno.getAttribute('data-turno');

const lblCajaTotal = document.getElementById("lblCajaTotal");
activarDesactivarBoton("btn-modal-pagar-orden",0, lblCajaTotal);

lblCajaTotal.addEventListener('input', ()=>{
    activarDesactivarBoton("btn-modal-pagar-orden",0, lblCajaTotal);
});

function activarDesactivarBoton(id, valor, objetivo){
    if (turno == 'True') {
        if (objetivo.textContent == valor){
            document.getElementById(id).disabled = true;
        }else{
            document.getElementById(id).disabled = false;
        }
    }else{
        document.getElementById(id).disabled = true;
    }
    
}

// Botones de turnos
if (turno == 'True') {
    // turno = true, bloquear boton abrir turno y habilitar boton cerrar turno
    document.getElementById("btn-abrir-turno").disabled = true;
    document.getElementById("btn-cerrar-turno").disabled = false;
} else {
    // turno = False, Bloquear boton Cerrar Turno y Habilitar boton abrir turno
    document.getElementById("btn-abrir-turno").disabled = false;
    document.getElementById("btn-cerrar-turno").disabled = true;
}


// ***************************************** VALIDAR MONTO PAGO *****************************************
const inputTotal = document.getElementById("montoTotalPago")
const inputEfectivo = document.getElementById("montoEfectivoPago");
const inputTarjeta = document.getElementById("montoTarjetaPago");
const inputCambio = document.getElementById("montoCambioPago")

const txtTotalPagar = document.getElementById("txtOrdenTotalPagar");
const txtEfectivo = document.getElementById("txtOrdenEfectivo");
const txtTarjeta = document.getElementById("txtOrdenTarjeta");

const lblCambio = document.getElementById("lblOrdenCambio")
const txtCambio = document.getElementById("txtOrdenCambio");

inputEfectivo.focus()
setCursorToEnd(inputEfectivo)
// evento cambios input Efectivo
inputEfectivo.addEventListener('input' ,()=>{
    txtEfectivo.textContent = inputEfectivo.value;
    calcularCambio()
});

// evento cambios input Tarjeta
inputTarjeta.addEventListener('input' ,()=>{ 
    
    let total = parseInt(inputTotal.value);
    let tarjeta = parseInt(inputTarjeta.value);
    
    if (tarjeta > total) {
        inputTarjeta.value = total
        txtTarjeta.textContent = total;
    }else{
        txtTarjeta.textContent = inputTarjeta.value;
    }
    calcularCambio()
});

// Evento Enter
document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
    }
});

// Evento Tab 
inputEfectivo.addEventListener('keydown', function(event) {
    if (event.key === 'Tab') {
        event.preventDefault();
        if (inputEfectivo.value === inputTotal.value) {
            inputEfectivo.value = 0;
            inputTarjeta.value = inputTotal.value;
            inputTarjeta.focus()
            calcularCambio()
        }else{
            const total = parseFloat(inputTotal.value)
            let efectivo = parseFloat(inputEfectivo.value )
            let tarjeta = parseFloat(inputTarjeta.value)
            if (efectivo > total) {
                inputTarjeta.value = 0
                setCursorToEnd(inputTarjeta)
                calcularCambio()

            }else{
                inputTarjeta.value = inputTotal.value - inputEfectivo.value;
                txtTarjeta.textContent = inputTarjeta.value
                setCursorToEnd(inputTarjeta)
                calcularCambio()
            }
            inputTarjeta.focus()
        }
    }
});

// Pone el cursos del input tipo number al final del valor
function setCursorToEnd(input) {
    inp = input;
    value = input.value;

    input.type = 'text';
            
    // Colocar el cursor al final del valor
    input.selectionStart = input.selectionEnd = value.length;
            
    // Restaurar el tipo a 'number'
    input.type = 'number';
}

// ***************************************** CAMBIO *****************************************
function calcularCambio(){
    
    let total = inputTotal.value;
    let efectivo = inputEfectivo.value;
    let tarjeta = inputTarjeta.value;
    let cambio = 0;

    parseInt(total)
    let efectivo2 = parseInt(efectivo)
    let tarjeta2 = parseInt(tarjeta)

    let subtotal = (efectivo2 + tarjeta2);


    // Evaluamos el subtotal, si es mayor o igual desbloquea el boton.
    if(subtotal >= total){
        document.getElementById("btn-form-pagar-orden").disabled = false;
    } else{
        document.getElementById("btn-form-pagar-orden").disabled = true;
    }

    // cambiamos el titulo del label del cambio y ponemos el cambio en positivo
    if (subtotal < total){
        cambio = total - subtotal;
        lblCambio.textContent = "Faltante $";
        txtCambio.textContent = `${parseFloat(cambio)}`;
        inputCambio.value = cambio;
    } else {
        cambio = subtotal - total;
        lblCambio.textContent = "Cambio $";
        txtCambio.textContent = `${parseFloat(cambio)}`;
        inputCambio.value = cambio;
    }

}

// ***************************************** Imprime fecha y hora actual *****************************************
function getFechaActual(){
    const fechaActual = new Date()
    const inputFecha = document.getElementById("imput-fecha-turno");
    const diasSemana = ["Domingo", "Lunes","Martes","Miercoles","Jueves","Viernes","Sábado"]

    let dia = fechaActual.getDate();
    let mes = fechaActual.getMonth();
    let anio = fechaActual.getFullYear();
    let diaSemana = fechaActual.getDay();

    let hora = fechaActual.getHours();
    let minutos = fechaActual.getMinutes();

    // AM o PM
    let jornada = hora <= 12 ? 'AM' : 'PM'
    // Formato de 12 horas
    if (hora > 12) {
        hora = hora - 12;
    }
    // agregar cero dias 1-9
    if (dia < 10){
        dia = "0"+ dia;
    }
    // agregar cero meces 1-9
    if (mes < 10) {
        mes = "0"+ mes;
    }
    inputFecha.value = `${diasSemana[diaSemana]} ${dia}/${mes}/${anio} ${hora}:${minutos} ${jornada}`
}

function getFechaCierre(){
    const fechaCierre = new Date()
    const inputFecha = document.getElementById("imput-cierre-turno");
    inputFecha.value = fechaCierre;
}

// ***************************************** AVISOS *****************************************
window.onload = function() {
    setTimeout(function() {
        const aviso = document.getElementById('aviso');
        if (aviso) {
            aviso.style.display = 'none';
            aviso.id = "";
            aviso.className = "";
        }
    }, 5000);  // 5000 milisegundos = 5 segundos
};