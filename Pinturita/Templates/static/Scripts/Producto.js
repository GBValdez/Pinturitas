(function(){
    var Costo= document.getElementById("Precio_costo");
    var Precio= document.getElementById("Precio_venta");
    var Ganancia= document.getElementById("Ganancia");
    Costo.addEventListener("input",Gananciafun)
    Precio.addEventListener("input",Gananciafun)
    
    function Gananciafun(){
        
        Ganancia.value=Precio.value-Costo.value;
    }
    

})()