"""Servicio sencillo de notificaciones por consola."""

from cliente import Cliente


class Notificaciones:
    """Simula el envío de notificaciones a clientes."""

    def notificar(self, cliente: Cliente, mensaje: str) -> None:
        """Imprime una notificación dirigida al correo del cliente."""
        if not isinstance(cliente, Cliente):
            raise ValueError("El destinatario debe ser un objeto Cliente.")
        if not isinstance(mensaje, str) or not mensaje.strip():
            raise ValueError("El mensaje no puede estar vacío.")
        print(f"Notificación enviada a {cliente.correo_electronico}: {mensaje}")
