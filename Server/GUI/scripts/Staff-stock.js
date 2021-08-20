panelAdd.querySelector('.card-footer-item').addEventListener('click',function(){
    console.log(panelAdd.dataset.id)
    dato = {}
    dato.id = parseInt(panelAdd.dataset.id)
    dato.nombre = panelAdd.querySelector('.input.name').value
    dato.nombre = dato.nombre.charAt(0).toUpperCase() + dato.nombre.slice(1);
    dato.cantidad = parseInt(panelAdd.querySelector('.input.num').value)
    dato.clase = parseInt(panelAdd.querySelector('select').selectedIndex)
    if(dato.nombre.length == 0 || dato.cantidad <= 0 || dato.clase == 0){
        panelAdd.querySelector('#error').innerHTML = 'Complete todos los campos.'}
    else {enviarAdb(panelAdd.dataset.id,dato)}
    console.log(dato)
})

function borrarElemento(id){enviarAdb(id,'borrar')}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function enviarAdb (targetID,data){
    let url ='';
    if        (data == 'borrar') {url=`/staff/stock/remove/${targetID}/`}
    else if   (targetID == 0)    {url = '/staff/stock/add/'}
    else                         {url = `/staff/stock/edit/${targetID}/`}
    const csrftoken = getCookie('csrftoken');
    console.log(csrftoken)
    var http = new XMLHttpRequest();
    http.open("POST", url, true);
    http.setRequestHeader('X-CSRFToken', csrftoken);

    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) { 
        //aqui obtienes la respuesta de tu peticion
        // alert(peticion);
        }
    }
    // console.log(peticionFinal)
    http.send(JSON.stringify(data));
    setTimeout(() => {  location.reload(); }, 200);
}
