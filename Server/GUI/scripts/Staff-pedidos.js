

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
    let url ='/staff/pedidos/';
    if (accion == 'apruebo'){data = {'id':parseInt(id),'msg':msg,'estado':2}}
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
    setTimeout(() => {  location.reload(); }, 200);
}