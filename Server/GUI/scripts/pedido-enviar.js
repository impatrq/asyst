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

botonEnviar.addEventListener('click', function (){
    console.log(peticion)
    var peticionFinal = [modalSig.querySelector('select').value]
    if (modalSig.querySelector('select').value == 0){
        document.getElementById('error').innerHTML = 'Seleccione un area válida'
        return}
    const prepararPeticion = peticion =>{
        Object.values(peticion).forEach(elemento =>{
            console.log(elemento)
            if      (elemento.clase == 'fa-toolbox'){elemento.clase = 1}
            else if (elemento.clase == 'fa-tools'){elemento.clase = 2}
            peticionFinal.push(elemento)
        })
        peticionFinal.sort(function(a, b){
            if(a.nombre < b.nombre) { return -1; }
            if(a.nombre > b.nombre) { return 1; }
            return 0;
        })
        console.log(peticionFinal)
    }
    prepararPeticion(peticion)

    const csrftoken = getCookie('csrftoken');
    console.log(csrftoken)
    var http = new XMLHttpRequest();
    var url = "/user/pedir/";
    http.open("POST", url, true);
    http.setRequestHeader('X-CSRFToken', csrftoken);

    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) { 
        //aqui obtienes la respuesta de tu peticion
        alert(peticion);
        }
    }
    console.log(JSON.stringify(peticionFinal))
    http.send(JSON.stringify(peticionFinal));
})