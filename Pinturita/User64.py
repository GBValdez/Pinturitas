import base64
import string

from Pinturita.Archivos import Archivo,CONDICION as condi

#Codifica a base 64 los textos que se le envié
def Codificar(Bitles:string):
    Bitles= Bitles.encode("ascii")
    Usuario = base64.b64encode(Bitles)
    Usuario=str(Usuario)
    Usuario= Usuario[2:len(Usuario)-1]
    return Usuario

#Decodifica de base64 los textos que reciba
def Decodificar(Bitles):
    Datos=base64.b64decode(Bitles)
    Datos= str(Datos)
    Datos= Datos[2:len(Datos)-1]
    Datos= Datos.split("-")
    return Datos
#Verifica si el usuario esta autenticado en cada vista
def Verificar_autenticacion(request) -> bool:
    #Extraemos la informacion de la sesion
    codigo=request.session.get("User",None)
    if codigo!=None:
        #Decodificamos el texto
        codigo = Decodificar(codigo)
        #Buscamos si ese usuario se encuentra en los archivos de usuarios
        Buscar=Archivo("Usuarios").Extraer([{"KEY":"ID","VALOR":codigo[0],"COND":condi["="]},
                                    {"KEY":"USERNAME","VALOR":codigo[1],"COND":condi["="]}])
        #Returnamos si el resultado de nuestra búsqueda
        return len(Buscar["Registros"])>0
    return False