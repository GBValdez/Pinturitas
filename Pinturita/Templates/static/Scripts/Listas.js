( function (){
var Formulario= document.getElementsByClassName("Formulario")[0];
var Listas= document.getElementsByClassName("Listas");
var Emergente=document.getElementById("Emergente");
var Emergcopia= Emergente.cloneNode(true);
Emergente.remove()

function Desenfocar(){
    document.activeElement.blur();
}

for (var i=0;i<Listas.length;i++){
    Listas[i].addEventListener("blur",(e)=>{
        let IDBUSCAR=e.target.getAttribute("list");
        var DATOS= document.getElementById(IDBUSCAR);
        var Tama_List=DATOS.children.length;
        var Paro=true
        for(j=0;j<Tama_List;j++){
            let InputEntrante=DATOS.children[j].getAttribute("value")
            if(InputEntrante.length==1){
                Paro=false; 
                break;
            }
            
            if(InputEntrante == e.target.value){
                Paro=false; 
                break;
            }


        }
        if (Paro){
            document.body.appendChild(Emergcopia);
            Emergente=document.getElementById("Emergente");
            document.getElementById("Emergente_Elemento").innerText=e.target.value;
            let Boton = document.getElementById("Emergente_exit")
            var URLactual = window.location;
            document.getElementById("Emergente_enlace").setAttribute("href","/Edicion/Ingresar_unico/"+ e.target.dataset.archivo+"/"+e.target.value +"/" + e.target.dataset.direccion)
            //document.getElementById("Emergente_enlace").setAttribute("href",URLactual)
            Boton.addEventListener("click",()=>{
                Emergente.remove();
                e.target.value="";
            })
            setTimeout(Desenfocar,2);
            
        }
    })
}

Formulario.addEventListener("submit",(e)=>{
    for (var i=0 ; i< Listas.length;i++){
        var Parar=true
        let IDBUSCAR=Listas[i].getAttribute("list");
        var Listdata= document.getElementById(IDBUSCAR);
        var Tama_List=Listdata.children.length;
        for(j=0;j<Tama_List;j++){
            if(Listdata.children[j].getAttribute("value") == Listas[i].value){
                Parar=false;
                break;
            }
        }
        if (Parar){
            var Etiqueta= Listas[i].previousElementSibling.previousElementSibling      
            break;
        } 
        
    }
    if (Parar){
        alert("Error: Valor invalido\nEn " + Etiqueta.textContent + " elije un valor de la lista")
        e.preventDefault();
    }
    else{
        for (var i=0;i< Listas.length;i++ ){
            Listas[i].value=Listas[i].value.split(",")[1]
        }
    }
    
    

})


})()