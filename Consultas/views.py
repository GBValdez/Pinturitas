from Pinturita.Archivos import Archivo
from django.shortcuts import redirect, render
from Pinturita.Archivos import CONDICION as Condi
from Pinturita.User64 import Verificar_autenticacion as Authen
UserName=""

def Bodegas_Consultas(request):
    if Authen(request):
        Dicc= Obtener_dic("Bodegas",URLPA= "/Edicion/Bodegas/")
        return render(request,"Consulta/Bodegas_Consulta.html",Dicc)
    return redirect("/")

def Contactos_Consultas(request,Tipo:int):
    if Authen(request):
        Tipos=["Proveedores","Clientes","Empleados"]
        Tipos= Tipos[Tipo]
        Datos=Obtener_dic("Contacto",[{"KEY":"TIPO","VALOR":Tipos,"COND":Condi["="]}]
                          ,f"/Edicion/Contactos/{Tipos}/")
        Datos["Tipo"]=Tipos
        return render(request,"Consulta/Contacto_Consulta.html",Datos)
    return redirect("/")

def Facturas_Consulta(request):
    if Authen(request):
        return render(request,"Consulta/Facturas_Consulta.html")
    return redirect("/")


def Movimiento_Consulta(request,Tipo):
    if Authen(request):
        Plural=["Compras","Ventas","Interno"][Tipo]
        Tipos=["Compras","Ventas","Interno"]
        Tipos= Tipos[Tipo]
        Datos= Obtener_dic("Transaccion", [{"KEY":"TIPO","VALOR":Plural,"COND":Condi["="]}]
                           ,f"/Edicion/Movimiento/{Tipos}/{Tipo}/1/")
        Tipos=["Compras","Ventas","Interno"]
        Datos["Tipo"]=Plural
        Datos["Clase"]=Tipo
        return render(request,"Consulta/Movimiento_Consulta.html",Datos)
    return redirect("/")

def Producto_Consulta(request):
    if Authen(request):
        Dicc= Obtener_dic("Producto",URLPA="/Edicion/Productos/")
        return render(request,"Consulta/Producto_Consulta.html",Dicc)
    return redirect("/")

def Reporte_Inventario(request):
    if Authen(request):
        return render(request,"Consulta/Reporte_inventario.html")
    return redirect("/")

def Usuario_Consulta(request):
    if Authen(request):
        Dicc= Obtener_dic("Usuarios",URLPA="/Edicion/Usuarios/")
        return render(request,"Consulta/Usuario_Consulta.html",Dicc)    
    return redirect("/")
#Diccionario para obtener todas las consultas

def Obtener_dic(Nom_archivo,condiciones="",URLPA="") -> dict:
    Arch= Archivo(Nom_archivo).Extraer(condiciones)["Registros"]
    MasID=Archivo(Nom_archivo).Lineas() 
    Llaves=Arch[0].keys() if len(Arch)>0 else []
    Dic={"Encabezado":Llaves,"Valores": [Valor.values() for Valor in Arch],
         "URL":URLPA,"URLULTIMO": URLPA+str(MasID)}
    return Dic