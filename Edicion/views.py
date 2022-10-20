from asyncio.windows_events import NULL
from importlib.resources import path
from re import A
import string
from tkinter import Place
from django.conf import Settings
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
import os
from Pinturita.Archivos  import Archivo
from pathlib import Path
import datetime
DIRECCION = Path(__file__).resolve().parent.parent
print("Direccion papu" + str(DIRECCION))

def Obtener_dic(papu):
    if papu.method=="POST":
        Dic= papu.POST.dict()
        del(Dic['csrfmiddlewaretoken'])
        return Dic
    return NULL

def Crear_Dic_Base(Ruta):
    Lineas:int= Archivo(Ruta).Lineas()
    Datos= {"IDNO":Lineas,"CREADOR":"GBValdez"}
    return Datos


def Bodega_edicio(request):
    Datos= Crear_Dic_Base("Bodegas")
    return render(request,"Bodegas.html",Datos)

def Ingresar(request,Tipo):
    Palabras = Tipo.replace("-","/")
    Palabras= Palabras.split("_")
    Dic=Obtener_dic(request)
    if Dic!=NULL:
        Dic['Dia']= datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        Usuario= Archivo(Palabras[1])
        Usuario.Insertar(Dic)
    return redirect("/Edicion/"+Palabras[0])

def Ingresar_unicos(request,Nom_Archivo,Valor,Vista):
    if Nom_Archivo!="Dir":
        Dic=Crear_Dic_Base(Nom_Archivo)
        Dic["ID"]= Dic["IDNO"]
        del Dic["IDNO"]
        Dic["Nombre"]=Valor
        Dic['Dia']= datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        Arch= Archivo(Nom_Archivo)
        Arch.Insertar(Dic)
    url=Vista.replace("_","/")
    return redirect("/Edicion/"+url)


def Usuario_edicion(request):
    Datos= Crear_Dic_Base("Usuarios")
    Datos["Empleados"]=Archivo("Contacto").Extraer({"KEY":"TIPO","VALOR":"Empleados"})  # type: ignore
    return render(request,"Usuario.html",Datos)

def Clientes_edicion(request):
    Datos= Crear_Dic_Base("Usuarios")
    return render(request,"Clientes.html")

def Movimiento_Edicion(request,Tipo,Clase):
    Datos=Crear_Dic_Base("Transaccion_Pinturas")
    Datos["BOD_ENTRADA"]= Clase!=1
    Datos["BOD_SALIDA"]= Clase!=0
    Clase=["Cliente","Proveedor","Empleado"][Clase]
    Datos["Tipo"]=Tipo
    Datos["Clase"]=Clase
    Datos["URLMovimiento"]="Movimientos-"+Tipo+"-"+Clase+"_Transaccion_Pinturas" 
    return render(request,"Movimiento.html",Datos)

def  Contactos_edicion(request,Tipo):
    Datos= Crear_Dic_Base("Contacto")
    Datos["Tipo"]=Tipo
    Datos["URLContac"]="Contactos-"+Tipo+"_Contacto"
    return render(request,"Contactos.html",Datos)


def Producto_edicion(request):
    Datos= Crear_Dic_Base("Producto")
    Datos["Tipos"]=Archivo("Tipo_Productos").Extraer()  # type: ignore
    Datos["Marca"]=Archivo("Marca").Extraer()# type: ignore
    Datos["Medida"]=Archivo("Producto_Medida").Extraer()  # type: ignore
    return render(request,"Producto.html",Datos)