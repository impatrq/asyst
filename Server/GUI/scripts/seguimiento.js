const barra = document.querySelector('.steps')
// var estado = 0;
var estadoGuardado = 0;
function actualizar(estado){
    const items = barra.querySelectorAll('.step-item')
    // if (estado== estadoGuardado){
    //     return
    // }
    // else{estadoGuardado=estado}
    const etiquetas = ['is-active','is-completed','is-success','is-danger']
    console.log(items)
    for(let i=0;i<items.length;i++){
        for(let j=0;j<etiquetas.length;j++){
            items[i].classList.remove(etiquetas[j])
        }
    }

    if (estado == 0){
        items[0].classList.add('is-active')
    }
    else if (estado == 1){
        items[0].classList.add('is-completed')
        items[0].classList.add('is-success')
        items[1].classList.add('is-active')
    }
    else if (estado == 2){
        items[0].classList.add('is-completed')
        items[0].classList.add('is-success')
        items[1].classList.add('is-completed')
        items[1].classList.add('is-success')
        items[2].classList.add('is-active')
    }
    else if (estado == 3){
        items[0].classList.add('is-completed')
        items[0].classList.add('is-success')
        items[1].classList.add('is-completed')
        items[1].classList.add('is-success')
        items[2].classList.add('is-completed')
        items[2].classList.add('is-success')
        items[3].classList.add('is-completed')
        items[3].classList.add('is-success')
        document.getElementById('Devolbutton').disabled = false;
    }
    else if (estado ==4){
        items[0].classList.add('is-completed')
        items[0].classList.add('is-danger')
        items[0].querySelector('i.fa').classList.remove('fa-check')
        items[0].querySelector('i.fa').classList.add('fa-times')
    } 

// SI EL ESTADO ES 4 TENGO QUE MOSTRAR EL MSG DE RECHAZO
}


actualizar(document.getElementById('estado-db').value)
// setInterval(()=>{location.reload();console.log('a')},1000)