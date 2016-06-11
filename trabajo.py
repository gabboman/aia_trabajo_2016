#Trabajo de AIA por Gabriel Amador García

class MOK:
    '''Modelo oculto de markov'''


    def __init__(self,estados,estados_visibles,cambios_estados,posibilidades_iniciales,posibilidad_observaciones):
        self.estados=estados#Lista con los posibles estados.
        self.matriz_cambios_estados=cambios_estados#diccionario. Estilo: (estado1,estado2):posibildad
        self.posibilidades_inicio=posibilidades_iniciales#Vector
        self.matriz_posibilidad_observaciones=posibilidad_observaciones#diccionario. Estilo: (estado1,observacion):posibildad

        for a in estados:
            for b in estados:
                if ((a,b) not in matriz_cambios_estados):
                    #Si no existen todas las posibilidades: Alertar, setear a 0
                    print ("Matriz cambio estados incompleta. Poniendo a 0: "+a+", "+b)
            for observacion in matriz_posibilidad_observaciones.values() :
                if((a,observacion) not in matriz_posibilidad_observaciones):
                    print ("observacion imposible. Poniendo a 0: "+a+": "+observacion)
            if (a not in posibilidades_inicio):
                print ("Posibilidad de inicio nula. Poniendo a 0: "+a)


estados=['Moneda autentica','Dos caras']#Problema de testeo rápido
cambios={('Moneda autentica','Dos caras'):0.2,
    ('Moneda autentica','Moneda autentica'):0.8,
    ('Dos caras','Moneda autentica'):0.8,
    ('Dos caras','Dos caras'):0.2}
visible=['cara','cruz']
inicial={'Moneda autentica':0.5,'Dos caras':0.5}
posibilidad_observaciones={
    ('Moneda autentica','cara'):0.5,
    ('Moneda autentica','cruz'):0.5,
    ('dos caras','cara'):1,
    ('dos caras','cruz'):0}



#modeloOculto=MOK(estados)
#print (modeloOculto.matriz_cambios_estados)
