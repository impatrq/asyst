const autoForm = document.getElementById('autoform')
const idField= document.getElementById('ped-id')
const statField= document.getElementById('ped-status')
const msgField= document.getElementById('ped-msg')
function prepararPOST(id,accion,msg){
    idField.value = id
    if (accion == 'apruebo'){statField.value = 2}
    if (accion == 'rechazo'){statField.value = 3}
    msgField.value = msg
    setTimeout(autoForm.submit(),500)
}

function cerrarModal(){
    window.location.href = window.location.href
}