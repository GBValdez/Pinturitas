(function(){
    var Tabla=document.getElementById("Tabla");

    Tabla.addEventListener("change",(event)=>{
        if (event.target.classList.contains("CANTIDAD")){
            var Input=event.target;
            var Padre=Input.parentNode.parentNode;
            if (Input.dataset.tipo!="Compras"){
                var Cantidad= Padre.getElementsByClassName("STOCK")[0].value;
                if (parseInt(Input.value)>parseInt(Cantidad)){
                    console.log("Darle")
                    Input.value=Cantidad;
                }
            }
            Precio= Padre.getElementsByClassName("PRECIO")[0];
            Padre.getElementsByClassName("SUBTOTAL")[0].value=Input.value* Precio.value ;
        }
    })

})()