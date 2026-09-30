from vehiculo import Vehiculo


class Auto(Vehiculo):
    def __init__(self, patente, marca, modelo, tarifa_base_por_dia):
        super().__init__("Auto", patente, marca, modelo, tarifa_base_por_dia)
