#Trabajo de AIA por Gabriel Amador García
import random
import math


class MOK:
    '''Modelo oculto de markov'''
    #Metodo útil: dado un diccionario con la estructura (dato1, dato2):probabilidad
    #con entrada e1, filtra e1==dato1, y devuelve un dato2 de forma aleatoria con la probabilidad indicada en el dict
    def distribucion_aleatoria(self,dato,diccionario):
        posibilidades=dict()
        for (dato1,dato2) in diccionario:
            if(dato1==dato):
                posibilidades[dato2]=diccionario[dato1,dato2]
        #Rellenamos un diccionario con los posibles resultados y su respectivo valor.
        #Seleccionamos al azar teniendo en cuenta la posibilidad. Vamos a coger un numero entre 0 y 1 y vamos a ir restando
        #la posibilidad de la opcion actual. Si es <=0 entonces devolvemos el valor actual
        azar=random.uniform(0, 1)
        for a in posibilidades:
            azar=azar-posibilidades[a]
            if azar<=0:
                return a



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


estados=['Moneda autentica','Dos caras']#Problema de testeo rápido
cambios={('Moneda autentica','Dos caras'):0.2,
    ('Moneda autentica','Moneda autentica'):0.8,
    ('Dos caras','Moneda autentica'):0.8,
    ('Dos caras','Dos caras'):0.2}
inicial={'Moneda autentica':0.5,'Dos caras':0.5}
posibilidad_observaciones={
    ('Moneda autentica','cara'):0.5,
    ('Moneda autentica','cruz'):0.5,
    ('Dos caras','cara'):1,
    ('Dos caras','cruz'):0}



modeloOculto=MOK(estados,cambios,inicial,posibilidad_observaciones)
print(modeloOculto.distribucion_aleatoria('Dos caras',cambios))
