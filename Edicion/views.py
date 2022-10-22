from asyncio.windows_events import NULL
from importlib.resources import path
from re import A
import string
from tkinter import Place
from typing import List
from django.conf import Settings
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
import os
from Pinturita.Archivos  import Archivo
from pathlib import Path
import datetime
DIRECCION = Path(__file__).resolve().parent.parent
print("Direccion papu" + str(DIRECCION))

def Obtener_dic(papu,Archimas):
    if papu.method=="POST":
        Dic= papu.POST.dict()
        if Archimas!="":
            Lista= []
            Eliminar=[]
            Archivito= Archivo(Archimas)
            for llave in Dic.keys():
                if llave[0]=="_":
                    Registros= papu.POST.getlist(llave)
                    Eliminar.append(llave)
                    for j in range(0,len(Registros)):
                        if len(Lista)-1< j:
                            Lista.append({})
                        Lista[j][llave[1:len(llave)]]= Registros[j]
            for llave in Eliminar:
                del Dic[llave]
            for registros in Lista:
                registros["BODEGA"]=Dic["ID"]
                Archivito.Insertar(registros,False)
        del(Dic['csrfmiddlewaretoken'])
        return Dic
    return NULL

def Crear_Dic_Base(Ruta):
    Lineas:int= Archivo(Ruta).Lineas()
    Datos= {"IDNO":Lineas,"CREADOR":"GBValdez"}
    return Datos


def Bodega_edicio(request):
    Datos= Crear_Dic_Base("Bodegas")
    Datos["Productos"]= Archivo("Producto").Extraer()
    return render(request,"Bodegas.html",Datos)



def Ingresar(request,Tipo):
    Palabras = Tipo.replace("-","/")
    Palabras= Palabras.split("_")
    ArchiMAS:string=""
    if len(Palabras)==3:
        ArchiMAS=Palabras[2]
        
    Dic=Obtener_dic(request,ArchiMAS)
    if Dic!=NULL:
        Dic['Dia']= datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        Usuario= Archivo(Palabras[1])
        Usuario.Insertar(Dic,True)
    return redirect("/Edicion/"+Palabras[0])

def Ingresar_unicos(request,Nom_Archivo,Valor,Vista):
    #Verifica si el nombre del archivo no es Dir
    if Nom_Archivo!="Dir":
        #crea el diccionario 
        Dic=Crear_Dic_Base(Nom_Archivo)
        #cambiamos el IDNO a ID
        Dic["ID"]= Dic["IDNO"]
        #eliminamos IDNO
        del Dic["IDNO"]
        #colocamos valor al Nombre
        Dic["Nombre"]=Valor
        #Ingresamos la fecha y hora que se esta ejecutando
        Dic['Dia']= datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        #guardamos la info del diccionario
        Arch= Archivo(Nom_Archivo)
        Arch.Insertar(Dic)
        #la url nos dirige denuevo a la vista
    url=Vista.replace("_","/")
    return redirect("/Edicion/"+url)


def Usuario_edicion(request):
    #Creamos nuestro diccionario, que pueda el numero de registro que tiene el archivo y el nombre del creador
    Datos= Crear_Dic_Base("Usuarios")
    #Llamamos la informacion de contacto y extrae la informacion especifica de contacto
    Datos["Empleados"]=Archivo("Contacto").Extraer({"KEY":"TIPO","VALOR":"Empleados"})  # type: ignore
    #Muestra el archivo html o la vista y le pasa la informacion del diccionario
    return render(request,"Usuario.html",Datos)

def Clientes_edicion(request):
    Datos= Crear_Dic_Base("Usuarios")
    return render(request,"Clientes.html")

def Movimiento_Edicion(request,Tipo,Clase):
    Datos=Crear_Dic_Base("Transaccion")
    Datos["BOD_ENTRADA"]= Clase!=1
    Datos["BOD_SALIDA"]= Clase!=0
    Plural= ["Proveedores","Clientes","Empleados"] [Clase]
    No=str(Clase)
    Clase=["Proveedor","Cliente","Empleado"][Clase]
    Datos["Tipo"]=Tipo
    Datos["Clase"]=Clase
    Datos["URLMovimiento"]="Movimiento-"+Tipo+"-"+No+"_Transaccion_Transaccion2producto"
    Datos["Bodegas"]= Archivo("Bodegas").Extraer()
    Datos["Contactos"]= Archivo("Contacto").Extraer({"KEY":"TIPO","VALOR":Plural})
    Datos["Productos"]=Archivo("Producto").Extraer()
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