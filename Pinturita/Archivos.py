import string
import ast
from pathlib import Path
from os import path as pt

    
#Devuelve la ubicacion del proyecto
DIRECCION = Path(__file__).resolve().parent.parent
#Nos va a facilitar en la gestion de los archivos
#Funciones de para condiciones
def Igualar(valor1,valor2) ->bool:
    return valor1==valor2

def Mayor(valor1,valor2) -> bool:
    return valor1>valor2
    
def Menor(valor1,valor2) -> bool:
    return valor1<valor2
    
def Mayorigual(valor1,valor2) ->bool:
    return valor1>=valor2
    
def Menorigual(valor1,valor2) ->bool:
        return valor1<=valor2
    
def Diferente(valor1,valor2) -> bool:
    return valor1!=valor2
    
#En esta constante guardaremos una lista de todas las condiciones disponibles    
CONDICION:dict= {"=":Igualar,">":Mayor,">=":Mayorigual,"<=":Menorigual,
            "!=":Diferente,"<":Menor}

class Archivo():

    #Esta funcion indica que iniciar cada vez que se realice un objecto de esta CLASE
    def __init__(self,archivo:string) -> None:  # type: ignore
        #Indica la ruta del archivo solicitado
        self.RUTA= pt.join(DIRECCION,f"Archivos/{archivo}.txt")
        self.RUTA= pt.abspath(self.RUTA)
                
    #Funcion que sirve para insertar nueva información en el archivo de texto
    #Acepta como parametro, el objeto en si, la comprabacion guarda si se insertara la informacion
    #si cumple siertas condiciones, CONDIPARAMETRO guarda laa condiciones que necesitamos para ingresar
    #la información 
    def Insertar(self,Info,Comprobacion:bool=True,CONDIPARAMETRO="") -> None:
        Entrar:bool=True
        #Si queremos que la informacion se ingrese si cumple ciertas condiciones ejecutara el siguiente codigo
        if Comprobacion:
            #Verifica si le mandamos un areglo con las condiciones
            if CONDIPARAMETRO!="":
                CONDIFINAL=CONDIPARAMETRO
            else:
                #En caso que no hayamos enviado condiciones, la unica condicion que se hara para ingresar la informacion
                #Es que el ID sea diferente al id de las demas funciones
                CONDIFINAL=[{"KEY":"ID","VALOR":Info["ID"],"COND":CONDICION["="]}]
            #Extraemos la informacion del archivo con las condiciones dadas
            Dicc=  self.Extraer(CONDIFINAL)
            #Extraemos las posiciones de los registros que cumplieron con las condiciones
            Posiciones=Dicc["Posiciones"]
            #Verificamos si el numero de registros es igual a 0
            Entrar=len(Dicc["Registros"])==0
            #Si no se encontro registros, se ingresara un nuevo registro con la información recibida
        if Entrar:
            with open(self.RUTA,"a") as Arc:
                Arc.write(str(Info)+"\n")
        #En caso contrario solo actualizaremos los registros que coinciden con las condiciones
        else:
            self.Actualizar(CONDIFINAL,Info,Posiciones)
            
    #Esta función sirve para actualizar los registros en los archivos
    #Los parámetros son, el objecto en si, el nuevo registro, y  las posiciones de coincidencias 
    def Actualizar(self,Llave,Nuevo:dict,Posiciones) -> None:
        #Creamos un areglo para guardar los registros de las posiciones dadas
        Contenido=[]
        #Abrimos el archivo solicitado en modo leer 
        with open(self.RUTA,"r") as Archivo:
            Contenido= Archivo.read()
            #Separamos cada linea para tener cada registro
            Contenido= Contenido.split("\n")
            #Hacemos un ciclo que recorra las posiciones que necesitamos 
            for i in Posiciones:
                #Hacemos esa linea de código un diccionario
                Lin= ast.literal_eval(Contenido[i])
                #Y cambiamos todos los valores de ese registro
                for Key,Valor in Nuevo.items():
                    Lin[Key]=Valor
                Contenido[i]=str(Lin)
        #Sobreescribimos todo el archivo txt    
        with open(self.RUTA,"w") as Archivo:
            for i in Contenido:
                if i!="":
                    Archivo.write(i+"\n")
        
            
                                
                            
                    
    #Esta función permite extraer información de los archivos txt
    #Los parámetros son el mismo objecto y las condiciones        
    def Extraer(self,Llave="") -> dict:
        #Abrimos el archivo en modo lectura
        with open(self.RUTA,"r") as Archivo:
            Contenido= Archivo.read()
            #Separamos la informacion en un salto de linea para extraer los registros
            Contenido= Contenido.split("\n")
            Diccionarios=[]
            Posiciones=[]
            #En este ciclo extraemos la informacion con las condiciones dadas
            for index,i in enumerate(Contenido):
                #Miramos si la linea no esta vacia
                if i!="":
                    #La linea la convertimos en un diccionario
                    Lin=ast.literal_eval(i)
                    #Verificamos si hay condiciones
                    if Llave!="":
                        Valid:bool=True 
                        #Verificamos si el registro cumple con las condiciones en el siguiente ciclo
                        for Cond in Llave:
                            #Si no cumple con alguna condicion, cerrara el ciclo
                            if not Cond["COND"](Lin[Cond["KEY"]],Cond["VALOR"]):
                                Valid=False
                                break
                        #Si cumplió con todas las condiciones extraeremos esa linea
                        if Valid:
                            #Guardamos la posicion en el archivo donde se encuentra el archivo
                            Posiciones.append(index)
                            #Y guardamos el registro
                            Diccionarios.append(Lin)    
                    else:  
                        #Si no hubo condiciones solo se extraerá la linea     
                        Diccionarios.append(Lin)
        #Devolvemos una lista con los  registros y las posiciones de los registros
        return {"Registros" :Diccionarios,"Posiciones":Posiciones}
    #Esta funcion devolvera el numero de registros que hay en el archivo
    def Lineas(self) -> int:
        Contenido=[]
        #Abrimos el archivo en modo leer
        with open(self.RUTA,"r") as Archivo: 
            Contenido= Archivo.read()
            #Lo separamos por saltos de linea
            Contenido= Contenido.split("\n")
            #Devolvemos el tamaño del areglo
        return len(Contenido)
                