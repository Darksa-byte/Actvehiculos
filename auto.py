"""Implementación del vehículo tipo auto."""

from vehiculo import Vehiculo


class Auto(Vehiculo):
    """Vehículo con tarifa base sin recargo."""

    def __init__(self, patente: str, marca: str, modelo: str, tarifa_base_por_dia: float) -> None:
        super().__init__("Auto", patente, marca, modelo, tarifa_base_por_dia)

    def calcular_costo(self, dias: int) -> float:
        if not isinstance(dias, int) or dias <= 0:
            raise ValueError("La cantidad de días debe ser un entero mayor que cero.")
        return self.tarifa_base_por_dia * dias
