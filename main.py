from datetime import datetime

from auto import Auto
from camioneta import Camioneta
from cliente import Cliente
from moto import Moto
from registrohistorial import RegistroHistorial
from reserva import Reserva
from sucursal import Sucursal

class Aplicacion:
    def __init__(self):
        self.__clientes = {}
        self.__reservas = {}
        self.__sucursales = {
            "S1": Sucursal("S1", "Centro", "Av. Principal 100"),
            "S2": Sucursal("S2", "Norte", "Calle Norte 200"),
        }
        self.__contador_reservas = 1

    def _leer_no_vacio(self, mensaje):
        while True:
            valor = input(mensaje).strip()
            if valor:
                return valor
            print("El valor no puede estar vacío.")

    def _leer_entero(self, mensaje, minimo=None):
        while True:
            try:
                valor = int(input(mensaje).strip())
                if minimo is not None and valor < minimo:
                    raise ValueError
                return valor
            except ValueError:
                limite = f" mayor o igual que {minimo}" if minimo is not None else ""
                print(f"Ingrese un entero válido{limite}.")

    def _leer_decimal(self, mensaje):
        while True:
            try:
                return float(input(mensaje).strip().replace(",", "."))
            except ValueError:
                print("Ingrese un número válido.")

    def _leer_fecha(self, mensaje):
        while True:
            valor = input(mensaje).strip()
            try:
                fecha = datetime.strptime(valor, "%Y-%m-%d")
                return fecha.strftime("%Y-%m-%d")
            except ValueError:
                pass
            print("Ingrese una fecha válida con formato AAAA-MM-DD.")

    def configurar_fecha_hora(self):
        fecha = self._leer_fecha("Fecha del historial (AAAA-MM-DD): ")
        hora = self._leer_no_vacio("Hora del historial (HH:MM o HH:MM:SS): ")
        historial = RegistroHistorial()
        historial.ingresar_fecha(fecha)
        historial.ingresar_hora(hora)
        print("Fecha y hora configuradas para los próximos registros.")

    def _seleccionar(self, elementos, mensaje):
        if not elementos:
            raise ValueError("No hay elementos disponibles para seleccionar.")
        for indice, elemento in enumerate(elementos, 1):
            print(f"{indice}. {elemento}")
        indice = self._leer_entero(mensaje, 1)
        if indice > len(elementos):
            raise ValueError("La opción seleccionada no existe.")
        return elementos[indice - 1]

    def registrar_cliente(self):
        cliente = Cliente(
            self._leer_no_vacio("ID del cliente: "),
            self._leer_no_vacio("DNI: "),
            self._leer_no_vacio("Nombre: "),
            self._leer_no_vacio("Apellido: "),
            self._leer_no_vacio("Teléfono: "),
            self._leer_no_vacio("Correo electrónico: "),
        )
        if cliente.id_cliente in self.__clientes:
            raise ValueError("Ya existe un cliente con ese ID.")
        self.__clientes[cliente.id_cliente] = cliente
        RegistroHistorial().registrar("Cliente registrado", str(cliente))
        print("Cliente registrado correctamente.")

    def agregar_vehiculo(self):
        sucursal = self._seleccionar(list(self.__sucursales.values()), "Seleccione la sucursal: ")
        tipo = self._leer_no_vacio("Tipo (Auto/Camioneta/Moto): ").lower()
        patente = self._leer_no_vacio("Patente: ")
        for sucursal_item in self.__sucursales.values():
            for vehiculo_actual in sucursal_item.vehiculos:
                if vehiculo_actual.patente == patente.upper():
                    raise ValueError("Ya existe un vehículo con esa patente.")
        marca = self._leer_no_vacio("Marca: ")
        modelo = self._leer_no_vacio("Modelo: ")
        tarifa = self._leer_decimal("Tarifa base por día: ")
        if tipo == "auto":
            vehiculo = Auto(patente, marca, modelo, tarifa)
        elif tipo == "camioneta":
            vehiculo = Camioneta(patente, marca, modelo, tarifa)
        elif tipo == "moto":
            vehiculo = Moto(patente, marca, modelo, tarifa)
        else:
            raise ValueError("El tipo debe ser Auto, Camioneta o Moto.")
        sucursal.agregar_vehiculo(vehiculo)
        print("Vehículo agregado correctamente.")

    def listar_vehiculos(self):
        sucursal = self._seleccionar(list(self.__sucursales.values()), "Seleccione la sucursal: ")
        sucursal.listar_vehiculos()

    def transferir_vehiculo(self):
        origen = self._seleccionar(
            list(self.__sucursales.values()), "Seleccione la sucursal de origen: "
        )
        vehiculo = self._seleccionar(origen.vehiculos, "Seleccione el vehículo: ")
        destinos = []
        for sucursal in self.__sucursales.values():
            if sucursal is not origen:
                destinos.append(sucursal)
        destino = self._seleccionar(destinos, "Seleccione la sucursal destino: ")
        origen.transferir_vehiculo(vehiculo, destino)
        print("Vehículo transferido correctamente.")

    def crear_reserva(self):
        cliente = self._seleccionar(list(self.__clientes.values()), "Seleccione el cliente: ")
        vehiculos = []
        for sucursal in self.__sucursales.values():
            for vehiculo in sucursal.vehiculos:
                if vehiculo.estado == "disponible":
                    vehiculos.append(vehiculo)
        vehiculo = self._seleccionar(vehiculos, "Seleccione el vehículo disponible: ")
        fecha_inicio = self._leer_fecha("Fecha de inicio (AAAA-MM-DD): ")
        fecha_fin = self._leer_fecha("Fecha de finalización (AAAA-MM-DD): ")
        for reserva_actual in self.__reservas.values():
            if reserva_actual.vehiculo is vehiculo:
                if reserva_actual.estado == "pendiente" or reserva_actual.estado == "confirmada":
                    if fecha_inicio < reserva_actual.fecha_fin and reserva_actual.fecha_inicio < fecha_fin:
                        raise ValueError("El vehículo ya está reservado en ese período.")
        id_reserva = f"R{self.__contador_reservas:04d}"
        reserva = Reserva(id_reserva, cliente, vehiculo, fecha_inicio, fecha_fin)
        self.__reservas[reserva.id] = reserva
        self.__contador_reservas += 1
        print(f"Reserva creada: {reserva}")

    def cambiar_estado_reserva(self):
        reserva = self._seleccionar(list(self.__reservas.values()), "Seleccione la reserva: ")
        nuevo_estado = self._leer_no_vacio(
            "Nuevo estado (confirmada/cancelada/finalizada): "
        ).lower()
        reserva.cambiar_estado(nuevo_estado)
        print("Estado actualizado correctamente.")

    def calcular_costo(self):
        reserva = self._seleccionar(list(self.__reservas.values()), "Seleccione la reserva: ")
        print(f"Días: {reserva.calcular_dias()}")
        print(f"Costo total: ${reserva.calcular_costo_total():.2f}")

    def mostrar_menu(self):
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
            try:
                if opcion == "1":
                    self.registrar_cliente()
                elif opcion == "2":
                    self.agregar_vehiculo()
                elif opcion == "3":
                    self.listar_vehiculos()
                elif opcion == "4":
                    self.transferir_vehiculo()
                elif opcion == "5":
                    self.crear_reserva()
                elif opcion == "6":
                    self.cambiar_estado_reserva()
                elif opcion == "7":
                    self.calcular_costo()
                elif opcion == "8":
                    RegistroHistorial().mostrar_historial()
                elif opcion == "9":
                    self.configurar_fecha_hora()
                elif opcion == "10":
                    print("Hasta luego.")
                    return
                else:
                    print("Opción inválida.")
            except ValueError as error:
                print(f"Error: {error}")


def main():
    Aplicacion().mostrar_menu()


if __name__ == "__main__":
    main()
