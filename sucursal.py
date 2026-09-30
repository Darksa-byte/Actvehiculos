from registrohistorial import RegistroHistorial


class Sucursal:
    def __init__(self, idsucursal, ciudad, direccion):
        self.idsucursal = idsucursal
        self.ciudad = ciudad
        self.direccion = direccion
        self.vehiculos = []

    def _validar_texto(self, texto, campo):
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError(f"{campo} no puede estar vacío.")
        return texto.strip()

    @property
    def idsucursal(self):
        return self.__idsucursal

    @idsucursal.setter
    def idsucursal(self, valor):
        self.__idsucursal = self._validar_texto(valor, "El ID de sucursal")

    @property
    def ciudad(self):
        return self.__ciudad

    @ciudad.setter
    def ciudad(self, valor):
        self.__ciudad = self._validar_texto(valor, "La ciudad")

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, valor):
        self.__direccion = self._validar_texto(valor, "La dirección")

    @property
    def vehiculos(self):
        return self.__vehiculos

    @vehiculos.setter
    def vehiculos(self, lista_vehiculos):
        if not isinstance(lista_vehiculos, list):
            raise ValueError("Los vehículos deben guardarse en una lista.")
        self.__vehiculos = lista_vehiculos

    def agregar_vehiculo(self, vehiculo):
        if vehiculo in self.vehiculos:
            raise ValueError("El vehículo ya pertenece a esta sucursal.")
        self.vehiculos.append(vehiculo)
        RegistroHistorial().registrar(
            "Vehículo agregado", f"{vehiculo.patente} agregado a sucursal {self.idsucursal}."
        )

    def remover_vehiculo(self, vehiculo):
        if vehiculo not in self.vehiculos:
            raise ValueError("El vehículo no está en esta sucursal.")
        self.vehiculos.remove(vehiculo)

    def transferir_vehiculo(self, vehiculo, otra_sucursal):
        if otra_sucursal is self:
            raise ValueError("La sucursal de destino debe ser diferente.")
        if vehiculo not in self.vehiculos:
            raise ValueError("El vehículo no está en esta sucursal.")
        if vehiculo in otra_sucursal.vehiculos:
            raise ValueError("El vehículo ya está en la sucursal de destino.")
        self.vehiculos.remove(vehiculo)
        otra_sucursal.agregar_vehiculo(vehiculo)
        RegistroHistorial().registrar(
            "Vehículo transferido",
            f"{vehiculo.patente}: {self.idsucursal} -> {otra_sucursal.idsucursal}.",
        )

    def listar_vehiculos(self):
        print(f"Sucursal {self.idsucursal} - {self.ciudad}, {self.direccion}")
        if not self.vehiculos:
            print("  No hay vehículos registrados.")
            return
        for vehiculo in self.vehiculos:
            print(f"  {vehiculo}")

    def __str__(self):
        return f"[{self.idsucursal}] {self.ciudad} - {self.direccion}"
