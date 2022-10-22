from Pinturita.Archivos import Archivo
from django.shortcuts import render

def Bodegas_Consultas(request):
    Dicc= Obtener_dic("Bodegas")
    return render(request,"Consulta/Bodegas_Consulta.html",Dicc)

def Contactos_Consultas(request,Tipo:int):
    Tipos=["Proveedores","Clientes","Empleados"]
    Datos=Obtener_dic("Contacto",{"KEY":"TIPO","VALOR":Tipos[Tipo]})
    Datos["Tipo"]=Tipos[Tipo]
    return render(request,"Consulta/Contacto_Consulta.html",Datos)

def Facturas_Consulta(request):
    return render(request,"Consulta/Facturas_Consulta.html")

def Interno_Consulta(request):
    return render(request,"Consulta/Interno_Consulta.html")

def Movimiento_Consulta(request,Tipo):
    Plural=["Compras","Ventas","Interno"][Tipo]
    Datos= Obtener_dic("Transaccion", {"KEY":"TIPO","VALOR":Plural})
    Tipos=["Compras","Ventas","Interno"]
    Datos["Tipo"]=Tipos[Tipo]
    Datos["Clase"]=Tipo
    return render(request,"Consulta/Movimiento_Consulta.html",Datos)

def Producto_Consulta(request):
    Dicc= Obtener_dic("Producto")
    return render(request,"Consulta/Producto_Consulta.html",Dicc)

def Reporte_Inventario(request):
    return render(request,"Consulta/Reporte_inventario.html")


def Usuario_Consulta(request):
    Dicc= Obtener_dic("Usuarios")
    return render(request,"Consulta/Usuario_Consulta.html",Dicc)    
# Create your views here.

def Obtener_dic(Nom_archivo,condiciones="") -> dict:
    Arch= Archivo(Nom_archivo).Extraer(condiciones)
    Llaves=Arch[0].keys() if len(Arch)>0 else []
    Dic={"Encabezado":Llaves,"Valores": [Valor.values() for Valor in Arch]}
    return Dic