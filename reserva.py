"""Reservas, estados y control de disponibilidad de vehículos."""

from cliente import Cliente
from notificaciones import Notificaciones
from registrohistorial import RegistroHistorial
from vehiculo import Vehiculo


class Reserva:
    """Relaciona un cliente con un vehículo durante un período."""

    ESTADOS_VALIDOS = {"pendiente", "confirmada", "cancelada", "finalizada"}
    _reservas: list["Reserva"] = []
    _TRANSICIONES: dict[str, set[str]] = {
        "pendiente": {"confirmada", "cancelada"},
        "confirmada": {"cancelada", "finalizada"},
        "cancelada": set(),
        "finalizada": set(),
    }

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        vehiculo: Vehiculo,
        fecha_inicio: str,
        fecha_fin: str,
    ) -> None:
        self.id = id_reserva
        self.cliente = cliente
        self.vehiculo = vehiculo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = "pendiente"
        self._validar_disponibilidad()
        self.vehiculo.estado = "alquilado"
        Reserva._reservas.append(self)
        RegistroHistorial().registrar(
            "Reserva creada",
            f"Reserva {self.id}: vehículo {self.vehiculo.patente} por {self.calcular_dias()} días.",
        )

    def _validar_texto(self, valor: str, campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{campo} debe ser un texto no vacío.")
        return valor.strip()

    def _validar_fecha(self, valor: str) -> str:
        """Valida una fecha escrita como AAAA-MM-DD sin usar librerías."""
        partes = valor.split("-") if isinstance(valor, str) else []
        if len(partes) != 3 or not all(parte.isdigit() for parte in partes):
            raise ValueError("La fecha debe tener formato AAAA-MM-DD.")
        anio, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
        if anio < 1 or mes < 1 or mes > 12:
            raise ValueError("La fecha no es válida.")
        dias_mes = [31, 29 if self._es_bisiesto(anio) else 28, 31, 30, 31, 30,
                    31, 31, 30, 31, 30, 31]
        if dia < 1 or dia > dias_mes[mes - 1]:
            raise ValueError("La fecha no es válida.")
        return f"{anio:04d}-{mes:02d}-{dia:02d}"

    def _es_bisiesto(self, anio: int) -> bool:
        return anio % 400 == 0 or (anio % 4 == 0 and anio % 100 != 0)

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, valor: str) -> None:
        self._id = self._validar_texto(valor, "El ID de reserva")

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @cliente.setter
    def cliente(self, valor: Cliente) -> None:
        if not isinstance(valor, Cliente):
            raise ValueError("El cliente debe ser un objeto Cliente.")
        self._cliente = valor

    @property
    def vehiculo(self) -> Vehiculo:
        return self._vehiculo

    @vehiculo.setter
    def vehiculo(self, valor: Vehiculo) -> None:
        if not isinstance(valor, Vehiculo):
            raise ValueError("El vehículo debe ser un objeto Vehiculo.")
        self._vehiculo = valor

    @property
    def fecha_inicio(self) -> str:
        return self._fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, valor: str) -> None:
        valor = self._validar_fecha(valor)
        self._fecha_inicio = valor
        if hasattr(self, "_fecha_fin") and self._fecha_fin <= valor:
            raise ValueError("La fecha de finalización debe ser posterior a la de inicio.")

    @property
    def fecha_fin(self) -> str:
        return self._fecha_fin

    @fecha_fin.setter
    def fecha_fin(self, valor: str) -> None:
        valor = self._validar_fecha(valor)
        if hasattr(self, "_fecha_inicio") and valor <= self._fecha_inicio:
            raise ValueError("La fecha de finalización debe ser posterior a la de inicio.")
        self._fecha_fin = valor

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, valor: str) -> None:
        if valor not in self.ESTADOS_VALIDOS:
            permitidos = ", ".join(sorted(self.ESTADOS_VALIDOS))
            raise ValueError(f"Estado inválido. Valores permitidos: {permitidos}.")
        self._estado = valor

    def _validar_disponibilidad(self) -> None:
        if self.vehiculo.estado == "en mantenimiento":
            raise ValueError("No se puede reservar un vehículo en mantenimiento.")
        for reserva in Reserva._reservas:
            if reserva.vehiculo is self.vehiculo and reserva.estado in {"pendiente", "confirmada"}:
                hay_solapamiento = (
                    self.fecha_inicio < reserva.fecha_fin
                    and reserva.fecha_inicio < self.fecha_fin
                )
                if hay_solapamiento:
                    raise ValueError("El vehículo ya está asignado a otra reserva activa en ese período.")

    def cambiar_estado(self, nuevo_estado: str) -> None:
        """Valida una transición, actualiza disponibilidad y notifica al cliente."""
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado de reserva inválido: {nuevo_estado}.")
        permitidos = self._TRANSICIONES[self.estado]
        if nuevo_estado not in permitidos:
            raise ValueError(f"No se permite pasar de {self.estado} a {nuevo_estado}.")
        if nuevo_estado == "confirmada":
            self._validar_disponibilidad_sin_esta_reserva()
            if self.vehiculo.estado != "alquilado":
                raise ValueError("No se puede confirmar: el vehículo no está asignado a esta reserva.")
        self.estado = nuevo_estado
        if nuevo_estado in {"cancelada", "finalizada"}:
            self.vehiculo.estado = "disponible"
        RegistroHistorial().registrar(
            "Estado de reserva cambiado",
            f"Reserva {self.id}: {self.estado} para {self.vehiculo.patente}.",
        )
        notificacion = Notificaciones()
        notificacion.notificar(
            self.cliente, f"La reserva {self.id} ahora está {self.estado}."
        )

    def _validar_disponibilidad_sin_esta_reserva(self) -> None:
        for reserva in Reserva._reservas:
            if reserva is self or reserva.vehiculo is not self.vehiculo:
                continue
            if reserva.estado in {"pendiente", "confirmada"} and (
                self.fecha_inicio < reserva.fecha_fin
                and reserva.fecha_inicio < self.fecha_fin
            ):
                raise ValueError("El vehículo no está disponible para confirmar este período.")

    def calcular_dias(self) -> int:
        """Devuelve la cantidad de días del alquiler."""
        inicio = self._convertir_a_dias(self.fecha_inicio)
        fin = self._convertir_a_dias(self.fecha_fin)
        dias = fin - inicio
        if dias <= 0:
            raise ValueError("El alquiler debe durar al menos un día.")
        return dias

    def _convertir_a_dias(self, fecha: str) -> int:
        anio, mes, dia = [int(parte) for parte in fecha.split("-")]
        total = anio * 365 + anio // 4 - anio // 100 + anio // 400
        dias_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for numero_mes in range(1, mes):
            total += dias_mes[numero_mes - 1]
            if numero_mes == 2 and self._es_bisiesto(anio):
                total += 1
        return total + dia

    def calcular_costo_total(self) -> float:
        """Calcula el costo usando la fórmula específica del vehículo."""
        costo = self.vehiculo.calcular_costo(self.calcular_dias())
        if costo < 0:
            raise ValueError("El costo total de un alquiler nunca puede ser negativo.")
        return costo

    def __str__(self) -> str:
        return (
            f"Reserva {self.id} | Cliente: {self.cliente.nombre} {self.cliente.apellido} | "
            f"Vehículo: {self.vehiculo.patente} | {self.fecha_inicio} a {self.fecha_fin} | "
            f"Estado: {self.estado}"
        )
