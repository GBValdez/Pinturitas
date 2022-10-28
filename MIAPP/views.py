import string
from django.shortcuts import redirect, render
from Pinturita.Archivos import Archivo,CONDICION as Condi
from Pinturita.User64 import Codificar
# Create your views here.
def Login(request):
    return render(request,"Login/Login.html")

def Revisar(request):
    if request.method=="POST":
        Respuesta=request.POST.dict()
        Arch= Archivo("Usuarios").Extraer([{"KEY":"USERNAME","VALOR":Respuesta["USUARIO"],"COND":Condi["="]},
                                           {"KEY":"PASSWORD","VALOR":Respuesta["CLAVE"],"COND":Condi["="]}])["Registros"]
    if len(Arch)>0:
        Bitles= Arch[0]["ID"]+"-"+Arch[0]["USERNAME"]
        Usuario= Codificar(Bitles)
        request.session["User"]=Usuario
        request.session.modified = True
        
        match Arch[0]["Rol"]:
            case "Vendedor":
                return redirect("/Consultas/Movimiento/1")
            case "Administrador":
                return redirect("/Consultas/Usuarios")
            case "Bodeguero":
                return redirect("/Consultas/Bodegas")
    return redirect("/")