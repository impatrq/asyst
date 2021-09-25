document.addEventListener('DOMContentLoaded', e => { fetchData() });
const fragment = document.createDocumentFragment()
const subFragment = document.createDocumentFragment()
const templateCard = document.getElementById('card-pedido').content
const columnas = document.querySelector('.columns.is-centered.is-multiline')
const templateHerramienta = document.getElementById('herramienta-card').content
var data = []
var users = []
const modal = document.getElementById('modal-more')
const botonCerrar = document.getElementById('boton-cerrar')
const modalRechazo = document.getElementById('modal-reject')
const botonCerrar2 = document.getElementById('boton-cerrar-2')


const fetchData = async () => {
    // const res = await fetch('/user/getstock');
    // data = await res.json()
    data = JSON.parse(document.getElementById('pedidos-db').value)
    users = JSON.parse(document.getElementById('usuarios-db').value)
    // console.log(data)
    dataFiltrada = data
    data.forEach(pedido =>{
        pedido.pedido = JSON.parse(pedido.pedido)
    })
    console.log(data)
    console.log(users)
    pintarCards(data)
}

const pintarCards = data => {
    data.forEach(pendiente =>{
        // console.log(pendiente)
        let usuario;
        users.forEach(user =>{if (user.id == pendiente.autor_id){usuario = user}})
        if(usuario.first_name.length == 0){
            templateCard.querySelector('.card-header-title').innerHTML = `${usuario.username} #${pendiente.id}`}
        else{
            templateCard.querySelector('.card-header-title').innerHTML = `${usuario.username} (${usuario.last_name} ${usuario.first_name}) #${pendiente.id}`}
        templateCard.querySelector('time').innerHTML = transformarHora(pendiente.hora)
        templateCard.querySelector('.card').dataset.id = pendiente.id
        templateCard.querySelector('.herrs').innerHTML = ''
        let c = 0;
        pendiente.pedido.forEach(item =>{
            c++;
            templateHerramienta.querySelector('i').classList.remove('fa-toolbox'); 
            templateHerramienta.querySelector('i').classList.remove('fa-tools'); 
            templateHerramienta.querySelector('i').classList.remove('fa-question-circle');
            templateHerramienta.querySelector('a').classList.remove('expandir');

            if (c<3 || pendiente.pedido.length <=3){
                // console.log(item) 
                if      (item.clase == 1){templateHerramienta.querySelector('i').classList.add('fa-toolbox');         }
                else if (item.clase == 2){templateHerramienta.querySelector('i').classList.add('fa-tools');           }  
                else                     {templateHerramienta.querySelector('i').classList.add('fa-question-circle'); }
                templateHerramienta.querySelector('p.nombre-herr').innerHTML = `${item.nombre} <b>x${item.cantidad}</b>` }
            else if (c==3){ 
                templateHerramienta.querySelector('i').classList.add('fa-question-circle');
                templateHerramienta.querySelector('p.nombre-herr').innerHTML = `<b>Haga click para ver más (${pendiente.pedido.length -2})</b>`
                templateHerramienta.querySelector('a').classList.add('expandir')
            }
            if (c<=3){
            const subClone = templateHerramienta.cloneNode(true)
            subFragment.appendChild(subClone)}
        })
        templateCard.querySelector('.herrs').appendChild(subFragment)

        const clone = templateCard.cloneNode(true)
        fragment.appendChild(clone)
    })
    columnas.appendChild(fragment)

}
function transformarHora(dato){
    // YYYY-MM-DD T HH:MM:SS.xxxZ
    dato = dato.split('T')
    dato[0] = dato[0].split('-')
    dato[1] = dato[1].split(':')
    finalDato = `${dato[0][2]}/${dato[0][1]}/${dato[0][0]} - ${dato[1][0]}:${dato[1][1]}hs.`
    return finalDato;
}

columnas.addEventListener('click', (e)=>{
    e.stopPropagation()
    let selected = e.target
    if (selected.classList.contains('fas')){selected = selected.parentNode}
    if (selected.classList.contains('panel-icon')){selected = selected.parentNode}
    if (selected.tagName.toLowerCase() == 'b'){selected = selected.parentNode}
    if (selected.tagName.toLowerCase() == 'p'){selected = selected.parentNode}
    if (selected.classList.contains('expandir')){
        console.log('EXPANDIR '+selected.parentNode.parentNode.parentNode.parentNode.dataset.id)
        expandirModal(selected.parentNode.parentNode.parentNode.parentNode.dataset.id)
    }
    if (selected.classList.contains('aprobar')){
        console.log('APROBAR '+selected.parentNode.parentNode.dataset.id)
        prepararPOST(selected.parentNode.parentNode.dataset.id,'apruebo','')
    }
    if (selected.classList.contains('rechazar')){
        console.log('RECHAZAR '+selected.parentNode.parentNode.dataset.id)
        panelRechazar(selected.parentNode.parentNode.dataset.id)
    }
        // console.log(selected)

})

function expandirModal(id){
    let pedidoActual;
    let usuarioActual;
    data.forEach(pedido=>{if (pedido.id == id)                 {pedidoActual = pedido}})
    users.forEach(user=> {if (pedidoActual.autor_id == user.id){usuarioActual = user }})
    // console.log(pedidoActual)
    // console.log(usuarioActual)
    if(usuarioActual.first_name.length == 0){
         modal.querySelector('.modal-card-title').innerHTML =  `${usuarioActual.username} #${pedidoActual.id}`}
    else{modal.querySelector('.modal-card-title').innerHTML =  `${usuarioActual.username} (${usuarioActual.last_name} ${usuarioActual.first_name}) #${pedidoActual.id}`}
    modal.querySelector('time').innerHTML = transformarHora(pedidoActual.hora)
    modal.querySelector('.herrs').innerHTML = ''
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
botonCerrar2.addEventListener('click',function(){modalRechazo.classList.remove('is-active')})

function panelRechazar(id){
    modalRechazo.dataset.id = id
    console.log(modalRechazo)
    modalRechazo.classList.add('is-active')
}
modalRechazo.querySelector('.button.is-danger').addEventListener('click',function(){
    if (modalRechazo.querySelector('.textarea').value.length == 0){
        modalRechazo.querySelector('#error').innerHTML = 'No puedes dejar este campo vacio.'}
    else{prepararPOST(modalRechazo.dataset.id,'rechazo',modalRechazo.querySelector('.textarea').value)}
    // console.log(modalRechazo.querySelector('.textarea').value)
})

