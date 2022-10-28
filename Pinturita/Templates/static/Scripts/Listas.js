( function (){
// emergente llama por el parametro id el elemento emergente este tiene como funcion verificar si el valor existe o no  
var Emergente=document.getElementById("Emergente");
//hace una copia del elemento 
var Emergcopia= Emergente.cloneNode(true);
//Remueve el elemento de la ventana
Emergente.remove()
//guarda el elemento del formulario en una variables   
var Formulario= document.getElementsByClassName("Formulario")[0];

//esta funcion bloquea la escritura al momento de mostrar el elemento
function Desenfocar(){
    document.activeElement.blur();
}

//este indica que el elemento aparecera al momento que el input pierda el enfoque 
Formulario.addEventListener("focusout",(event)=>{
    // este if verifica si el input tiene classe lista si lo tiene  generara la funcion si no no la ejecutara
    if (event.target.classList.contains("Listas")){
        //este llama la list que tenemos en el input y al momento de seleccionarlo guarda el elemento del data list
        let IDBUSCAR=event.target.getAttribute("list");
        let DATOS= document.getElementById(IDBUSCAR);
        var Tama_List=DATOS.children.length;
        var Paro=true;
        var Elegido=null
        var Blanco=false;
        // verifica si la informacion que ingreso el usuario no sean solamente espacios en blanco y tambien verifica que si se encuentra ingresado la informacion en la lista
        for(j=0;j<Tama_List;j++){
            let InputEntrante=DATOS.children[j].getAttribute("value")
            
            if(event.target.value.replace(/\s+/g, '').length==0){
                event.target.value=""
                Paro=false; 
                break;
            }
            
            if(InputEntrante == event.target.value){
                Paro=false;
                Elegido=DATOS.children[j]; 
                break;
            }


        }
        // este se ejecuta si la informacion no existe en la lista 
        if (Paro){
            //inserta l elemento en el body
            document.body.appendChild(Emergcopia);
            //guarda en una variable el elemento que acabamos de ingresar
            Emergente=document.getElementById("Emergente");
            //guarda el elemnto para mostrarlo en la nota "no se encontro (y el elemento)"
            document.getElementById("Emergente_Elemento").innerText=event.target.value;
            //Guarda el boton en la variable
            let Boton = document.getElementById("Emergente_exit")
            //indica la ruta al boton guardar
            let IDACTUAL= document.getElementById("ID").value;
            document.getElementById("Emergente_enlace").setAttribute("href","/Edicion/Ingresar_unico/"
                + event.target.dataset.archivo+"/"+event.target.value +"/" + event.target.dataset.direccion
                +"/"+IDACTUAL.toString())
            //es la funcion que realiza el boton de salir
            Boton.addEventListener("click",()=>{
                Emergente.remove();
                event.target.value="";
            })
            setTimeout(Desenfocar,2);
            Blanco=true

        }else if (event.target.classList.contains("CONINP") && Elegido!=null){

            Blanco=false;
            Demas_entrada=document.getElementsByClassName("CONINP");
            console.log(Demas_entrada.length)
            for ( entrada=0 ; entrada< Demas_entrada.length; entrada++){
                if (Demas_entrada[entrada].value == event.target.value && Demas_entrada[entrada]!= event.target){
                    event.target.value="";
                    Blanco=true;
                    alert("No puedes agregar dos registros con el mismo producto")
                    break;
                }
            }

        }else{
            if (document.getElementsByTagName("h2")[0].textContent =="Interno")
                {
            if (event.target.id=="Bodega_Salida"){
                
                let Numbod= event.target.value.split(",")[1];
                Numbod= Numbod.trimStart()
                window.location.href="/Edicion/Movimiento/Interno/2/"+ Numbod;
                
            }
            if (event.target.id=="Bodega_Entrada"){
                var Salida=document.getElementById("Bodega_Salida")
                if (event.target.value== Salida.value){
                    event.target.value="";
                    alert("La bodega salida no puede ser igual a la bodega de entrada")
                }
            }
        }
            Blanco=true;
        }
        
        if (event.target.classList.contains("CONINP")){
        Tabla=event.target.parentNode.parentNode;
        In_STOCK= Tabla.getElementsByClassName("STOCK")[0]; 
        if (In_STOCK!=null){ 
            In_STOCK.value=""
            if (!Blanco){
                In_STOCK.value =  parseFloat(Elegido.dataset.stock);
            }
        }
        In_STOCK= Tabla.getElementsByClassName("PRECIO")[0];
        if(In_STOCK!=null){
            In_STOCK.value=""
            Tabla.getElementsByClassName("CANTIDAD")[0].readOnly =true;
            Tabla.getElementsByClassName("CANTIDAD")[0].value="";
            Tabla.getElementsByClassName("SUBTOTAL")[0].value="";
            if (!Blanco){
                Tabla.getElementsByClassName("CANTIDAD")[0].readOnly =false;
                In_STOCK.value = parseFloat(Elegido.dataset.precio);
            }
        }
    }
        
    }
})


Formulario.addEventListener("submit",(e)=>{
    var Listas= document.getElementsByClassName("Listas");
    for (var i=0 ; i< Listas.length;i++){
        var Parar=true
        let IDBUSCAR=Listas[i].getAttribute("list");
        var Listdata= document.getElementById(IDBUSCAR);
        var Tama_List=Listdata.children.length;
        for(j=0;j<Tama_List;j++){
            if(Listdata.children[j].getAttribute("value") == Listas[i].value){
                Listas[i].value = Listdata.children[j].getAttribute("value")
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
        e.preventDefault();
    }
    else{
        for (var i=0;i< Listas.length;i++ ){
            Listas[i].value=Listas[i].value.split(",")[1]
            Listas[i].value= Listas[i].value.trimStart()
        }
    }
    
    

})


})()