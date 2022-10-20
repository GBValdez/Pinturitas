
(function () {
    M_Desplegado=false;
Boton_menu=document.getElementById("Btn_Menu");
Panel= document.getElementById("HeadCabeza");
Boton_menu.addEventListener("click",()=>{
    console.log("hola");
    M_Desplegado=!M_Desplegado;
    if (M_Desplegado){
        Panel.className="HeadCabeza HeadComplete";
    }
    else{
        Panel.className="HeadCabeza";
    }
})

class Datos{
    constructor(Archivo){
        this._archivo = Archivo;
    }
    Ingresar(){

    }
}



/* 
object.OpenTextFile(filename[, iomode[, create[, format]]]) 
Parámetro 
object 
Requerido objeto debe ser el nombre de un FileSystemObject. 
filename 
Requerido Una expresión de cadena que indica el archivo a abrir. 
iomode 
Opcional Puede ser una de tres constantes: ForReading, ForWriting o ForAppending. 
create 
Opcional Valor booleano que indica si se debe crear un nuevo archivo cuando el nombre de archivo especificado no existe. El valor es True si se crea un nuevo archivo y False si no se crea. Si se omite, no se crea un nuevo archivo. 
format 
Opcional Use uno de los valores de tres estados para indicar el formato del archivo abierto. Si se omite, el archivo se abrirá en formato ASCII. 
Configurar 
El parámetro iomode puede ser cualquiera de las siguientes configuraciones: 
Descripción del valor constante 
ForReading 1 Abra el archivo como solo lectura. No se puede escribir este archivo. 
ForWriting 2 Abrir archivo para escribir 
ForAppending 8 Abra el archivo y comience a escribir desde el final del archivo. 

El parámetro de formato puede ser cualquiera de las siguientes configuraciones: 
Descripción del valor 
TristateTrue abre el archivo en formato Unicode. 
TristateFalse abre el archivo en formato ASCII. 
TristateUseDefault Abre el archivo con los valores predeterminados del sistema. 
*/ 

// leer archivo 
function readFile(filename){ 
var fso = new ActiveXObject("Scripting.FileSystemObject"); 
var f = fso.OpenTextFile(filename,1); 
var s = ""; 
while (!f.AtEndOfStream) 
s += f.ReadLine()+"\n"; 
f.Close(); 
return s; 
} 

// escribir archivo 
function writeFile(filename,filecontent){ 
    var fso, f, s ; 
    fso = new ActiveXObject("Scripting.FileSystemObject");    
    f = fso.OpenTextFile(filename,8,true); 
    f.WriteLine(filecontent);   
    f.Close(); 
alert('ok'); 
} 

/*
<html> 
<input type="text" id="in" name="in" /> 
<input type="button" value="Write!" onclick="writeFile('c:/12.txt',document.getElementById('in').value);"/><br><br> 
<input type="button" value="Read!" onclick="document.getElementById("__content").value=readFile('http://sc.stock.cnfol.com/090917/123,1282,6534044,00.shtml');"/><br> 
<textarea id="show" name="show" cols="100" rows="20" > 
</textarea> 
</html>
*/

})();