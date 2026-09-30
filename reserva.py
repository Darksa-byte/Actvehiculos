from datetime import datetime

from notificaciones import Notificaciones
from registrohistorial import RegistroHistorial


class Reserva:
    def __init__(self, id_reserva, cliente, vehiculo, fecha_inicio, fecha_fin):
        self.__fecha_inicio = ""
        self.__fecha_fin = ""
        self.id = id_reserva
        self.cliente = cliente
        self.vehiculo = vehiculo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = "pendiente"
        self.vehiculo.estado = "alquilado"
        RegistroHistorial().registrar(
            "Reserva creada",
            f"Reserva {self.id}: vehículo {self.vehiculo.patente} por {self.calcular_dias()} días.",
        )

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        if not valor.strip():
            raise ValueError("El ID de la reserva no puede estar vacío.")
        self.__id = valor.strip()

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, valor):
        if valor is None:
            raise ValueError("La reserva debe tener un cliente.")
        self.__cliente = valor

    @property
    def vehiculo(self):
        return self.__vehiculo

    @vehiculo.setter
    def vehiculo(self, valor):
        if valor is None:
            raise ValueError("La reserva debe tener un vehículo.")
        self.__vehiculo = valor

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, valor):
        fecha = self._validar_fecha(valor)
        if self.__fecha_fin and fecha >= self.__fecha_fin:
            raise ValueError("La fecha final debe ser posterior a la fecha inicial.")
        self.__fecha_inicio = fecha

    @property
    def fecha_fin(self):
        return self.__fecha_fin

    @fecha_fin.setter
    def fecha_fin(self, valor):
        fecha = self._validar_fecha(valor)
        if self.__fecha_inicio and fecha <= self.__fecha_inicio:
            raise ValueError("La fecha final debe ser posterior a la fecha inicial.")
        self.__fecha_fin = fecha

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        estados_validos = ["pendiente", "confirmada", "cancelada", "finalizada"]
        if valor not in estados_validos:
            raise ValueError("El estado de la reserva no es válido.")
        self.__estado = valor

    def _validar_fecha(self, fecha):
        try:
            fecha_valida = datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener formato AAAA-MM-DD.")
        return fecha_valida.strftime("%Y-%m-%d")

    def cambiar_estado(self, nuevo_estado):
        cambio_valido = False

        if self.estado == "pendiente":
            if nuevo_estado == "confirmada" or nuevo_estado == "cancelada":
                cambio_valido = True
        elif self.estado == "confirmada":
            if nuevo_estado == "cancelada" or nuevo_estado == "finalizada":
                cambio_valido = True

        if not cambio_valido:
            raise ValueError("No se puede realizar ese cambio de estado.")

        self.estado = nuevo_estado
        if nuevo_estado == "cancelada" or nuevo_estado == "finalizada":
            self.vehiculo.estado = "disponible"

        RegistroHistorial().registrar(
            "Estado de reserva cambiado",
            f"Reserva {self.id}: {self.estado} para {self.vehiculo.patente}.",
        )
        Notificaciones().notificar(
            self.cliente, f"La reserva {self.id} ahora está {self.estado}."
        )

    def calcular_dias(self):
        inicio = datetime.strptime(self.fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(self.fecha_fin, "%Y-%m-%d")
        return (fin - inicio).days

    def calcular_costo_total(self):
        return self.vehiculo.calcular_costo(self.calcular_dias())

    def __str__(self):
        return (
            f"Reserva {self.id} | Cliente: {self.cliente.nombre} {self.cliente.apellido} | "
            f"Vehículo: {self.vehiculo.patente} | {self.fecha_inicio} a {self.fecha_fin} | "
            f"Estado: {self.estado}"
        )
