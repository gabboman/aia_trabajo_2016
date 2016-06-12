#Trabajo de AIA por Gabriel Amador García
import random
import math


class MOK:
    '''Modelo oculto de markov'''
    #Metodo útil: dado un diccionario con la estructura (dato1, dato2):probabilidad
    #con entrada e1, filtra e1==dato1, y devuelve un dato2 de forma aleatoria con la probabilidad indicada en el dict
    def azar_basico(self,diccionario):
        azar=random.uniform(0, 1)
        for a in diccionario:
            azar=azar-diccionario[a]
            if azar<=0:
                return a
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
        res=list()#Usamos una lista de diccionarios
        #Para saber del estado s3 en la observacion 4 hacemos res[4][s3]
        maximos=dict()
        for s in self.estados:
            maximos[s]=self.posibilidades_inicio[s]*self.matriz_posibilidad_observaciones[(s,observaciones[0])]#Tema 4
        res.append(maximos)
        for i in range(1,len(observaciones)):
            maximos=dict()#reutilizamos variables, se ha testeado y no hay problema en python3
            for s in self.estados:
                maximos[s]=0
                acum=list()
                for s2 in self.estados:
                    #print(s+s2)
                    #print (self.matriz_cambios_estados[(s2,s)])
                    #print(res[i-1][s2])
                    acum.append(self.matriz_cambios_estados[(s2,s)]*res[i-1][s2])
                #print (acum)
                maximos[s]=self.matriz_posibilidad_observaciones[(s,observaciones[i])]*max(acum)
            res.append(maximos)
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

modeloOculto=MOK(estados,cambios,inicial,posibilidad_observaciones)
print(modeloOculto.viterbi(observaciones_ejemplo))
