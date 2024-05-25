import random
import time
from functools import reduce
import math

class Sistema():
    """
    Clase que representa el sistema de control de temperatura. Se encarga de gestionar los datos y las estrategias.
    He utilizado el patron de diseño Singleton para asegurarme de que solo se pueda crear una instancia de la clase.
    Ademas la funcion actualizar cuando se aplique Apache Kafka se encargara de recibir los datos y calcular las estadisticas haciendo asi un uso del patron de diseño Observer.

    Atributos:
    _unicaInstancia: Atributo de clase que guarda la unica instancia de la clase
    manejador_umbral: Atributo de clase que guarda el manejador de umbral
    manejador_ultimos30: Atributo de clase que guarda el manejador de los ultimos 30 segundos para ver si ha subido la temperatura
    manejador_estrategia: Atributo de clase que guarda el manejador de las estrategias para calcular las estadisticas

    Metodos:
    __init__: Constructor de la clase
    obtemerInstance: Metodo de clase que devuelve la unica instancia de la clase
    actualizar: Metodo que simula la llegada de un nuevo dato y calcula las estadisticas
    """
    _unicaInstancia = None

    def __init__(self, umbral, estrategia=None):
        manejador_umbral = ManejadorUmbral(umbral)
        self.manejador_ultimos30 = ManejadorUltimos30(manejador_umbral)
        self.manejador_estrategia = Estrategias(self.manejador_ultimos30, estrategia)

    @classmethod
    def obtemerInstance(cls, umbral, estrategia=None):
        if not cls._unicaInstancia:
            cls._unicaInstancia = Sistema(umbral, estrategia)
        return cls._unicaInstancia
    
    def actualizar(self, datos=1):
        #Simulacion de nuevo dato
        temperatura = random.randint(0, 50)
        hora = time.strftime("%H:%M:%S")
        dato = (hora, temperatura)
        print("Nuevo dato: ", dato)

        #Calculo las estadisticas con el nuevo dato
        self.manejador_estrategia.calculo_estadistico(dato[1])

class ManejadorCalculos():
    """
    Esta clase es la clase abstracta que define el comportamiento de los manejadores de calculos.
    Se encarga de definir el metodo que se encargara de calcular las estadisticas. Es un uso del patron de disesño Chain of Responsability.
    """

    def __init__(self):
        pass

    def calculo_estadistico(self):
        pass

class ManejadorUmbral(ManejadorCalculos):
    """
    La clase ManejadorUmbral es una clase que hereda de ManejadorCalculos y se encarga de comprobar si se ha superado un umbral establecido. 
    Es uno de los manejadores de calculos en la cadena del Chain of Resposability.

    Atributos:
    manejador: Atributo que guarda el siguiente manejador en la cadena
    umbral: Atributo que guarda el umbral establecido

    Metodos:
    __init__: Constructor de la clase
    calculo_estadistico: Metodo que se encarga de comprobar si se ha superado el umbral y llama al siguiente manejador en la cadena
    """

    def __init__(self, umbral, manejador=None):
        self.manejador = manejador
        self._umbral = umbral

    def calculo_estadistico(self, dato):
        if dato > self._umbral:
            print("Se ha superado el umbral")
        else:
            print("No se ha superado el umbral")
        
        if self.manejador is not None:
            self.manejador.calculo_estadistico(dato)

class ManejadorUltimos30(ManejadorCalculos):
    """
    La clase ManejadorUltimos30 es una clase que hereda de ManejadorCalculos y se encarga de comprobar si se ha incrementado la temperatura en 10 grados durante los ultimos 30 segundos.
    Es uno de los manejadores de calculos en la cadena del Chain of Resposability.

    Atributos:
    manejador: Atributo que guarda el siguiente manejador en la cadena
    _datos_pasados: Atributo que guarda los datos de los ultimos 30 segundos

    Metodos:
    __init__: Constructor de la clase
    calculo_estadistico: Metodo que se encarga de comprobar si se ha incrementado la temperatura en 10 grados durante los ultimos 30 segundos y llama al siguiente manejador en la cadena
    """
    def __init__(self, manejador=None):
        self.manejador = manejador
        self._datos_pasados = []

    def calculo_estadistico(self, dato):
        if len(self._datos_pasados) < 6:
            self._datos_pasados.append(dato)
            print("No se han completado los 30 segundos")
        else:
            suma_anterior = reduce(lambda x, y: x + y, self._datos_pasados)

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
    """
    La clase Estrategias es una clase que hereda de ManejadorCalculos y se encarga de calcular las estadisticas de los datos.
    Es uno de los manejadores de calculos en la cadena del Chain of Resposability. Ademas se encarga de gestionar las estrategias de calculo de las estadisticas.
    Como hay varias estrategias, se ha utilizado el patron de diseño Strategy para poder cambiar la estrategia de calculo de las estadisticas.
    En caso de no especificar una estrategia, se utilizan las tres.

    Atributos:
    manejador: Atributo que guarda el siguiente manejador en la cadena
    _estrategia: Atributo que guarda la estrategia de calculo de las estadisticas
    _datos_pasados: Atributo que guarda los datos pasados

    Metodos:
    __init__: Constructor de la clase
    calculo_estadistico: Metodo que se encarga de calcular las estadisticas de los datos y llama al siguiente manejador en la cadena
    """
    def __init__(self, manejador=None, estrategia=None, datos=[]):
        self._datos_pasados = datos
        self.manejador = manejador
        self._estrategia = estrategia

    def calculo_estadistico(self, dato):
        #Si no se ha definido una estrategia, se utilizan las tres
        if len(self._datos_pasados) < 12:
            self._datos_pasados.append(dato)
            print("No se han completado los 60 segundos")
        else:
            self._datos_pasados.pop(0)
            self._datos_pasados.append(dato)

            self._media = EstrategiaMedia(self._datos_pasados)
            self._desviacion = EstrategiaDesviacion(self._datos_pasados)
            self._cuartiles = EstrategiaCuartiles(self._datos_pasados)

            if self._estrategia is None:
                self._media.calculo_estadistico()
                self._desviacion.calculo_estadistico()
                self._cuartiles.calculo_estadistico()
            else:
                self._estrategia.calculo_estadistico()


        if self.manejador is not None:
            self.manejador.calculo_estadistico(dato)

class EstrategiaMedia(Estrategias):
    """
    Es una de las estrategias de calculo de las estadisticas. Se encarga de calcular la media de los datos de los ultimos 60 segundos.

    Atributos:
    _datos_pasados: Atributo que guarda los datos pasados. En realidad al haber cambiado ya los datos a la hora de instanciar la clase, 
    se guardan los datos de los ultimos 60 segundos pero el nombre preferia no cambiarlo por simplicidad.

    Metodos:
    __init__: Constructor de la clase
    calculo_estadistico: Metodo que se encarga de calcular la media de los datos pasados
    """
    def __init__(self, datos_pasados):
        super().__init__(datos = datos_pasados)

    def calculo_estadistico(self):
        media = reduce(lambda x, y: x + y, self._datos_pasados) / len(self._datos_pasados)
        print("La media de las temperaturas es: ", media)

class EstrategiaDesviacion(Estrategias):
    """
    Es una de las estrategias de calculo de las estadisticas. Se encarga de calcular la desviacion tipica de los datos de los ultimos 60 segundos.

    Atributos:
    _datos_pasados: Atributo que guarda los datos pasados. En realidad al haber cambiado ya los datos a la hora de instanciar la clase,
    se guardan los datos de los ultimos 60 segundos pero el nombre preferia no cambiarlo por simplicidad.

    Metodos:
    __init__: Constructor de la clase
    calculo_estadistico: Metodo que se encarga de calcular la desviacion tipica de los datos pasados
    """
    def __init__(self, datos_pasados):
        super().__init__(datos = datos_pasados)

    def calculo_estadistico(self):
        media = reduce(lambda x, y: x + y, self._datos_pasados) / len(self._datos_pasados)
        desviacion_tipica = math.sqrt(reduce(lambda x, y: x + y, map(lambda x: (x - media) ** 2, self._datos_pasados)) / len(self._datos_pasados))
        print("La desviacion tipica de las temperaturas es: ", desviacion_tipica)

class EstrategiaCuartiles(Estrategias):
    """
    Es una de las estrategias de calculo de las estadisticas. Se encarga de calcular el primer y tercer cuartil de los datos de los ultimos 60 segundos.

    Atributos:
    _datos_pasados: Atributo que guarda los datos pasados. En realidad al haber cambiado ya los datos a la hora de instanciar la clase,
    se guardan los datos de los ultimos 60 segundos pero el nombre preferia no cambiarlo por simplicidad.

    Metodos:
    __init__: Constructor de la clase
    calculo_estadistico: Metodo que se encarga de calcular el primer y tercer cuartil de los datos pasados.
    """
    def __init__(self, datos_pasados):
        super().__init__(datos = datos_pasados)

    def calculo_estadistico(self):
        datos_ordenados = sorted(self._datos_pasados)

        #Primer cuartil
        pos = (len(datos_ordenados) - 1) * 0.25
        suelo = math.floor(pos)
        techo = math.ceil(pos)
        if suelo == techo:
            q1 = datos_ordenados[int(pos)]
        else:
            q1 = datos_ordenados[int(suelo)] * (techo - pos) + datos_ordenados[int(techo)] * (pos - suelo)

        #Tercer cuartil
        pos = (len(datos_ordenados) - 1) * 0.75
        suelo = math.floor(pos)
        techo = math.ceil(pos)
        if suelo == techo:
            q3 = datos_ordenados[int(pos)]
        else:
            q3 = datos_ordenados[int(suelo)] * (techo - pos) + datos_ordenados[int(techo)] * (pos - suelo)

        print("El primer cuartil es: ", q1)
        print("El tercer cuartil es: ", q3)
    
if __name__ == "__main__":
    sistema = Sistema.obtemerInstance(30)
    sistema.actualizar()
    sistema.actualizar()
    sistema.actualizar()
    sistema.actualizar()
    sistema.actualizar()
    sistema.actualizar()
    sistema.actualizar()
    sistema.actualizar()
    sistema.actualizar()
    sistema.actualizar()
    sistema.actualizar()
    sistema.actualizar()
    sistema.actualizar()
    sistema.actualizar()
    sistema.actualizar()