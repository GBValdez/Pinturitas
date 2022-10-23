import string
import ast
from pathlib import Path


    
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
    
CONDICION:dict= {"=":Igualar,">":Mayor,">=":Mayorigual,"<=":Menorigual,
            "!=":Diferente,"<":Menor}

class Archivo():

    #Esta funcion indica que iniciar cada vez que se realice un objecto de esta CLASE
    def __init__(self,archivo:string) -> None:  # type: ignore
        #Indica la ruta del archivo solicitado
        self.RUTA=str(DIRECCION)+"\\Archivos\\"+archivo+".txt"  # type: ignore
                
    
    def Insertar(self,Info,Comprobacion:bool=True) -> None:
        Entrar:bool=True
        if Comprobacion:
            Dicc=  self.Extraer([{"KEY":"ID","VALOR":Info["ID"],"COND":CONDICION["="]}])
            Posiciones=Dicc["Posiciones"]
            Entrar=len(Dicc["Registros"])==0
        if Entrar:
            with open(self.RUTA,"a") as Arc:
                Arc.write(str(Info)+"\n")
        else:
            self.Actualizar([{"KEY":"ID","VALOR":Info["ID"],"COND":CONDICION["="]}],Info,Posiciones)
    
    
    def Actualizar(self,Llave,Nuevo:dict,Posiciones) -> None:
        Contenido=[]
        with open(self.RUTA,"r") as Archivo:
            Contenido= Archivo.read()
            Contenido= Contenido.split("\n")
            for i in Posiciones:
                Lin= ast.literal_eval(Contenido[i])
                for Key,Valor in Nuevo.items():
                    Lin[Key]=Valor
                Contenido[i]=str(Lin)
            
        with open(self.RUTA,"w") as Archivo:
            for i in Contenido:
                Archivo.write(i+"\n")
        
            
                                
                            
                    
            
    def Extraer(self,Llave="") -> dict:
        with open(self.RUTA,"r") as Archivo:
            Contenido= Archivo.read()
            Contenido= Contenido.split("\n")
            Diccionarios=[]
            Posiciones=[]
            for index,i in enumerate(Contenido):
                if i!="":
                    Lin=ast.literal_eval(i)
                    if Llave!="":
                        Valid:bool=True 
                        for Cond in Llave:
                            if not Cond["COND"](Lin[Cond["KEY"]],Cond["VALOR"]):
                                Valid=False
                                break
                        if Valid:
                            Posiciones.append(index)
                            Diccionarios.append(Lin)    
                    else:       
                        Diccionarios.append(Lin)
        return {"Registros" :Diccionarios,"Posiciones":Posiciones}

    def Lineas(self) -> int:
        Contenido=[]
        with open(self.RUTA,"r") as Archivo: 
            Contenido= Archivo.read()
            Contenido= Contenido.split("\n")
        return len(Contenido)
                