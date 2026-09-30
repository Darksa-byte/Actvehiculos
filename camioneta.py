from vehiculo import Vehiculo


class Camioneta(Vehiculo):
    def __init__(self, patente, marca, modelo, tarifa_base_por_dia):
        super().__init__("Camioneta", patente, marca, modelo, tarifa_base_por_dia)

    def calcular_costo(self, dias):
        return super().calcular_costo(dias) * 1.20
