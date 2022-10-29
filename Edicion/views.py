import string
from django.shortcuts import redirect, render
from Consultas import url
from Pinturita.Archivos  import Archivo, CONDICION as Condi
from pathlib import Path
import datetime
from Pinturita.User64 import Decodificar,Verificar_autenticacion as Authen 
UserName=""

#La siguiente función procesa la información enviada en los formularios para crear los registros
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
    return None

#Este la informacion base que se incrustara en los archivos html
def Crear_Dic_Base(Ruta,request,ID,URL):
    #Extraemos el total del lineas que tiene el documento para el ID
    Lineas:int= Archivo(Ruta).Lineas()
    #Extraemos el usuario la que tiene abierta la sesion
    Usuario=  Decodificar(request.session.get("User"))
    #Creamos un diccionario con la información
    Datos= {"IDNO":ID,"CREADOR":Usuario[1]}
    if ID==0:
        #Si el id de la url es 0, entnces IDNO sera el total de lineas del archivo
        Datos["IDNO"]=Lineas
    #La url para el form
    Datos["URLPASAR"]=f"/Edicion/Ingresar/{URL}"
    if ID=="":
         Datos["IDNO"]=Lineas           
    return Datos


#Esta funcion se ejecutara cuando se envié la información por los form
def Ingresar(request,Tipo):
    #Cambiamos algunos caracteres de la variable enviada por url
    Palabras = Tipo.replace("-","/")
    #Separamos la variable enviada por url
    Palabras= Palabras.split("_")
    #Remplazamos el * de todo el areglo que acabamos de hacer
    Otra= [pal.replace("*","_") for pal in Palabras]
    Palabras=Otra
    ArchiMAS:string=""
    #Si se encuentra 3 valores en el arreglo que acabamos de hacer, guardaremos en esta variable el 3er valor
    if len(Palabras)==3:
        ArchiMAS=Palabras[2]
    #Procesamos la informacion enviada para obtener un registro    
    Dic=Obtener_dic(request,ArchiMAS)
    if Dic!=None:
        #Guardamos en ese registro el dia que fue creado
        Dic['Dia']= datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        #Creamos un objecto de archivo para insertar la informacion
        Usuario= Archivo(Palabras[1])
        #Insertamos la información en el archivo
        Usuario.Insertar(Dic,True)
    #Regresamo a la vista consulta de la modulo que estamos
    return redirect("/Consultas/"+Palabras[0])


def Ingresar_unicos(request,Nom_Archivo,Valor,Vista,ID):
    #Verifica si el nombre del archivo no es Dir
    PREID=0
    if Nom_Archivo!="Dir":
        PREID=ID
        #crea el diccionario 
        Dic=Crear_Dic_Base(Nom_Archivo,request,"","")
        #cambiamos el IDNO a ID
        Dic["ID"]= Dic["IDNO"]
        #eliminamos IDNO
        del Dic["IDNO"]
        
        del Dic["URLPASAR"]
        del Dic["ACTUAREGISTRO"]
        #colocamos valor al Nombre
        Dic["Nombre"]=Valor
        #Ingresamos la fecha y hora que se esta ejecutando
        Dic['Dia']= datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        #guardamos la info del diccionario
        Arch= Archivo(Nom_Archivo)
        Arch.Insertar(Dic)
        #la url nos dirige de nuevo a la vista
    if PREID==0:
        ID=0
    url=Vista.replace("_","/")
    return redirect("/Edicion/"+url+"/"+str(ID))

#Vista de la bodega edicion
def Bodega_edicio(request,ID):
    #Verificamos si el usuario esta autenticado
    if Authen(request):
        #Creamos nuestra informacion base para incrustar en el archivo html
        Datos= Crear_Dic_Base("Bodegas",request,ID,"Bodegas_Bodegas")
        #Extraemos los productos que existen
        Datos["Productos"]= Archivo("Producto").Extraer()["Registros"]
        #Renderizamos nuestra vista
        return render(request,"Bodegas.html",Datos)
    return redirect("/")

#Vista de Usuario Edicion
def Usuario_edicion(request,ID):
    if Authen(request):
        #Creamos nuestro diccionario, que pueda el numero de registro que tiene el archivo y el nombre del creador
        Datos= Crear_Dic_Base("Usuarios",request,ID,"Usuarios_Usuarios")
        #Llamamos la informacion de contacto y extrae la informacion especifica de contacto
        Datos["Empleados"]=Archivo("Contacto").Extraer([{"KEY":"TIPO","VALOR":"Empleados","COND":Condi["="]}])["Registros"]  # type: ignore
        #Muestra el archivo html o la vista y le pasa la informacion del diccionario
        return render(request,"Usuario.html",Datos)
    return redirect("/")

#Vista de movimientos edicion
def Movimiento_Edicion(request,Tipo,Clase,Salida="*",ID=0):
    if Authen(request):
        Datos=Crear_Dic_Base("Transaccion",request,ID,"")
        Datos["BOD_ENTRADA"]= Clase!=1
        Datos["BOD_SALIDA"]= Clase!=0
        Plural= ["Proveedores","Clientes","Empleados"] [Clase]
        Datos["TRANSACCION"]= ["Comprado","Vendido","Transferido"][Clase]
        No=str(Clase)
        Clase=["Proveedor","Cliente","Empleado"][Clase]
        Datos["Tipo"]=Tipo
        Datos["Clase"]=Clase
        Datos["URLPASAR"]="/Edicion/Ingresar/Movimiento-"+No+"_Transaccion_Transaccion2producto3TRANSACCION"
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

#Vista para contactos edición
def  Contactos_edicion(request,Tipo,ID):
    if Authen(request):
        Tipos= str(["Proveedores","Clientes","Empleados"].index(Tipo))
        print("Valor "+Tipos)
        Datos= Crear_Dic_Base("Contacto",request,ID,f"Contactos-{Tipos}_Contacto")
        Datos["Tipo"]=Tipo
        Datos["URLContac"]="Contactos-"+Tipo+"_Contacto"
        return render(request,"Contactos.html",Datos)
    return redirect("/")

#Vista para producto edicion
def Producto_edicion(request,ID):
    if Authen(request):
        Datos= Crear_Dic_Base("Producto",request,ID,"Producto*Consulta_Producto")
        Datos["Tipos"]=Archivo("Tipo_Productos").Extraer()["Registros"]  # type: ignore
        Datos["Marca"]=Archivo("Marca").Extraer()["Registros"] # type: ignore
        Datos["Medida"]=Archivo("Producto_Medida").Extraer()["Registros"]  # type: ignore
        return render(request,"Producto.html",Datos)
    return redirect("/")