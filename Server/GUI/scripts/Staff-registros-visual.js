var users
var data
const fragment = document.createDocumentFragment()
const subFragment = document.createDocumentFragment()
const templateCard = document.getElementById('temp-pedido').content
const modal = document.getElementById('modal-more')
const botonCerrar = document.getElementById('boton-cerrar')
const lista = document.querySelector('.item-list')
const templateHerramienta = document.getElementById('herramienta-card').content

document.addEventListener('DOMContentLoaded', e => { fetchData() });

const fetchData = async () => {                       //leo la base de datos y la acomodo
    // const res = await fetch('/user/getstock');
    // data = await res.json()
    // data = JSON.parse(document.getElementById('stock-db').value)
    users   = JSON.parse(document.getElementById( 'usuarios-db' ).value)
    data    = JSON.parse(document.getElementById('peticiones-db').value)
    // console.log(data)
    // dataFiltrada = data
    // console.log(data)
    data.forEach(pedido =>{
        pedido.pedido = JSON.parse(pedido.pedido)
        users.forEach(user =>{
            if (user.id == pedido.autor_id){pedido.autor = user}
            if (user.id == pedido.staff_id){pedido.staff = user}
        })
        pedido.hora = transformarHora(pedido.hora)
    })
    console.log(users)
    console.log(data)
    pintarCards(data)   // pinto las tarjetas con todos los datos
}


const pintarCards = data => {
    data.forEach(pendiente =>{
        // console.log(pendiente)

        if(pendiente.autor.first_name.length == 0){
            templateCard.querySelector('p.info').innerHTML = `<b>#${pendiente.id}</b> - ${pendiente.hora[0]} - (${pendiente.pedido.length}) <br> <b>${pendiente.autor.username}</b> - ${pendiente.staff.username}`}
        else{
            templateCard.querySelector('p.info').innerHTML = `<b>#${pendiente.id}</b> - ${pendiente.hora[0]} - (${pendiente.pedido.length}) <br> <b>${pendiente.autor.username}</b> (${pendiente.autor.last_name} ${pendiente.autor.first_name}) - ${pendiente.staff.username}`}
      
        // agregar iconos
        templateCard.querySelector('i').classList.remove('fa-question-circle'); 
        templateCard.querySelector('i').classList.remove('fa-check-circle'); 
        templateCard.querySelector('i').classList.remove('fa-times-circle'); 

        if      (pendiente.estado == 2){templateCard.querySelector('i').classList.add('fa-check-circle');}
        else if (pendiente.estado == 3){templateCard.querySelector('i').classList.add('fa-times-circle');}
        else                           {templateCard.querySelector('i').classList.add('fa-question-circle');}




        templateCard.querySelector('button.is-info').dataset.id = pendiente.id

        const clone = templateCard.cloneNode(true)
        fragment.appendChild(clone)
    })
    lista.appendChild(fragment)

}

function transformarHora(dato){
    // YYYY-MM-DD T HH:MM:SS.xxxZ
    dato = dato.split('T')
    dato[0] = dato[0].split('-')
    dato[1] = dato[1].split(':')
    finalDato = [`${dato[0][2]}/${dato[0][1]}/${dato[0][0]}`,`${dato[1][0]}:${dato[1][1]}hs.`]
    return finalDato;
}


lista.addEventListener('click', (e)=>{
    e.stopPropagation()
    if(e.target.classList.contains('is-info')){//console.log(e.target); 
        expandirModal(e.target.dataset.id)
    }
        // console.log(selected)

})

function expandirModal(id){
    let pedidoActual;
    data.forEach(pedido=>{if (pedido.id == id)                 {pedidoActual = pedido}})
    // console.log(pedidoActual)
    // console.log(usuarioActual)
    if(pedidoActual.autor.first_name.length == 0){
         modal.querySelector('.modal-card-title').innerHTML =  `${pedidoActual.autor.username} #${pedidoActual.id}`}
    else{modal.querySelector('.modal-card-title').innerHTML =  `${pedidoActual.autor.username} (${pedidoActual.autor.last_name} ${pedidoActual.autor.first_name}) #${pedidoActual.id}`}
    modal.querySelector('time').innerHTML = `${pedidoActual.hora[0]} - ${pedidoActual.hora[1]}`
    modal.querySelector('.herrs').innerHTML = ''
    if(pedidoActual.autor.first_name.length == 0){
        modal.querySelector('.staff').innerHTML = pedidoActual.staff.username}
    else{
        modal.querySelector('.staff').innerHTML = `${pedidoActual.staff.username} (${pedidoActual.staff.first_name} ${pedidoActual.staff.last_name})`}
    if(pedidoActual.estado == 2){
        modal.querySelector('.estado').innerHTML = 'Aprobado'
    }
    else if (pedidoActual.estado == 3){
        modal.querySelector('.estado').innerHTML = 'Rechazado'
    }
    else{        modal.querySelector('.estado').innerHTML = '.'}
    if(pedidoActual.mensaje.length == 0){
        modal.querySelector('.pre-mensaje').setAttribute('hidden',true)
        modal.querySelector('.mensaje').innerHTML = ''
    }
    else{
        modal.querySelector('.pre-mensaje').removeAttribute('hidden')
        modal.querySelector('.mensaje').innerHTML = `${pedidoActual.mensaje}`
    }
    modal.querySelector('.mensaje').innerHTML = pedidoActual.mensaje
    pedidoActual.pedido.forEach(item =>{
        templateHerramienta.querySelector('i').classList.remove('fa-toolbox'); 
        templateHerramienta.querySelector('i').classList.remove('fa-tools'); 
        templateHerramienta.querySelector('i').classList.remove('fa-question-circle');
        templateHerramienta.querySelector('a').classList.remove('expandir');

            if      (item.clase == 1){templateHerramienta.querySelector('i').classList.add('fa-toolbox');         }
            else if (item.clase == 2){templateHerramienta.querySelector('i').classList.add('fa-tools');           }  
            else                     {templateHerramienta.querySelector('i').classList.add('fa-question-circle'); }
            templateHerramienta.querySelector('p.nombre-herr').innerHTML = `${item.nombre} <b>x${item.cantidad}</b>` 

        const subClone = templateHerramienta.cloneNode(true)
        subFragment.appendChild(subClone)
    })
    modal.querySelector('.herrs').appendChild(subFragment)
    modal.classList.add('is-active')
}

botonCerrar.addEventListener ('click',function(){modal.classList.remove('is-active')})


