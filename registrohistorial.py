"""Registro centralizado de acciones del sistema."""


class RegistroHistorial:
    """Almacena acciones con fecha, hora, acción y detalles."""

    _historial: list["RegistroHistorial"] = []
    _fecha_actual: str = "sin fecha"
    _hora_actual: str = "00:00:00"

    def __init__(
        self,
        fecha: str | None = None,
        hora: str | None = None,
        accion: str | None = None,
        detalles: str | None = None,
    ) -> None:
        if fecha is None and hora is None and accion is None and detalles is None:
            return
        if fecha is None or hora is None or accion is None or detalles is None:
            raise ValueError("Un registro debe tener todos sus datos.")
        self.fecha = fecha
        self.hora = hora
        self.accion = accion
        self.detalles = detalles

    @property
    def fecha(self) -> str:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La fecha no puede estar vacía.")
        self._fecha = valor

    @property
    def hora(self) -> str:
        return self._hora

    @hora.setter
    def hora(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La hora no puede estar vacía.")
        self._hora = valor

    @property
    def accion(self) -> str:
        return self._accion

    @accion.setter
    def accion(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La acción no puede estar vacía.")
        self._accion = valor.strip()

    @property
    def detalles(self) -> str:
        return self._detalles

    @detalles.setter
    def detalles(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Los detalles no pueden estar vacíos.")
        self._detalles = valor.strip()

    def registrar(self, accion: str, detalles: str) -> "RegistroHistorial":
        """Crea y guarda un registro con la fecha y hora configuradas."""
        registro = RegistroHistorial(
            RegistroHistorial._fecha_actual,
            RegistroHistorial._hora_actual,
            accion,
            detalles,
        )
        self._historial.append(registro)
        return registro

    def ingresar_fecha(self, fecha: str) -> None:
        """Establece la fecha que usarán los próximos registros."""
        if not isinstance(fecha, str) or not fecha.strip():
            raise ValueError("La fecha no puede estar vacía.")
        RegistroHistorial._fecha_actual = fecha.strip()

    def ingresar_hora(self, hora: str) -> None:
        """Establece la hora que usarán los próximos registros."""
        partes = hora.strip().split(":")
        if len(partes) not in {2, 3} or not all(parte.isdigit() for parte in partes):
            raise ValueError("La hora debe tener formato HH:MM o HH:MM:SS.")
        horas = int(partes[0])
        minutos = int(partes[1])
        segundos = int(partes[2]) if len(partes) == 3 else 0
        if not 0 <= horas <= 23 or not 0 <= minutos <= 59 or not 0 <= segundos <= 59:
            raise ValueError("La hora ingresada no es válida.")
        RegistroHistorial._hora_actual = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    def mostrar_historial(self) -> None:
        """Imprime todos los registros guardados."""
        if not self._historial:
            print("No hay registros en el historial.")
            return
        for registro in self._historial:
            print(
                f"{registro.fecha} {registro.hora} | "
                f"{registro.accion} | {registro.detalles}"
            )

    def __str__(self) -> str:
        return (
            f"{self.fecha} {self.hora} | "
            f"{self.accion} | {self.detalles}"
        )
