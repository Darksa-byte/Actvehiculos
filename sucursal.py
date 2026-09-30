"""Modelo de sucursales y su inventario de vehículos."""

from registrohistorial import RegistroHistorial
from vehiculo import Vehiculo


class Sucursal:
    """Representa una sucursal que administra vehículos."""

    def __init__(self, idsucursal: str, ciudad: str, direccion: str) -> None:
        self.idsucursal = idsucursal
        self.ciudad = ciudad
        self.direccion = direccion
        self.vehiculos: list[Vehiculo] = []

    def _validar_texto(self, valor: str, campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{campo} debe ser un texto no vacío.")
        return valor.strip()

    @property
    def idsucursal(self) -> str:
        return self._idsucursal

    @idsucursal.setter
    def idsucursal(self, valor: str) -> None:
        self._idsucursal = self._validar_texto(valor, "El ID de sucursal")

    @property
    def ciudad(self) -> str:
        return self._ciudad

    @ciudad.setter
    def ciudad(self, valor: str) -> None:
        self._ciudad = self._validar_texto(valor, "La ciudad")

    @property
    def direccion(self) -> str:
        return self._direccion

    @direccion.setter
    def direccion(self, valor: str) -> None:
        self._direccion = self._validar_texto(valor, "La dirección")

    @property
    def vehiculos(self) -> list[Vehiculo]:
        return self._vehiculos

    @vehiculos.setter
    def vehiculos(self, valor: list[Vehiculo]) -> None:
        if not isinstance(valor, list):
            raise ValueError("Los vehículos deben almacenarse en una lista.")
        self._vehiculos = valor

    def agregar_vehiculo(self, vehiculo: Vehiculo) -> None:
        """Agrega un vehículo que todavía no esté en la sucursal."""
        if not isinstance(vehiculo, Vehiculo):
            raise ValueError("Solo se pueden agregar objetos Vehiculo.")
        if vehiculo in self.vehiculos:
            raise ValueError("El vehículo ya pertenece a esta sucursal.")
        self.vehiculos.append(vehiculo)
        RegistroHistorial().registrar(
            "Vehículo agregado", f"{vehiculo.patente} agregado a sucursal {self.idsucursal}."
        )

    def remover_vehiculo(self, vehiculo: Vehiculo) -> None:
        """Retira un vehículo o lanza una excepción si no está presente."""
        if vehiculo not in self.vehiculos:
            raise ValueError("El vehículo no está en esta sucursal.")
        self.vehiculos.remove(vehiculo)

    def transferir_vehiculo(self, vehiculo: Vehiculo, otra_sucursal: "Sucursal") -> None:
        """Mueve un vehículo a otra sucursal."""
        if not isinstance(otra_sucursal, Sucursal):
            raise ValueError("El destino debe ser una Sucursal.")
        if otra_sucursal is self:
            raise ValueError("La sucursal de destino debe ser diferente.")
        self.remover_vehiculo(vehiculo)
        try:
            otra_sucursal.agregar_vehiculo(vehiculo)
        except Exception:
            self.vehiculos.append(vehiculo)
            raise
        RegistroHistorial().registrar(
            "Vehículo transferido",
            f"{vehiculo.patente}: {self.idsucursal} -> {otra_sucursal.idsucursal}.",
        )

    def listar_vehiculos(self) -> None:
        """Muestra los vehículos registrados en la sucursal."""
        print(f"Sucursal {self.idsucursal} - {self.ciudad}, {self.direccion}")
        if not self.vehiculos:
            print("  No hay vehículos registrados.")
            return
        for vehiculo in self.vehiculos:
            print(f"  {vehiculo}")

    def __str__(self) -> str:
        return f"[{self.idsucursal}] {self.ciudad} - {self.direccion}"
