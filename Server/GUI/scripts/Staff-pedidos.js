var dataGet = ''
var enviar = false

async function getCarritos(){
    var request = new XMLHttpRequest();
    request.open('GET', '/carrito/?matricula=0', true);

    request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
        // Success!
        dataGet = JSON.parse(request.responseText);
        console.log(dataGet)
    } else {
        // We reached our target server, but it returned an error

    }
    };

    request.onerror = function() {
    // There was a connection error of some sort
    };
    request.send();
    return dataGet
}

function postOcupar(matricula){
    var http = new XMLHttpRequest();
    http.open("POST", '/carrito/', true);
    http.send(`${matricula}-ocupado-True`);

}
async function ocuparCarrito(){
    var encontrado = false;
    var dato_carro = getCarritos();
    console.log(dato_carro)
    setTimeout(function(){
    for (let carrito of dataGet){
       if (carrito.ocupado == false){
           mensajeOcupar(true,carrito.matricula);
           postOcupar(carrito.matricula);
           encontrado = true;
           enviar = true
           return true;
       }
    }
    if (!encontrado){
        mensajeOcupar(false);
        enviar = false
        return false;
    }},500)
    return enviar
}


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

function prepararPOST(id,accion,msg){
    if(accion=='rechazo'){enviar=true}
    let url ='/staff/pedidos/';
    if (accion == 'apruebo'){
        data = {'id':parseInt(id),'msg':msg,'estado':2}
        var respuesta = ocuparCarrito().then(function(){
            if (respuesta){enviar = true}            
            console.log('dentri del then',enviar)
        })
    }
    if(!enviar){return}
    else{
    if (accion == 'rechazo'){data = {'id':parseInt(id),'msg':msg,'estado':3}}
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
    //setTimeout(() => {  location.reload(); }, 200);
    console.log('RECARGA')  }
}

// function sendPost
