from datetime import datetime


class RegistroHistorial:
    __historial = []
    __fecha_actual = "sin fecha"
    __hora_actual = "00:00:00"

    @property
    def historial(self):
        return RegistroHistorial.__historial

    @property
    def fecha_actual(self):
        return RegistroHistorial.__fecha_actual

    @fecha_actual.setter
    def fecha_actual(self, fecha):
        try:
            fecha_valida = datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener formato AAAA-MM-DD.")
        RegistroHistorial.__fecha_actual = fecha_valida.strftime("%Y-%m-%d")

    @property
    def hora_actual(self):
        return RegistroHistorial.__hora_actual

    @hora_actual.setter
    def hora_actual(self, hora):
        try:
            hora_valida = datetime.strptime(hora, "%H:%M")
        except ValueError:
            try:
                hora_valida = datetime.strptime(hora, "%H:%M:%S")
            except ValueError:
                raise ValueError("La hora debe tener formato HH:MM o HH:MM:SS.")
        RegistroHistorial.__hora_actual = hora_valida.strftime("%H:%M:%S")

    def registrar(self, accion, detalles):
        registro = {
            "fecha": self.fecha_actual,
            "hora": self.hora_actual,
            "accion": accion,
            "detalles": detalles,
        }
        self.historial.append(registro)

    def ingresar_fecha(self, fecha):
        self.fecha_actual = fecha

    def ingresar_hora(self, hora):
        self.hora_actual = hora

    def mostrar_historial(self):
        if not self.historial:
            print("No hay registros en el historial.")
            return

        for registro in self.historial:
            print(
                f"{registro['fecha']} {registro['hora']} | "
                f"{registro['accion']} | {registro['detalles']}"
            )
