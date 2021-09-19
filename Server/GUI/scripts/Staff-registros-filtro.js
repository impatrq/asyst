
const botonBuscar = document.getElementById('boton-filtro')
// const botonBuscar = document.getElementById('boton-buscar')
botonBuscar.addEventListener('click',(e)=>{
    // console.log(data)
    var dataFiltrada1 = {};
    var dataFiltrada2 = {};
    console.log(listaUsuarios.value)
   if(listaUsuarios.value == '0'){   //filtra por usuarios
        console.log(data)
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
    dataFiltrada2.sort(function compare(a, b) {
        if (a.id > b.id) {return -1;}
        if (a.id < b.id) {return  1;}
        return 0;})
    console.log(dataFiltrada2)
    console.log(element['bulmaCalendar'].datePicker.value())
    pintarCards(dataFiltrada2)
    
})

