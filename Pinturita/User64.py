from asyncio.windows_events import NULL
import base64
import re
import string

from Pinturita.Archivos import Archivo,CONDICION as condi

def Codificar(Bitles:string):
    Bitles= Bitles.encode("ascii")
    Usuario = base64.b64encode(Bitles)
    Usuario=str(Usuario)
    Usuario= Usuario[2:len(Usuario)-1]
    return Usuario

def Decodificar(Bitles):
    Datos=base64.b64decode(Bitles)
    Datos= str(Datos)
    Datos= Datos[2:len(Datos)-1]
    Datos= Datos.split("-")
    return Datos

def Verificar_autenticacion(request) -> bool:
    codigo=request.session.get("User",None)
    if codigo!=None:
        codigo = Decodificar(codigo)
        Buscar=Archivo("Usuarios").Extraer([{"KEY":"ID","VALOR":codigo[0],"COND":condi["="]},
                                    {"KEY":"USERNAME","VALOR":codigo[1],"COND":condi["="]}])
        return len(Buscar["Registros"])>0
    return False