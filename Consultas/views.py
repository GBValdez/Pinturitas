from Pinturita.Archivos import Archivo
from django.shortcuts import redirect, render
from Pinturita.Archivos import CONDICION as Condi
from Pinturita.User64 import Verificar_autenticacion as Authen
UserName=""
#Vista bbodegas consulta
def Bodegas_Consultas(request):
    #Verificamos si el usuario esta autenticado
    if Authen(request):
        #Obtenemos la informacion para incustrar en la plantilla
        Dicc= Obtener_dic("Bodegas",URLPA= "/Edicion/Bodegas/")
        #Renderizamos nuestro html
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

#Esta funcion devolvera la informacion necesaria para mostrar en las vistas de consulta
#sus parametros es el nombre del archivo donde se estraera la informacion, las condiciones para extraer esa informacion
#y l url para ir las vistas edicion
def Obtener_dic(Nom_archivo,condiciones="",URLPA="") -> dict:
    #Extraemos los registros
    Arch= Archivo(Nom_archivo).Extraer(condiciones)["Registros"]
    #Extraemos el total de lineas de cada registro
    MasID=Archivo(Nom_archivo).Lineas() 
    #Esta variable guardara una lista de lo tipos de registros que hay para poner el encabezado de la tabla
    Llaves=Arch[0].keys() if len(Arch)>0 else []
    #Creamos nuestro dic
    Dic={"Encabezado":Llaves,"Valores": [Valor.values() for Valor in Arch],
         "URL":URLPA,"URLULTIMO": URLPA+str(MasID)}
    return Dic