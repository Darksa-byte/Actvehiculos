"""Clase abstracta base para los vehículos."""

from abc import ABC, abstractmethod


class Vehiculo(ABC):
    """Define el comportamiento común de cualquier vehículo alquilable."""

    ESTADOS_VALIDOS = {"disponible", "alquilado", "en mantenimiento"}

    def __init__(
        self,
        tipo_vehiculo: str,
        patente: str,
        marca: str,
        modelo: str,
        tarifa_base_por_dia: float,
        estado: str = "disponible",
    ) -> None:
        self.tipo_vehiculo = tipo_vehiculo
        self.patente = patente
        self.marca = marca
        self.modelo = modelo
        self.tarifa_base_por_dia = tarifa_base_por_dia
        self.estado = estado

    def _validar_texto(self, valor: str, campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{campo} debe ser un texto no vacío.")
        return valor.strip()

    @property
    def tipo_vehiculo(self) -> str:
        return self._tipo_vehiculo

    @tipo_vehiculo.setter
    def tipo_vehiculo(self, valor: str) -> None:
        self._tipo_vehiculo = self._validar_texto(valor, "El tipo de vehículo")

    @property
    def patente(self) -> str:
        return self._patente

    @patente.setter
    def patente(self, valor: str) -> None:
        valor = self._validar_texto(valor, "La patente")
        if len(valor) < 3:
            raise ValueError("La patente debe tener al menos 3 caracteres.")
        self._patente = valor.upper()

    @property
    def marca(self) -> str:
        return self._marca

    @marca.setter
    def marca(self, valor: str) -> None:
        self._marca = self._validar_texto(valor, "La marca")

    @property
    def modelo(self) -> str:
        return self._modelo

    @modelo.setter
    def modelo(self, valor: str) -> None:
        self._modelo = self._validar_texto(valor, "El modelo")

    @property
    def tarifa_base_por_dia(self) -> float:
        return self._tarifa_base_por_dia

    @tarifa_base_por_dia.setter
    def tarifa_base_por_dia(self, valor: float) -> None:
        try:
            tarifa = float(valor)
        except (TypeError, ValueError) as error:
            raise ValueError("La tarifa base debe ser numérica.") from error
        if tarifa <= 0:
            raise ValueError("La tarifa base por día debe ser mayor que cero.")
        self._tarifa_base_por_dia = tarifa

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, valor: str) -> None:
        if valor not in self.ESTADOS_VALIDOS:
            permitidos = ", ".join(sorted(self.ESTADOS_VALIDOS))
            raise ValueError(f"Estado inválido. Valores permitidos: {permitidos}.")
        self._estado = valor

    @abstractmethod
    def calcular_costo(self, dias: int) -> float:
        """Calcula el costo para una cantidad positiva de días."""

    def __str__(self) -> str:
        return (
            f"{self.tipo_vehiculo} | Patente: {self.patente} | "
            f"{self.marca} {self.modelo} | ${self.tarifa_base_por_dia:.2f}/día | "
            f"Estado: {self.estado}"
        )
