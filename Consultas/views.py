import re
from django.shortcuts import render

def Bodegas_Consultas(request):
    return render(request,"Consulta/Bodegas_Consulta.html")

def Contactos_Consultas(request,Tipo:int):
    Tipos=["Proveedores","Clientes","Empleados"]
    Datos={"Tipo":Tipos[Tipo]}
    return render(request,"Consulta/Contacto_Consulta.html",Datos)

def Facturas_Consulta(request):
    return render(request,"Consulta/Facturas_Consulta.html")

def Interno_Consulta(request):
    return render(request,"Consulta/Interno_Consulta.html")

def Movimiento_Consulta(request,Tipo):
    Tipos=["Compras","Ventas","Interno"]
    Datos={"Tipo":Tipos[Tipo],"Clase":Tipo}
    return render(request,"Consulta/Movimiento_Consulta.html",Datos)

def Producto_Consulta(request):
    return render(request,"Consulta/Producto_Consulta.html")

def Reporte_Inventario(request):
    return render(request,"Consulta/Reporte_inventario.html")

def Usuario_Consulta(request):
    return render(request,"Consulta/Usuario_Consulta.html")    
# Create your views here.
0