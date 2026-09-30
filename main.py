"""Punto de entrada del sistema de alquiler de vehículos."""

from auto import Auto
from camioneta import Camioneta
from cliente import Cliente
from moto import Moto
from registrohistorial import RegistroHistorial
from reserva import Reserva
from sucursal import Sucursal
from vehiculo import Vehiculo

class Aplicacion:
    """Coordina los datos en memoria y las operaciones del menú."""

    def __init__(self) -> None:
        self.clientes: dict[str, Cliente] = {}
        self.reservas: dict[str, Reserva] = {}
        self.sucursales: dict[str, Sucursal] = {
            "S1": Sucursal("S1", "Centro", "Av. Principal 100"),
            "S2": Sucursal("S2", "Norte", "Calle Norte 200"),
        }
        self._contador_reservas = 1

    def _leer_no_vacio(self, mensaje: str) -> str:
        while True:
            valor = input(mensaje).strip()
            if valor:
                return valor
            print("El valor no puede estar vacío.")

    def _leer_entero(self, mensaje: str, minimo: int | None = None) -> int:
        while True:
            try:
                valor = int(input(mensaje).strip())
                if minimo is not None and valor < minimo:
                    raise ValueError
                return valor
            except ValueError:
                limite = f" mayor o igual que {minimo}" if minimo is not None else ""
                print(f"Ingrese un entero válido{limite}.")

    def _leer_decimal(self, mensaje: str) -> float:
        while True:
            try:
                return float(input(mensaje).strip().replace(",", "."))
            except ValueError:
                print("Ingrese un número válido.")

    def _leer_fecha(self, mensaje: str) -> str:
        while True:
            valor = input(mensaje).strip()
            partes = valor.split("-")
            if len(partes) == 3 and all(parte.isdigit() for parte in partes):
                anio, mes, dia = [int(parte) for parte in partes]
                if anio > 0 and 1 <= mes <= 12 and 1 <= dia <= 31:
                    return f"{anio:04d}-{mes:02d}-{dia:02d}"
            print("Ingrese una fecha válida con formato AAAA-MM-DD.")

    def configurar_fecha_hora(self) -> None:
        """Solicita fecha y hora para los próximos registros."""
        fecha = self._leer_fecha("Fecha del historial (AAAA-MM-DD): ")
        hora = self._leer_no_vacio("Hora del historial (HH:MM o HH:MM:SS): ")
        historial = RegistroHistorial()
        historial.ingresar_fecha(fecha)
        historial.ingresar_hora(hora)
        print("Fecha y hora configuradas para los próximos registros.")

    def _seleccionar(
        self, elementos: list, descripcion, mensaje: str
    ) -> object:
        if not elementos:
            raise ValueError("No hay elementos disponibles para seleccionar.")
        for indice, elemento in enumerate(elementos, 1):
            print(f"{indice}. {descripcion(elemento)}")
        indice = self._leer_entero(mensaje, 1)
        if indice > len(elementos):
            raise ValueError("La opción seleccionada no existe.")
        return elementos[indice - 1]

    def registrar_cliente(self) -> None:
        """Solicita datos y registra un cliente."""
        cliente = Cliente(
            self._leer_no_vacio("ID del cliente: "),
            self._leer_no_vacio("DNI: "),
            self._leer_no_vacio("Nombre: "),
            self._leer_no_vacio("Apellido: "),
            self._leer_no_vacio("Teléfono: "),
            self._leer_no_vacio("Correo electrónico: "),
        )
        if cliente.id_cliente in self.clientes:
            raise ValueError("Ya existe un cliente con ese ID.")
        self.clientes[cliente.id_cliente] = cliente
        RegistroHistorial().registrar("Cliente registrado", str(cliente))
        print("Cliente registrado correctamente.")

    def agregar_vehiculo(self) -> None:
        """Crea un vehículo y lo agrega a una sucursal."""
        sucursal = self._seleccionar(
            list(self.sucursales.values()), str, "Seleccione la sucursal: "
        )
        tipo = self._leer_no_vacio("Tipo (Auto/Camioneta/Moto): ").lower()
        patente = self._leer_no_vacio("Patente: ")
        if any(
            vehiculo.patente == patente.upper()
            for sucursal_item in self.sucursales.values()
            for vehiculo in sucursal_item.vehiculos
        ):
            raise ValueError("Ya existe un vehículo con esa patente.")
        marca = self._leer_no_vacio("Marca: ")
        modelo = self._leer_no_vacio("Modelo: ")
        tarifa = self._leer_decimal("Tarifa base por día: ")
        clases = {"auto": Auto, "camioneta": Camioneta, "moto": Moto}
        if tipo not in clases:
            raise ValueError("El tipo debe ser Auto, Camioneta o Moto.")
        vehiculo = clases[tipo](patente, marca, modelo, tarifa)
        sucursal.agregar_vehiculo(vehiculo)
        print("Vehículo agregado correctamente.")

    def listar_vehiculos(self) -> None:
        """Lista los vehículos de la sucursal seleccionada."""
        sucursal = self._seleccionar(
            list(self.sucursales.values()), str, "Seleccione la sucursal: "
        )
        sucursal.listar_vehiculos()

    def transferir_vehiculo(self) -> None:
        """Transfiere un vehículo entre dos sucursales."""
        origen = self._seleccionar(
            list(self.sucursales.values()), str, "Seleccione la sucursal de origen: "
        )
        vehiculo = self._seleccionar(
            origen.vehiculos, str, "Seleccione el vehículo: "
        )
        destinos = [sucursal for sucursal in self.sucursales.values() if sucursal is not origen]
        destino = self._seleccionar(destinos, str, "Seleccione la sucursal destino: ")
        origen.transferir_vehiculo(vehiculo, destino)
        print("Vehículo transferido correctamente.")

    def crear_reserva(self) -> None:
        """Crea una reserva para un cliente y un vehículo disponible."""
        cliente = self._seleccionar(
            list(self.clientes.values()), str, "Seleccione el cliente: "
        )
        vehiculos = [
            vehiculo
            for sucursal in self.sucursales.values()
            for vehiculo in sucursal.vehiculos
            if vehiculo.estado == "disponible"
        ]
        vehiculo = self._seleccionar(vehiculos, str, "Seleccione el vehículo disponible: ")
        fecha_inicio = self._leer_fecha("Fecha de inicio (AAAA-MM-DD): ")
        fecha_fin = self._leer_fecha("Fecha de finalización (AAAA-MM-DD): ")
        id_reserva = f"R{self._contador_reservas:04d}"
        reserva = Reserva(id_reserva, cliente, vehiculo, fecha_inicio, fecha_fin)
        self.reservas[reserva.id] = reserva
        self._contador_reservas += 1
        print(f"Reserva creada: {reserva}")

    def cambiar_estado_reserva(self) -> None:
        """Cambia el estado de una reserva existente."""
        reserva = self._seleccionar(
            list(self.reservas.values()), str, "Seleccione la reserva: "
        )
        nuevo_estado = self._leer_no_vacio(
            "Nuevo estado (confirmada/cancelada/finalizada): "
        ).lower()
        reserva.cambiar_estado(nuevo_estado)
        print("Estado actualizado correctamente.")

    def calcular_costo(self) -> None:
        """Muestra el costo total de una reserva."""
        reserva = self._seleccionar(
            list(self.reservas.values()), str, "Seleccione la reserva: "
        )
        print(f"Días: {reserva.calcular_dias()}")
        print(f"Costo total: ${reserva.calcular_costo_total():.2f}")

    def mostrar_menu(self) -> None:
        """Ejecuta el ciclo principal de interacción."""
        acciones = {
            "1": self.registrar_cliente,
            "2": self.agregar_vehiculo,
            "3": self.listar_vehiculos,
            "4": self.transferir_vehiculo,
            "5": self.crear_reserva,
            "6": self.cambiar_estado_reserva,
            "7": self.calcular_costo,
            "8": RegistroHistorial().mostrar_historial,
            "9": self.configurar_fecha_hora,
        }
        while True:
            print(
                "\n=== SISTEMA DE ALQUILER DE VEHÍCULOS ===\n"
                "1. Registrar cliente\n"
                "2. Agregar vehículo a sucursal\n"
                "3. Listar vehículos de una sucursal\n"
                "4. Transferir vehículo entre sucursales\n"
                "5. Crear reserva\n"
                "6. Cambiar estado de reserva\n"
                "7. Calcular costo total de una reserva\n"
                "8. Ver historial de registros\n"
                "9. Ingresar fecha y hora para el historial\n"
                "10. Salir"
            )
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "10":
                print("Hasta luego.")
                return
            accion = acciones.get(opcion)
            if accion is None:
                print("Opción inválida.")
                continue
            try:
                accion()
            except (ValueError, TypeError) as error:
                print(f"Error: {error}")


def main() -> None:
    """Inicia la aplicación interactiva."""
    Aplicacion().mostrar_menu()


if __name__ == "__main__":
    main()
