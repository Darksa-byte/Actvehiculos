class Vehiculo:
    def __init__(self, tipo_vehiculo, patente, marca, modelo, tarifa_base_por_dia):
        self.tipo_vehiculo = tipo_vehiculo
        self.patente = patente
        self.marca = marca
        self.modelo = modelo
        self.tarifa_base_por_dia = tarifa_base_por_dia
        self.estado = "disponible"

    def _validar_texto(self, texto, campo):
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError(f"{campo} no puede estar vacío.")
        return texto.strip()

    @property
    def tipo_vehiculo(self):
        return self.__tipo_vehiculo

    @tipo_vehiculo.setter
    def tipo_vehiculo(self, valor):
        self.__tipo_vehiculo = self._validar_texto(valor, "El tipo de vehículo")

    @property
    def patente(self):
        return self.__patente

    @patente.setter
    def patente(self, valor):
        patente = self._validar_texto(valor, "La patente")
        if len(patente) < 3:
            raise ValueError("La patente debe tener al menos 3 caracteres.")
        self.__patente = patente.upper()

    @property
    def marca(self):
        return self.__marca

    @marca.setter
    def marca(self, valor):
        self.__marca = self._validar_texto(valor, "La marca")

    @property
    def modelo(self):
        return self.__modelo

    @modelo.setter
    def modelo(self, valor):
        self.__modelo = self._validar_texto(valor, "El modelo")

    @property
    def tarifa_base_por_dia(self):
        return self.__tarifa_base_por_dia

    @tarifa_base_por_dia.setter
    def tarifa_base_por_dia(self, valor):
        try:
            tarifa = float(valor)
        except (TypeError, ValueError):
            raise ValueError("La tarifa debe ser un número.")
        if tarifa <= 0:
            raise ValueError("La tarifa por día debe ser mayor que cero.")
        self.__tarifa_base_por_dia = tarifa

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, nuevo_estado):
        estados_validos = ["disponible", "alquilado", "en mantenimiento"]
        if nuevo_estado not in estados_validos:
            raise ValueError("El estado del vehículo no es válido.")
        self.__estado = nuevo_estado

    def calcular_costo(self, dias):
        if dias <= 0:
            raise ValueError("Los días deben ser mayores que cero.")
        return self.tarifa_base_por_dia * dias

    def __str__(self):
        return (
            f"{self.tipo_vehiculo} | Patente: {self.patente} | "
            f"{self.marca} {self.modelo} | ${self.tarifa_base_por_dia:.2f}/día | "
            f"Estado: {self.estado}"
        )
