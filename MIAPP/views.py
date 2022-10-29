import string
from django.shortcuts import redirect, render
from Pinturita.Archivos import Archivo,CONDICION as Condi
from Pinturita.User64 import Codificar
# Create your views here.

#Vista de nuestro LOGIN
def Login(request):
    return render(request,"Login/Login.html")

#Revisamos si el que logeo se encuentra registrado
def Revisar(request):
    #Recimos los datos del POST
    if request.method=="POST":
        #Volvemos esos datos en un diccionario 
        Respuesta=request.POST.dict()
        #Extraemos los registros que cumplan con las condiciones, uSERNAME y Contraseña esten en los registros
        Arch= Archivo("Usuarios").Extraer([{"KEY":"USERNAME","VALOR":Respuesta["USUARIO"],"COND":Condi["="]},
                                           {"KEY":"PASSWORD","VALOR":Respuesta["CLAVE"],"COND":Condi["="]}])["Registros"]
    #Verifica si se encontro mas de un registros con las condiciones dadas 
    if len(Arch)>0:
        #Concatenamos el id y el username y lo codificamos
        Bitles= Arch[0]["ID"]+"-"+Arch[0]["USERNAME"]
        Usuario= Codificar(Bitles)
        #Creamos una COOKIE que guarde nuestra sesion
        request.session["User"]=Usuario
        request.session.modified = True
        #Verificamos que tipo de usuario ingreso
        match Arch[0]["Rol"]:
            case "Vendedor":
                return redirect("/Consultas/Movimiento/1")
            case "Administrador":
                return redirect("/Consultas/Usuarios")
            case "Bodeguero":
                return redirect("/Consultas/Bodegas")
    return redirect("/")