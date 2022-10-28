from asyncio.windows_events import NULL
import string
from django.shortcuts import redirect, render
from Pinturita.Archivos  import Archivo, CONDICION as Condi
from pathlib import Path
import datetime
from Pinturita.User64 import Decodificar,Verificar_autenticacion as Authen 
UserName=""

def Obtener_dic(papu,Archimas):
    if papu.method=="POST":
        Dic= papu.POST.dict()
        if Archimas!="":
            Archimas= Archimas.split("3")
            Lista= []
            Eliminar=[]
            Archivito= Archivo(Archimas[0])
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
                registros[Archimas[1]]=Dic["ID"]
                Archivito.Insertar(registros,False)
                if Archimas[1]=="TRANSACCION":
                    if "BOD_ENTRADA" in Dic:
                        CONDPALABRA=[{"KEY":"BODEGA","VALOR":Dic["BOD_ENTRADA"],"COND":Condi["="]}
                                                        , {"KEY":"PRODUCTO","VALOR":registros["PRODUCTO"],"COND":Condi["="]}]
                        ArchCompra= Archivo("Bodega2producto").Extraer(CONDPALABRA)["Registros"]
                        if len(ArchCompra)>0:
                            ArchCompra[0]["STOCK"]= str(int(ArchCompra[0]["STOCK"])+ int(registros["CANTIDAD"]))
                            ArchCompra= ArchCompra[0]
                        else:
                            ArchCompra={"PRODUCTO": registros["PRODUCTO"],"STOCK": registros["CANTIDAD"],"BODEGA": Dic["BOD_ENTRADA"] }
                        Archivo("Bodega2producto").Insertar(ArchCompra,True,CONDPALABRA)
                    
                    if "BOD_SALIDA" in Dic:
                        CONDPALABRA=[{"KEY":"BODEGA","VALOR":Dic["BOD_SALIDA"],"COND":Condi["="]}
                                                        , {"KEY":"PRODUCTO","VALOR":registros["PRODUCTO"],"COND":Condi["="]}]
                        ArchCompra= Archivo("Bodega2producto").Extraer(CONDPALABRA)["Registros"][0]
                        ArchCompra["STOCK"]= str(int(ArchCompra["STOCK"])-int(registros["CANTIDAD"]))
                        Archivo("Bodega2producto").Insertar(ArchCompra,True,CONDPALABRA)
                    
        del(Dic['csrfmiddlewaretoken'])
        return Dic
    return NULL

def Crear_Dic_Base(Ruta,request):
    Lineas:int= Archivo(Ruta).Lineas()
    Usuario=  Decodificar(request.session.get("User"))
    Datos= {"IDNO":Lineas,"CREADOR":Usuario[1]}
    return Datos

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
        Dic=Crear_Dic_Base(Nom_Archivo,request)
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


def Bodega_edicio(request):
    if Authen(request):
        Datos= Crear_Dic_Base("Bodegas",request)
        Datos["Productos"]= Archivo("Producto").Extraer()["Registros"]
        return render(request,"Bodegas.html",Datos)
    return redirect("/")

def Usuario_edicion(request):
    if Authen(request):
        #Creamos nuestro diccionario, que pueda el numero de registro que tiene el archivo y el nombre del creador
        Datos= Crear_Dic_Base("Usuarios",request)
        #Llamamos la informacion de contacto y extrae la informacion especifica de contacto
        Datos["Empleados"]=Archivo("Contacto").Extraer([{"KEY":"TIPO","VALOR":"Empleados","COND":Condi["="]}])["Registros"]  # type: ignore
        #Muestra el archivo html o la vista y le pasa la informacion del diccionario
        return render(request,"Usuario.html",Datos)
    return redirect("/")


def Movimiento_Edicion(request,Tipo,Clase,Salida="*"):
    if Authen(request):
        Datos=Crear_Dic_Base("Transaccion",request)
        Datos["BOD_ENTRADA"]= Clase!=1
        Datos["BOD_SALIDA"]= Clase!=0
        Plural= ["Proveedores","Clientes","Empleados"] [Clase]
        Datos["TRANSACCION"]= ["Comprado","Vendido","Transferido"][Clase]
        No=str(Clase)
        Clase=["Proveedor","Cliente","Empleado"][Clase]
        Datos["Tipo"]=Tipo
        Datos["Clase"]=Clase
        Datos["URLMovimiento"]="Movimiento-"+Tipo+"-"+No+"-*"+"_Transaccion_Transaccion2producto3TRANSACCION"
        if Tipo=="Compras":
            Datos["Bodegas"]= Archivo("Bodegas").Extraer()["Registros"]
            Datos["Productos"]=Archivo("Producto").Extraer()["Registros"]
        else:
            if Tipo=="Ventas":
                Bodeg=Archivo("Bodegas").Extraer([{"KEY":"Ventas","VALOR":"Verdadero","COND":Condi["="]}])["Registros"][0]
                Datos["Bodegas"]=  {"NOMBRE":Bodeg["Nombre"],"ID": Bodeg["ID"]}
            else:
                if Salida!="*":
                    Bodeg=Archivo("Bodegas").Extraer([{"KEY":"ID","VALOR":Salida,"COND":Condi["="]}])["Registros"][0]
                else:
                    Bodeg=Archivo("Bodegas").Extraer([{"KEY":"ID","VALOR":"1","COND":Condi["="]}])["Registros"][0]
                Datos["Bodegas"]= Archivo("Bodegas").Extraer()["Registros"]
                Datos["Bod"]= Bodeg
            Productos=Archivo("Bodega2producto").Extraer([{"KEY":"BODEGA","VALOR":Bodeg["ID"],"COND":Condi["="]}])["Registros"]
            ProdFinal=[]
            for prod in Productos:
                DICProducto=Archivo("Producto").Extraer([{"KEY":"ID","VALOR":prod["PRODUCTO"],"COND":Condi["="]}])["Registros"][0]
                DICProducto["STOCK"]=prod["STOCK"]
                ProdFinal.append(DICProducto)
            Datos["Productos"]=ProdFinal
        if Tipo=="Interno" and Salida=="*":
            Datos["Productos"]=Archivo("Producto").Extraer()["Registros"]
        Datos["Contactos"]= Archivo("Contacto").Extraer([{"KEY":"TIPO","VALOR":Plural,"COND":Condi["="]}])["Registros"]
        
        return render(request,"Movimiento.html",Datos)
    return redirect("/")

def  Contactos_edicion(request,Tipo):
    if Authen(request):
        Datos= Crear_Dic_Base("Contacto",request)
        Datos["Tipo"]=Tipo
        Datos["URLContac"]="Contactos-"+Tipo+"_Contacto"
        return render(request,"Contactos.html",Datos)
    return redirect("/")

def Producto_edicion(request):
    if Authen(request):
        Datos= Crear_Dic_Base("Producto",request)
        Datos["Tipos"]=Archivo("Tipo_Productos").Extraer()["Registros"]  # type: ignore
        Datos["Marca"]=Archivo("Marca").Extraer()["Registros"] # type: ignore
        Datos["Medida"]=Archivo("Producto_Medida").Extraer()["Registros"]  # type: ignore
        return render(request,"Producto.html",Datos)
    return redirect("/")