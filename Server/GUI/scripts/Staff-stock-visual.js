const botonAdd = document.getElementById('add-stock')
const panelAdd = document.getElementById('panel-add')
const botonCerrar = document.getElementById('boton-cerrar')
document.addEventListener('DOMContentLoaded', e => { fetchData() });
const templateCard = document.getElementById('item-stock').content
const panel = document.querySelector('.bloque-lista')
const fragment = document.createDocumentFragment()
const barraBusqueda = document.getElementById('barra-busqueda')
const selectorBusqueda = document.querySelector('p.panel-tabs')
let dataFiltrada = []
let dataFiltrada2 = []
let filtrado = 0
const botonEditar = document.querySelector('.is-warning')
const fetchData = async () => {
    // const res = await fetch('/user/getstock');
    // data = await res.json()
    data = JSON.parse(document.getElementById('stock-db').value)
    // console.log(data)
    dataFiltrada = data
    console.log(data)
    pintarCards(data)
}

const pintarCards = data => {
    panel.innerHTML = ""
    data.forEach(item => {
        templateCard.querySelector('p.nombre-herr').innerHTML = `${item.nombre}<b class="cantidad"> x${item.cantidad}</b>`
        templateCard.querySelector('a.panel-block').dataset.id = item.id
        templateCard.querySelector('i').classList.remove('fa-toolbox'); 
        templateCard.querySelector('i').classList.remove('fa-tools'); 
        templateCard.querySelector('i').classList.remove('fa-question-circle'); 
        if      (item.clase == 1){templateCard.querySelector('i').classList.add('fa-toolbox');         }
        else if (item.clase == 2){templateCard.querySelector('i').classList.add('fa-tools');           }  
        else {                    templateCard.querySelector('i').classList.add('fa-question-circle'); }
        // console.log(templateCard.querySelector('.card-header-title'))
        // console.log(item.nombre)

        const clone = templateCard.cloneNode(true)
        fragment.appendChild(clone)
    }) 
    panel.appendChild(fragment)}


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


botonAdd.addEventListener('click',function(){datosModal(0);})
botonCerrar.addEventListener('click',function(){
    panelAdd.classList.remove('is-active')
})

panel.addEventListener("click", (e)=>{  //Si hago un click en el panel
    e.stopPropagation()
    if      (e.target.classList.contains("is-warning")){ // Si es el boton amarillo
        selectedCard = e.target.parentNode.parentNode    // agarro la base de la card
        // console.log(selectedCard)
        datosModal(selectedCard.dataset.id)
    }
    else if (e.target.classList.contains("is-danger")){
        selectedCard = e.target.parentNode.parentNode    // agarro la base de la card
        borrarElemento(selectedCard.dataset.id)
    }
})

function datosModal(id){
    let herrEdit;
    if (id != 0){
        data.forEach(herramienta =>{
            if (id == herramienta.id){
                herrEdit = herramienta
                // console.log(herramienta)
                panelAdd.querySelector('.card-header-title').innerHTML = `Editar #${herrEdit.id}`
            }})}
    else{
        herrEdit = {id:0,nombre:'',cantidad:null,clase:0}
        panelAdd.querySelector('.card-header-title').innerHTML = `Agregar al stock`
    }
    panelAdd.dataset.id = herrEdit.id
    console.log(herrEdit)
    panelAdd.classList.add('is-active')
    panelAdd.querySelector('select').selectedIndex = herrEdit.clase
    panelAdd.querySelector('.input.name').value = herrEdit.nombre
    panelAdd.querySelector('.input.num').value = herrEdit.cantidad
    // console.log(panelAdd.querySelector('select').selectedIndex)
    // console.log(panelAdd)
}

