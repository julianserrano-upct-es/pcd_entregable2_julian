import random
import time
from functools import reduce

class Sistema():
    _unicaInstancia = None

    def __init__(self):
        pass

    @classmethod
    def obtemerInstance(cls):
        if not cls._unicaInstancia:
            cls._unicaInstancia = Sistema()
        return cls._unicaInstancia
    
    def actualizar(self, datos):
        #Simulacion de nuevo dato
        temperatura = random.randint(0, 50)
        hora = time.strftime("%H:%M:%S")
        dato = (hora, temperatura)

        #Calculo las estadisticas con el nuevo dato
        manejador_umbral = ManejadorUmbral(30)
        manejador_ultimos30 = ManejadorUltimos30(manejador_umbral)
        manejador_estrategia = Estrategias(manejador_ultimos30)




class ManejadorCalculos():
    def __init__(self):
        pass

    def calculo_estadistico(self, dato):
        pass

class ManejadorUmbral(ManejadorCalculos):
    def __init__(self, umbral, manejador=None):
        self.manejador = manejador
        self._umbral = umbral

    def calculo_estadistico(self, dato):
        if dato[1] > self._umbral:
            print("Se ha superado el umbral")
        else:
            print("No se ha superado el umbral")
        
        if self.manejador is not None:
            self.manejador.calculo_estadistico(dato)

class ManejadorUltimos30(ManejadorCalculos):
    def __init__(self, manejador=None):
        self.manejador = manejador
        self._datos_pasados = []

    def calculo_estadistico(self, dato):
        suma_anterior = reduce(lambda x, y: x + y, self._datos_pasados)

        if len(self._datos_pasados) < 12:
            self._datos_pasados.append(dato)
        else:
            self._datos_pasados.pop(0)
            self._datos_pasados.append(dato)

        suma_actual = reduce(lambda x, y: x + y, self._datos_pasados)
        if suma_actual + 10 > suma_anterior:
            print("Se ha incrementado la temperatura en 10 grados durante los ultimos 30 segundos")
        else:
            print("No se ha incrementado la temperatura en 10 grados durante los ultimos 30 segundos")
        
        if self.manejador is not None:
            self.manejador.calculo_estadistico(dato)

class Estrategias(ManejadorCalculos):
    def __init__(self, manejador=None, estrategia=None):
        self.manejador = manejador
        self._estrategia = estrategia

    def calculo_estadistico(self, dato):
        

        if self.manejador is not None:
            self.manejador.calculo_estadistico(dato)

class EstrategiaMedia(Estrategias):
    def __init__(self):
        pass

    def calculo_estadistico(self, dato):
        pass

class EstrategiaDesviacion(Estrategias):
    def __init__(self):
        pass

    def calculo_estadistico(self, dato):
        pass

class EstrategiaCuartiles(Estrategias):
    def __init__(self):
        pass

    def calculo_estadistico(self, dato):
        pass

class Contexto():
    def __init__(self, estrategia: Estrategias):
        self._estrategia = estrategia

    def operar(self):
        result = self._estrategia.calculo_estadistico([])
        return result
    

if __name__ == "__main__":
    sistema = Sistema.obtemerInstance()


    context = Contexto(EstrategiaCuartiles())
    print("Client: Strategy is set to normal sorting.")
    print(context.operar())
