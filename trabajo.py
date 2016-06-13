#Trabajo de AIA por Gabriel Amador García
import random
import math
import itertools
import json
import pdb

class MOK:
    '''Modelo oculto de markov'''
    #Metodo útil: dado un diccionario con la estructura (dato1, dato2):probabilidad
    #con entrada e1, filtra e1==dato1, y devuelve un dato2 de forma aleatoria con la probabilidad indicada en el dict
    def azar_basico(self,diccionario):
        azar=random.uniform(0, 1)
        res=None
        for a in diccionario:
            res=a
            azar=azar-diccionario[a]
            if azar<=0:
                return a
        return res
    def distribucion_aleatoria(self,dato,diccionario):
        posibilidades=dict()
        for (dato1,dato2) in diccionario:
            if(dato1==dato):
                posibilidades[dato2]=diccionario[dato1,dato2]
        #Rellenamos un diccionario con los posibles resultados y su respectivo valor.
        #Seleccionamos al azar teniendo en cuenta la posibilidad. Vamos a coger un numero entre 0 y 1 y vamos a ir restando
        #la posibilidad de la opcion actual. Si es <=0 entonces devolvemos el valor actual
        return self.azar_basico(posibilidades)



    def __init__(self,estados,cambios_estados,posibilidades_iniciales,posibilidad_observaciones):
        self.estados=estados#Lista con los posibles estados.
        self.matriz_cambios_estados=cambios_estados#diccionario. Estilo: (estado1,estado2):posibildad
        self.posibilidades_inicio=posibilidades_iniciales#Vector
        self.matriz_posibilidad_observaciones=posibilidad_observaciones#diccionario. Estilo: (estado1,observacion):posibildad

        for a in estados:
            for b in estados:
                if ((a,b) not in self.matriz_cambios_estados):
                    #Si no existen todas las posibilidades: Alertar, setear a 0
                    print ("Matriz cambio estados incompleta. Poniendo a 0: "+str(a)+", "+str(b))
            for (estado,observacion) in self.matriz_posibilidad_observaciones :
                if((a,observacion) not in self.matriz_posibilidad_observaciones):
                    print ("observacion imposible. Poniendo a 0: "+str(a)+": "+str(observacion))
            if (a not in self.posibilidades_inicio):
                print ("Posibilidad de inicio nula. Poniendo a 0: "+str(a))



    def muestreo(self,n):
        if n<1:
            print ("ERROR: muestreo recibe numero negativo")
            return -1
        res=list()
        #Primer elemento
        estado=self.azar_basico(self.posibilidades_inicio)
        visible=self.distribucion_aleatoria(estado,self.matriz_posibilidad_observaciones)
        res.append((estado,visible))
        n=n-1
        while n>0:
            n=n-1
            estado=self.distribucion_aleatoria(res[len(res)-1][0],self.matriz_cambios_estados)
            visible=self.distribucion_aleatoria(estado,self.matriz_posibilidad_observaciones)
            res.append((estado,visible))
        return res


    def avance(self,observaciones):
        res=list()#Usamos una lista de diccionarios
        #Para saber del estado s3 en la observacion 4 hacemos res[4][s3]
        alfas=dict()
        for s in self.estados:
            alfas[s]=self.posibilidades_inicio[s]*self.matriz_posibilidad_observaciones[(s,observaciones[0])]#Tema 4
        res.append(alfas)
        for i in range(1,len(observaciones)):
            alfas=dict()#reutilizamos variables, se ha testeado y no hay problema en python3
            for s in self.estados:
                alfas[s]=0
                acum=0
                for s2 in self.estados:
                    #print(s+s2)
                    #print (self.matriz_cambios_estados[(s2,s)])
                    #print(res[i-1][s2])
                    acum=acum+self.matriz_cambios_estados[(s2,s)]*res[i-1][s2]
                #print (acum)
                alfas[s]=self.matriz_posibilidad_observaciones[(s,observaciones[i])]*acum
            res.append(alfas)
        res2=list()
        #for x in reverse(res):

        return res


    def viterbi(self,observaciones):
        construccion=list()
        vk=dict()
        prk=dict()
        for s in self.estados:
            vk[s]=self.posibilidades_inicio[s]*self.matriz_posibilidad_observaciones[(s,observaciones[0])]
            prk[s]=None

            #Tema 4
        construccion.append((vk,prk))
        for i in range(1,len(observaciones)):
            vk=dict()
            prk=dict()
            for s in self.estados:
                prkMax=dict()
                acum=list()
                for s2 in self.estados:
                    acum.append(self.matriz_cambios_estados[(s2,s)]*construccion[i-1][0][s2])
                    prkMax[s2]=self.matriz_cambios_estados[(s2,s)]*construccion[i-1][0][s2]
                prk[s]=max(prkMax, key=prkMax.get)
                #print(prk)
                vk[s]=self.matriz_posibilidad_observaciones[(s,observaciones[i])]*max(acum)
            construccion.append((vk,prk))

        #Reconstrucción:
        #Seleccionamos la mayor probabilidad en s4:
        ProbabilidadFinal=construccion[len(construccion)-1][0]
        res=list()
        res.append(max(ProbabilidadFinal, key=ProbabilidadFinal.get))
        for i in range(len(construccion)-1,0,-1):
            res.append(construccion[i][1][res[len(res)-1]])
        return res




# estados=['Moneda autentica','Dos caras']#Problema de testeo rápido
# cambios={('Moneda autentica','Dos caras'):0.2,
#     ('Moneda autentica','Moneda autentica'):0.8,
#     ('Dos caras','Moneda autentica'):0.8,
#     ('Dos caras','Dos caras'):0.2}
# inicial={'Moneda autentica':0.5,'Dos caras':0.5}
# posibilidad_observaciones={
#     ('Moneda autentica','cara'):0.5,
#     ('Moneda autentica','cruz'):0.5,
#     ('Dos caras','cara'):1,
#     ('Dos caras','cruz'):0}

estados=['c','f']
cambios={('c','f'):0.3,
    ('c','c'):0.7,
    ('f','c'):0.4,
    ('f','f'):0.6
    }
inicial={'c':0.8,'f':0.2}
posibilidad_observaciones={
    ('c','1'):0.2,
    ('c','2'):0.4,
    ('c','3'):0.4,
    ('f','1'):0.5,
    ('f','2'):0.4,
    ('f','3'):0.1,
}

observaciones_ejemplo=['3','1','3','2']

#modeloOculto=MOK(estados,cambios,inicial,posibilidad_observaciones)
#print(modeloOculto.viterbi(observaciones_ejemplo))



#Parte 2: ROBOT


cuadricula_0=[
    [0,0,1,0],
    [1,0,1,0],
    [0,0,0,0]
]

cuadricula_ejemplo=[
    [0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0],#En caso de empezar en (15,0) el programa daría NONE
    [1,1,0,0,1,0,1,1,0,1,0,1,0,1,1,1],
    [1,0,0,0,1,0,1,1,0,0,0,0,0,1,1,0],
    [0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0]
]

def genera_cuadricula(x,y,obstaculos):
    pos_obstaculos=set()
    while len(pos_obstaculos)<obstaculos:
        pos_x = random.randint(0,x-1)
        pos_y = random.randint(0,y-1)
        pos_obstaculos.add((pos_x,pos_y))
    print(pos_obstaculos)
    res=list()
    for fila in range(y):
        res.append([0]*x)
    for obstaculo in pos_obstaculos:
        res[obstaculo[0]][obstaculo[1]]=1
    return res




def mok_robot_cuadricula(cuadricula,epsilon_error):
    #estados,cambios_estados,posibilidades_iniciales,posibilidad_observaciones
    estados=list()
    todas_observaciones=list()
    todas_observaciones.append({})
    for i in range(1,5):
        combs=itertools.combinations({'N','S','E','O'},i)
        for a in combs:
            todas_observaciones.append(set(a))
    for j in range(len(cuadricula)):
        for i in range(len(cuadricula[j])):
            if(cuadricula[j][i] == 0):
                estados.append((i,j))
    posibilidades_iniciales=dict()
    cambios_estados=dict()
    posibilidad_observaciones=dict()
    #Las observaciones serán varios posibles conjuntos, con todas las posibilidades de obstaculos (4! como mucho)
    for e in estados:
        posibilidades_iniciales[e]=1.0/len(estados)
        #Por simplificar, inicializaremos todas las posibilidades a 0
        for j in estados:#no soy muy imaginativo con los nombres de las variables
            cambios_estados[(e,j)]=0.0
        obstaculos=set({'N','S','E','O'})
        for obs in todas_observaciones:
            posibilidad_observaciones[(e,frozenset(obs))]=epsilon_error/15#16 posibilidades en total

        if((e[0],e[1]-1) in estados):#Podemos ir al norte
            obstaculos.remove('N')
        if((e[0],e[1]+1) in estados):#Podemos ir al sur
            obstaculos.remove('S')
        if((e[0]+1,e[1]) in estados):#Podemos ir al este
            obstaculos.remove('E')
        if((e[0]-1,e[1]) in estados):#Podemos ir al oeste
            obstaculos.remove('O')
        if(len(obstaculos)!=4):
            posibilidad_movimiento=1.0/(4-len(obstaculos))
        else:
            posibilidad_movimiento=0.0

        if((e[0],e[1]-1) in estados):#Podemos ir al norte
            cambios_estados[(e,(e[0],e[1]-1))]=posibilidad_movimiento
        if((e[0],e[1]+1) in estados):#Podemos ir al sur
            cambios_estados[(e,(e[0],e[1]+1))]=posibilidad_movimiento
        if((e[0]+1,e[1]) in estados):#Podemos ir al este
            cambios_estados[(e,(e[0]+1,e[1]))]=posibilidad_movimiento
        if((e[0]-1,e[1]) in estados):#Podemos ir al oeste
            cambios_estados[(e,(e[0]-1,e[1]))]=posibilidad_movimiento

        #En caso de que los sensores fallen, POSIBILIDAD AL AZAR!
        posibilidad_observaciones[(e,frozenset(obstaculos))]=1-epsilon_error
    #print(cambios_estados)
    return(MOK(estados,cambios_estados,posibilidades_iniciales,posibilidad_observaciones))

prueba_robot=mok_robot_cuadricula(cuadricula_ejemplo,0.001)



observaciones_robot=[frozenset({'S'}), frozenset({'N'}), frozenset({'O'}), frozenset({'S'}), frozenset({'S'})]

print("Estado final más probable")
pos=prueba_robot.avance(observaciones_robot)
pos=pos[len(pos)-1]
print(max(pos, key=pos.get))
print("Posibilidad del estado final:")
print(pos[max(pos, key=pos.get)])
print("Secuencia más probable")
print(prueba_robot.viterbi(observaciones_robot))



#Parte 3:
#Utilidades:
def distancia_manhattan(x,y):
    return abs(x[0]-y[0])+abs(x[1]-y[1])

def rendimiento_virterbi(autentico,descifrado):
    acum=0
    for i in range(len(descifrado)):
        if(autentico[i]==descifrado[i]):
            acum=acum+1
    return acum
#Parámetros que vamos a probar:

#Test del robot según la distancia y el error epsilon:

numeroRepeticiones=10
rangoError=10
distancia_recorrido=40
diccionarioAvance=dict()#Usaremos estos diccionarios para guardar datos
diccionarioViterbi=dict()#de como de buenas son las aprox. generadas
#Solo calcularemos la media

for error in range(0,rangoError):#Error máximo 0.5
    epsilon=0.01*error
    print("##############EPSILON: "+str(epsilon)+" ####################")
    mok_error=mok_robot_cuadricula(cuadricula_ejemplo,epsilon)
    for distancia in range(1,distancia_recorrido+1):
        media_viterbi=0
        media_avance=0
        for repeticiones in range(1,numeroRepeticiones+1):
            hechosYObservaciones=mok_error.muestreo(distancia)#En cada iteracion generamos un camino nuevo
            observaciones=list()
            hechos=list()#Juraria que hay otra variable llamada estados por ahi

            for (a,b) in hechosYObservaciones:
                hechos.append(a)
                observaciones.append(b)
            viterbi=mok_error.viterbi(observaciones)
            media_viterbi+=rendimiento_virterbi(hechos,viterbi)
            avan=mok_error.avance(observaciones)
            finAvance=max(avan[len(avan)-1], key=avan[len(avan)-1].get)
            media_avance+=distancia_manhattan(finAvance,hechos[len(hechos)-1])
        media_viterbi=media_viterbi*1.0/numeroRepeticiones
        media_avance=media_avance*1.0/numeroRepeticiones
        diccionarioViterbi[(distancia,epsilon)]=media_viterbi
        diccionarioAvance[(distancia,epsilon)]=media_avance
        print("###DISTANCIA RECORRIDA: "+str(distancia))
        #print(diccionarioViterbi)
print("###################RESULTADO FINAL#####################")
print("EXACTITUD VITERBI VARIANDO LA DISTANCIA RECORRIDA Y EL ERROR EPSILON. Más mejor")
print(diccionarioViterbi)
print("EXACTITUD AVANCE VARIANDO LA DISTANCIA RECORRIDA Y EL ERROR EPSILON. Menos es mejor")
print(diccionarioAvance)

archivo=open('salida_avance.json','w')
json_data = json.dump(diccionarioAvance,archivo, sort_keys=True, indent=4)
archivo.close()
archivo=open('salida_viterbi.json','w')
json_data = json.dump(diccionarioViterbi,archivo, sort_keys=True, indent=4)
archivo.close()
print("Se ha generado un archivo json con el nombre salida_avance.json y salida_viterbi.json")
