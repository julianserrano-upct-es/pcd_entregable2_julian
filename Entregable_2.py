class Sistema():
    _unicaInstancia = None

    def __init__(self):
        self.manejador = ManejadorCalculos()

    @classmethod
    def obtemerInstance(cls):
        if not cls._unicaInstancia:
            cls._unicaInstancia = Sistema()
        return cls._unicaInstancia
    
    def actualizar(datos):
        pass

class ManejadorCalculos():
    def __init__(self):
        self.calculos = []

    def calculo_estadistico(self, datos):
        pass

class ManejadorUmbral(ManejadorCalculos):
    def __init__(self, umbral):
        self._umbral = umbral

    def calculo_estadistico(self, datos):
        pass