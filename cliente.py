class Cliente:
    def __init__(self, id_cliente, dni, nombre, apellido, telefono, correo_electronico):
        self.id_cliente = id_cliente
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo_electronico = correo_electronico

    def _validar_texto(self, texto):
        if not texto.strip():
            raise ValueError("Los datos del cliente no pueden estar vacíos.")
        return texto.strip()

    @property
    def id_cliente(self):
        return self.__id_cliente

    @id_cliente.setter
    def id_cliente(self, valor):
        self.__id_cliente = self._validar_texto(valor)

    @property
    def dni(self):
        return self.__dni

    @dni.setter
    def dni(self, valor):
        self.__dni = self._validar_texto(valor)

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = self._validar_texto(valor)

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):
        self.__apellido = self._validar_texto(valor)

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        self.__telefono = self._validar_texto(valor)

    @property
    def correo_electronico(self):
        return self.__correo_electronico

    @correo_electronico.setter
    def correo_electronico(self, valor):
        self.__correo_electronico = self._validar_texto(valor)

    def __str__(self):
        return (
            f"[{self.id_cliente}] {self.nombre} {self.apellido} | "
            f"DNI: {self.dni} | Tel: {self.telefono} | "
            f"Correo: {self.correo_electronico}"
        )
