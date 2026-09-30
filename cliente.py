"""Modelo de clientes del sistema de alquiler."""


class Cliente:
    """Representa a una persona que puede realizar reservas."""

    def __init__(
        self,
        id_cliente: str,
        dni: str,
        nombre: str,
        apellido: str,
        telefono: str,
        correo_electronico: str,
    ) -> None:
        self.id_cliente = id_cliente
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo_electronico = correo_electronico

    def _validar_texto(self, valor: str, campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{campo} debe ser un texto no vacío.")
        return valor.strip()

    @property
    def id_cliente(self) -> str:
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, valor: str) -> None:
        self._id_cliente = self._validar_texto(valor, "El ID del cliente")

    @property
    def dni(self) -> str:
        return self._dni

    @dni.setter
    def dni(self, valor: str) -> None:
        valor = self._validar_texto(valor, "El DNI")
        caracteres_validos = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-"
        if not 6 <= len(valor) <= 20 or any(
            caracter not in caracteres_validos for caracter in valor
        ):
            raise ValueError("El DNI debe tener entre 6 y 20 caracteres válidos.")
        self._dni = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = self._validar_texto(valor, "El nombre")

    @property
    def apellido(self) -> str:
        return self._apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        self._apellido = self._validar_texto(valor, "El apellido")

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        valor = self._validar_texto(valor, "El teléfono")
        caracteres_validos = "+0123456789()- "
        digitos = 0
        for caracter in valor:
            if caracter not in caracteres_validos:
                raise ValueError("El teléfono contiene caracteres inválidos.")
            if caracter.isdigit():
                digitos += 1
        if not 7 <= digitos <= 15:
            raise ValueError("El teléfono debe contener entre 7 y 15 dígitos.")
        self._telefono = valor

    @property
    def correo_electronico(self) -> str:
        return self._correo_electronico

    @correo_electronico.setter
    def correo_electronico(self, valor: str) -> None:
        valor = self._validar_texto(valor, "El correo electrónico")
        partes = valor.split("@")
        if (
            len(partes) != 2
            or not partes[0]
            or "." not in partes[1]
            or partes[1].startswith(".")
            or partes[1].endswith(".")
            or " " in valor
        ):
            raise ValueError("El correo electrónico no tiene un formato válido.")
        self._correo_electronico = valor

    def __str__(self) -> str:
        return (
            f"[{self.id_cliente}] {self.nombre} {self.apellido} | "
            f"DNI: {self.dni} | Tel: {self.telefono} | "
            f"Correo: {self.correo_electronico}"
        )
