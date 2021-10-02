// -------------------------------------------------------declaraciones de DOM------------------------------
document.addEventListener('DOMContentLoaded', e => { fetchData() }); //cuando se carga la pag. se lee el JSON
//  (El JSON es provisional, ya que la base de datos va a estar en MySQL)
const fragment = document.createDocumentFragment() // Declaro el fragment, que uso para evitar el Reflow
const templateCard = document.getElementById('bloque-lista-buscar').content //Traigo el Template de los items de lista busqueda
const panelBusqueda = document.getElementById('panel-busqueda') // Declaro el "padre", es decir el panel busqueda que busca los items
let peticion = {}
let selectedCard
let data
let estaciones
let dataFiltrada = []
let dataFiltrada2 = []
let filtrado = 0
const templatePed = document.getElementById('bloque-lista-pedido').content
const panelPedido = document.getElementById('panel-pedido')
const templateVacio = document.getElementById('bloque-pedido-vacio').content
const botonEnviar = document.getElementById('Aceptbutton')
const botonSig = document.getElementById('sig-button')
const botonCerrar1 = document.getElementById('boton-cerrar-1')
const modalSig = document.getElementById('modal-envio')
const barraBusqueda = document.getElementById('searchBar1').querySelector('input')
const selectorBusqueda = document.querySelector('p.panel-tabs')
// no se como funciona esta parte del codigo, pero en resumen lee el JSON y deriva a la funcion pintarCards

const fetchData = async () => {
    // const res = await fetch('/user/getstock');
    // data = await res.json()
    data = JSON.parse(document.getElementById('stock-db').value)
    // console.log(data)
    dataFiltrada = data
    data.forEach(item =>{item.selected = false})
    console.log(data)
    pintarCards(data)
    estaciones = JSON.parse(document.getElementById('estaciones-db').value)
}
// panelBusqueda.addEventListener('click', e =>{
//     addPeticion(e)
// })

const pintarCards = data => {
    panelBusqueda.innerHTML = ""
    data.forEach(item => {
        templateCard.querySelector('p').textContent = item.nombre
        templateCard.querySelector('a.panel-block').dataset.id = item.id
        templateCard.querySelector('i').classList.remove('fa-toolbox'); 
        templateCard.querySelector('i').classList.remove('fa-tools'); 
        templateCard.querySelector('i').classList.remove('fa-question-circle'); 
        if      (item.clase == 1){templateCard.querySelector('i').classList.add('fa-toolbox');         }
        else if (item.clase == 2){templateCard.querySelector('i').classList.add('fa-tools');           }  
        else {                    templateCard.querySelector('i').classList.add('fa-question-circle'); }
        if(item.selected){templateCard.querySelector('a.panel-block').classList.add('tool-selected')}
        else{templateCard.querySelector('a.panel-block').classList.remove('tool-selected')}

        const clone = templateCard.cloneNode(true)
        fragment.appendChild(clone)
    })
    panelBusqueda.appendChild(fragment)}

panelBusqueda.addEventListener("click", (e)=>{  e.stopPropagation()
    selectedCard = undefined
    if      (e.target.classList.contains("panel-block")){selectedCard = e.target}
    else if (e.target.classList.contains("nombre-herr")){selectedCard = e.target.parentNode}
    else if (e.target.classList.contains("fas"))        {selectedCard = e.target.parentNode.parentNode}

//    console.log(selectedCard)
    if (selectedCard != undefined && !selectedCard.classList.contains("tool-selected")){
          selectedCard.classList.add("tool-selected")
          setPeticion(selectedCard) 
        //   console.log(selectedCard)
          data.forEach(item =>{
              if (item.id == selectedCard.dataset.id){item.selected = true}
          })
   }

})

const addPeticion = e => {
 //        console.log(e.target)
}

const setPeticion = objeto =>{
    // console.log(objeto)
    let herramienta = {
        id: parseInt(objeto.dataset.id),
        nombre: objeto.querySelector('.nombre-herr').textContent,
        clase: objeto.querySelector('i.fas').classList[1],
        cantidad: 1
    }
   // console.log(herramienta)
    peticion[herramienta.id] = {...herramienta}
    // console.log(peticion[herramienta.id])
    pintarPedido()
}

const pintarPedido = ()=>{
    panelPedido.innerHTML =""
    // console.log(peticion)
    Object.values(peticion).forEach(herramienta =>{
        templatePed.querySelector('.texto-ped-item').textContent = herramienta.nombre
        templatePed.querySelector('i.fas').classList.remove('fa-tools','fa-toolbox','fa-question-circle')
        templatePed.querySelector('i.fas').classList.add(herramienta.clase)
        templatePed.querySelector('.itemnum').value = herramienta.cantidad
        templatePed.querySelector('.panel-block').dataset.id = herramienta.id
        const clone = templatePed.cloneNode(true)
        fragment.appendChild(clone)
    })
    if (!Object.keys(peticion).length){
        const clone2 = templateVacio.cloneNode(true)
        fragment.appendChild(clone2)
    }
    panelPedido.appendChild(fragment)
}
pintarPedido()
const accionCantidad = panelPedido.addEventListener('click', (e)=>{
    // console.log(e.target)
    // const nCant = Object.values(peticion).reduce((acc,{cantidad}) => acc + cantidad,0)
    const pedActual = e.target.parentNode.parentNode.parentNode.parentNode.parentNode
    if(e.target.classList.contains('suma')){
        // const pedActual = e.target.parentNode.parentNode.parentNode.parentNode.parentNode
        // console.log(pedActual)
        peticion[parseInt(pedActual.dataset.id)].cantidad++
    }
    if(e.target.classList.contains('resta')){
        // const pedActual = e.target.parentNode.parentNode.parentNode.parentNode.parentNode
        // console.log(pedActual)
        if(peticion[parseInt(pedActual.dataset.id)].cantidad>1)
        peticion[parseInt(pedActual.dataset.id)].cantidad--
    }
    if(e.target.classList.contains('eliminar')){
        const pedActual2 = pedActual.querySelector('.panel-block')
        const idBorrada = peticion[pedActual2.dataset.id].id
        delete (peticion[pedActual2.dataset.id])
        // console.log(peticion)
        desTachar(idBorrada)
        // console.log(peticion)
    }
    pintarPedido()

})

function desTachar (id){
    // console.log(panelBusqueda.getElementByDataId(id))
    const tachado = panelBusqueda.querySelector(`[data-id="${id}"]`)
    tachado.classList.remove('tool-selected')
    data.forEach(item=>{if(id == tachado.dataset.id){item.selected = false}})
}




const filtrar = ()=>{
    dataFiltrada = []    
    const texto = barraBusqueda.value.toLowerCase()
    // console.log('-')
    for(herramienta of data){
        let nombre = herramienta.nombre.toLowerCase()
        if(nombre.indexOf(texto) !== -1){
            // console.log(nombre)
            if (filtrado == 0 ){dataFiltrada.push(herramienta)}
            if (filtrado == 2 ){if(herramienta.clase == filtrado){dataFiltrada.push(herramienta)}}
            if (filtrado == 1 ){if(herramienta.clase == filtrado){dataFiltrada.push(herramienta)}}
        }
        // if(!texto){pintarCards(data)}
    }
    pintarCards(dataFiltrada)}

barraBusqueda.addEventListener('keyup', ()=>filtrar())
selectorBusqueda.addEventListener('click', e=>{
    if (!e.target.classList.contains('panel-tabs')){
        dataFiltrada2 = []
    const filtro = selectorBusqueda.querySelectorAll('a')
    // console.log(filtro)
    for (i of filtro){if (i.classList.contains('is-active')){i.classList.remove('is-active')}}
    e.target.classList.add('is-active')
    if      (e.target.textContent == "Todos"){filtrado = 0}
    else if (e.target.textContent == "Herramientas"){filtrado = 2}
    else if (e.target.textContent == "Insumos"){filtrado = 1}
    // console.log(filtrado)
    filtrar()
}})

botonSig.addEventListener('click',function(){
    // console.log(peticion)
    if (Object.values(peticion).length > 0){
        modalSig.querySelector('select').innerHTML = '<option value="0">----------</option>'
        estaciones.forEach(estacion=>{
            modalSig.querySelector('select').innerHTML += `<option value="${estacion.id}">${estacion.nombre}</option>`
        })
        modalSig.classList.add('is-active')
    }
    else{
        alert('Seleccione herramientas o insumos para hacer un pedido.')
    }
})
botonCerrar1.addEventListener('click',function(){
    modalSig.classList.remove('is-active')
})
