from genericpath import exists
from operator import truediv
from pickle import NONE
import string
import ast
from pathlib import Path

#Devuelve la ubicacion del proyecto
DIRECCION = Path(__file__).resolve().parent.parent

#Nos va a facilitar en la gestion de los archivos
class Archivo():
    #Esta funcion indica que iniciar cada vez que se realice un objecto de esta CLASE
    def __init__(self,archivo:string) -> None:  # type: ignore
        #Indica la ruta del archivo solicitado
        self.RUTA=str(DIRECCION)+"\\Archivos\\"+archivo+".txt"  # type: ignore
        
    #Verifica si hay algun parametro que se repite en todo el archivo de texto
    def Existe(self,Llave:string,Info) ->bool:  # type: ignore
        #Abrir el archivo en modo leer
        Arc= open(self.RUTA,"r")
        #Guardaremo todo el contenido del archivo en una variable
        Contenido= Arc.read()
        #Lo separamos en lineas y lo guardamos en un areglo
        Contenido= Contenido.split("\n")
        #Esta variable guardara si se encontro un registro con un atributo igual que nuestro diccionario
        Esta:bool=False
        #Recorremos cada linea del contenido
        for i in Contenido:
            #Verificamos si la linea no esta vacia
            if i!="":
                #Convertimos esa linea en un diccionario
                Dicc= ast.literal_eval(i)
                #Hacemos la comparacion de atributos
                if Dicc[Llave]==Info[Llave]:
                    Esta=True
                    break
        #Cerramos el archivo
        Arc.close()
        #Retornamos la respuesta
        return Esta
    
    #
    def Insertar(self,Info,Comprobacion:bool=True) -> None:
        Entrar:bool=True
        if Comprobacion:
            Entrar=not self.Existe("ID",Info)
        if Entrar:  
            Arc=open(self.RUTA,"a")
            Arc.write(str(Info)+"\n")
            Arc.close()
            
    def Extraer(self,Llave=""):
        Archivo= open(self.RUTA,"r")
        Contenido= Archivo.read()
        Contenido= Contenido.split("\n")
        Diccionarios=[]
        for i in Contenido:
            if i!="":
                Lin=ast.literal_eval(i)
                if Llave!="":
                    if Llave["VALOR"]== Lin[Llave["KEY"]]:  # type: ignore
                        Diccionarios.append(Lin) 
                else:       
                    Diccionarios.append(Lin)
        Archivo.close()
        return Diccionarios

    def Lineas(self) -> int:
        Archivo= open(self.RUTA,"r")
        Contenido= Archivo.read()
        Contenido= Contenido.split("\n")
        Archivo.close()
        return len(Contenido)
                