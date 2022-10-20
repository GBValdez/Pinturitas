(function(){
    var Plant_Registro= document.getElementById("RegistroTabla").cloneNode(true)
    var Tabla= document.getElementById("Tabla");
    var Boton_Agregar= document.getElementById("BOTON_A_REGISTRO");
    Boton_Agregar.addEventListener("click",()=>{
        var NuevoRegistro= Plant_Registro.cloneNode(true);
        var BotonR = NuevoRegistro.getElementById("BOTON_B_REGISTRO");
        BotonR.addEventListener("click",Borrar_registro);
        Tabla.appendChild(NuevoRegistro);
    })

    function Borrar_registro(event) {
        event.target.parentNode.remove();
    }

    var Boton_Eliminar= document.getElementsByClassName("BOTON_BORRAR");
    for (var i=0; i<Boton_Eliminar.length;i++){
        Boton_Eliminar[i].addEventListener("click",(e)=>{
            e.target.parentNode.remove();
        })
    }
})()