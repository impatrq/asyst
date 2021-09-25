
const botonBuscar = document.getElementById('boton-filtro')
function fechaInt(fecha){
    fecha = fecha.split('/')
    let newFecha = fecha[2] + fecha[1] + fecha[0]
    return newFecha;
}
// const botonBuscar = document.getElementById('boton-buscar')
const filtrar = e =>{
    // console.log(data)
    var dataFiltrada1 = {};
    var dataFiltrada2 = {};
    var dataFiltrada3 = {};
    var dataFiltrada4 = {};
    console.log(listaUsuarios.value)
   if(listaUsuarios.value == '0'){   //filtra por usuarios
        // console.log(data)
        dataFiltrada1 = data
    }
    else{
        data.forEach(pedido=>{
            if(pedido.autor.id == listaUsuarios.value || pedido.staff.id == listaUsuarios.value){
                dataFiltrada1[pedido.id] = {...pedido}
            }
        })
        dataFiltrada1 = Object.values(dataFiltrada1)
    }

    if(listaEstados.value == '0'){ //filtra por estado (aprobado/rechazado)
        dataFiltrada2 = dataFiltrada1
    }
    else{
        dataFiltrada1.forEach(pedido=>{
            if(pedido.estado == listaEstados.value){
                dataFiltrada2[pedido.id] = {...pedido}
            }
        })
        dataFiltrada2 = Object.values(dataFiltrada2)
    }
    // console.log(dataFiltrada2)
    // console.log(element['bulmaCalendar'].datePicker.value())
    if(element['bulmaCalendar'].datePicker.value().length > 10){
    let calendario = element['bulmaCalendar'].datePicker.value().split(' - ')
    console.log(calendario)
    dataFiltrada2.forEach(pedido=>{
        if (fechaInt(calendario[0])<=fechaInt(pedido.hora[0]) && fechaInt(calendario[1])>=fechaInt(pedido.hora[0])){
            console.log(fechaInt(pedido.hora[0]))
            // console.log(fechaInt(calendario[0]) + fechaInt(calendario[1]))
            dataFiltrada3[pedido.id] = {...pedido}
        }
    })
    dataFiltrada3 = Object.values(dataFiltrada3)
}
    else{
        dataFiltrada3 = dataFiltrada2
    }

    let texto = botonBuscar.querySelector('input').value.toLocaleLowerCase()
    dataFiltrada3.forEach(pedido=>{
        pedido.pedido.forEach(herramienta=>{
            let nombre = herramienta.nombre.toLowerCase()
            if(nombre.indexOf(texto) !== -1){
                // console.log(nombre)
                dataFiltrada4[pedido.id] = {...pedido}
            }
        })
    })

    dataFiltrada4 = Object.values(dataFiltrada4)
    dataFiltrada4.sort(function compare(a, b) {
        if (a.id > b.id) {return -1;}
        if (a.id < b.id) {return  1;}
        return 0;})
    pintarCards(dataFiltrada4)
}
botonBuscar.addEventListener('click',filtrar)
botonBuscar.addEventListener('keyup',filtrar)
botonBuscar.addEventListener('input',filtrar)

for (node of botonBuscar.querySelectorAll('button')){
    if(!node.classList.contains('date-item')){
    node.addEventListener('click',(e)=>{
        console.log(e.target.nodeName)
        setTimeout(filtrar(), 500)
        // console.log(botonBuscar.querySelectorAll('button'))
    })}}