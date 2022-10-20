(function(){
    var Plant_Registro= document.getElementById("RegistroTabla").cloneNode(true)
    var Tabla= document.getElementById("Tabla");
    var Boton_Agregar= document.getElementById("BOTON_A_REGISTRO");
    Boton_Agregar.addEventListener("click",()=>{
        let NuevoRegistro= Plant_Registro.cloneNode(true);
        Tabla.appendChild(NuevoRegistro);
    })

    Tabla.addEventListener("click",(event)=>{
        if (event.target.className.split(" ").find(elemento => elemento=="BOTON_BORRAR")!=undefined){
            event.target.parentNode.parentNode.parentNode.remove();
        }
    })
})()