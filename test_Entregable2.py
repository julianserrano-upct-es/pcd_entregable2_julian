import pytest
from Entregable_2 import *
from math import sqrt


# Test de la clase Sistema y sus métodos
# El fixture significa que se ejecutará antes de cada test que lo requiera
@pytest.fixture
def sistema():
    return Sistema.obtemerInstance(30)

def test_singleton_instance(sistema):
    # Verificando que se obtenga la misma instancia para ver que funciona el patron Singleton
    sistema2 = Sistema.obtemerInstance(30)
    assert sistema is sistema2

def test_actualizar_datos(sistema):
    # Verificando que se actualicen los datos del sistema
    sistema.actualizar()
    assert len(sistema.manejador_ultimos30._datos_pasados) > 0

def test_estrategia_media():
    # Verificando que la estrategia de la media funcione correctamente
    datos = [1, 2, 3, 4, 5]
    estrategia = EstrategiaMedia(datos)
    assert estrategia.calculo_estadistico() == 3

def test_estrategia_desviacion_tipica():
    # Verificando que la estrategia de la desviación típica funcione correctamente
    datos = [1, 2, 3, 4, 5]
    estrategia = EstrategiaDesviacion(datos)
    assert pytest.approx(estrategia.calculo_estadistico(), 0.01) == sqrt(2)

def test_estrategia_cuartiles():
    # Verificando que la estrategia de los cuartiles funcione correctamente
    datos = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    estrategia = EstrategiaCuartiles(datos)
    q1, q3 = estrategia.calculo_estadistico()
    assert q1 == 3
    assert q3 == 7

def test_manejador_umbral():
    # Verificando que el manejador de umbral funcione correctamente con datos menores y mayores al umbral
    manejador = ManejadorUmbral(30)
    datos = [25, 35]
    valores = []
    for dato in datos:
        valores.append(manejador.calculo_estadistico(dato))
    assert valores[0] == False
    assert valores[1] == True


def test_manejador_ultimos30():
    # Verificando que el manejador de los últimos 30 segundos de datos funcione correctamente 
    manejador = ManejadorUltimos30(None)
    manejador._datos_pasados = [25, 30, 35]
    nuevo_dato = 40
    manejador.calculo_estadistico(nuevo_dato)
    assert len(manejador._datos_pasados) == 4
    assert manejador._datos_pasados[-1] == nuevo_dato
    assert manejador._datos_pasados[0] == 25 # Verificando que el dato más viejo se mantenga

    manejador._datos_pasados = [25, 30, 35, 40, 45, 50]
    nuevo_dato = (55)
    manejador.calculo_estadistico(nuevo_dato)
    assert len(manejador._datos_pasados) == 6
    assert manejador._datos_pasados[-1] == nuevo_dato
    assert manejador._datos_pasados[0] == 30  # Verificando que el dato más viejo se elimine