from django.shortcuts import redirect, render
from Pinturita.Archivos import Archivo,CONDICION as Condi
# Create your views here.
def Login(request):
    return render(request,"Login/Login.html")

def Revisar(request):
    if request.method=="POST":
        Respuesta=request.POST.dict()
        Arch= Archivo("Usuarios").Extraer([{"KEY":"USERNAME","VALOR":Respuesta["USUARIO"],"COND":Condi["="]},
                                           {"KEY":"PASSWORD","VALOR":Respuesta["CLAVE"],"COND":Condi["="]}])["Registros"]
    if len(Arch)>0:
        match Arch[0]["Rol"]:
            case "Vendedor":
                return redirect("/Consultas/Movimiento/1")
            case "Administrador":
                return redirect("/Consultas/Usuarios/")
            case "Bodeguero":
                return redirect("/Consultas/Usuarios/")
    return redirect("/")