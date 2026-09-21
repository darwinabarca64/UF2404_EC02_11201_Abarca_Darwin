"""
Ejercicio 5: Refactorización (Refactorització).
Módulo: MF0227_3 - Programación orientada a objetos (UF2404).

Este módulo refactoriza el antipatrón de condicionales múltiples en cascada (`if/elif`),
reemplazándolo por el Patrón Estrategia (Strategy Pattern) y Polimorfismo:
1. Clase base abstracta `Cliente` que define el contrato de cálculo.
2. Clases de clientes concretas con su factor de descuento encapsulado.
3. Extensión sin modificación (`ClienteEstudiante` con 15% de descuento).
4. Clase `Pedido` cerrada a modificaciones y abierta a cualquier nueva estrategia de cliente (OCP).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union

Numero = Union[int, float]


def _validar_positivo(valor: Numero, nombre_campo: str, solo_entero: bool = False) -> float:
    """Valida que un valor numérico sea estrictamente mayor que cero.

    Args:
        valor: Valor numérico a evaluar.
        nombre_campo: Nombre del parámetro para el mensaje de error.
        solo_entero: Si es True, exige que el valor sea un entero (int).

    Returns:
        float: El valor validado.

    Raises:
        TypeError: Si el valor no es del tipo esperado o es un booleano.
        ValueError: Si el valor es menor o igual a cero.
    """
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError(f"El campo '{nombre_campo}' debe ser numérico, recibido: {type(valor).__name__}")
    
    if solo_entero and not isinstance(valor, int):
        raise TypeError(f"El campo '{nombre_campo}' debe ser un número entero (int), recibido: {type(valor).__name__}")
    
    if valor <= 0:
        raise ValueError(f"El campo '{nombre_campo}' debe ser estrictamente positivo (> 0), recibido: {valor}")
    
    return float(valor)


class Cliente(ABC):
    """Clase base abstracta que representa la estrategia de cálculo de precio de un cliente."""

    @property
    @abstractmethod
    def tipo(self) -> str:
        """Nombre descriptivo del tipo de cliente."""
        pass

    @abstractmethod
    def calcular_precio(self, precio: Numero, cantidad: int) -> float:
        """Calcula el importe final aplicando la regla o descuento del cliente.

        Args:
            precio: Precio unitario del producto (> 0).
            cantidad: Cantidad de unidades a adquirir (entero > 0).

        Returns:
            float: Importe total resultante.
        """
        pass

    def __str__(self) -> str:
        return f"Cliente ({self.tipo})"


class ClienteNormal(Cliente):
    """Cliente estándar sin descuentos aplicables (100% del precio)."""

    @property
    def tipo(self) -> str:
        return "Normal"

    def calcular_precio(self, precio: Numero, cantidad: int) -> float:
        return float(precio * cantidad)


class ClienteVIP(Cliente):
    """Cliente VIP con un 20% de descuento (paga el 80%)."""

    @property
    def tipo(self) -> str:
        return "VIP (20% descuento)"

    def calcular_precio(self, precio: Numero, cantidad: int) -> float:
        return float(precio * cantidad * 0.8)


class ClienteEmpleado(Cliente):
    """Cliente empleado con un 50% de descuento (paga el 50%)."""

    @property
    def tipo(self) -> str:
        return "Empleado (50% descuento)"

    def calcular_precio(self, precio: Numero, cantidad: int) -> float:
        return float(precio * cantidad * 0.5)


class ClientePremium(Cliente):
    """Cliente Premium con un 30% de descuento (paga el 70%)."""

    @property
    def tipo(self) -> str:
        return "Premium (30% descuento)"

    def calcular_precio(self, precio: Numero, cantidad: int) -> float:
        return float(precio * cantidad * 0.7)


class ClienteEstudiante(Cliente):
    """Cliente Estudiante añadido mediante extensión con un 15% de descuento (paga el 85%)."""

    @property
    def tipo(self) -> str:
        return "Estudiante (15% descuento)"

    def calcular_precio(self, precio: Numero, cantidad: int) -> float:
        return float(precio * cantidad * 0.85)


# Alias en catalán según requisitos del PDF
ClientNormal = ClienteNormal
ClientVIP = ClienteVIP
ClientEmpleat = ClienteEmpleado
ClientPremium = ClientePremium
ClientEstudiant = ClienteEstudiante


class Pedido:
    """Gestiona el cálculo del pedido delegando polimórficamente en la estrategia de cliente.

    Cumple estrictamente el Principio Abierto/Cerrado (OCP): No requiere modificaciones
    cuando se incorporan nuevas categorías de clientes.
    """

    def calcular_precio(self, cliente: Cliente, precio: Numero, cantidad: int) -> float:
        """Calcula el precio total de una línea de pedido.

        Args:
            cliente: Objeto cliente que implementa la interfaz Cliente.
            precio: Precio unitario del artículo (> 0).
            cantidad: Número entero de unidades (> 0).

        Returns:
            float: Precio total con el descuento aplicado.

        Raises:
            TypeError: Si el cliente no es una instancia de Cliente o los tipos numéricos son inválidos.
            ValueError: Si el precio o la cantidad son menores o iguales a cero.
        """
        if not isinstance(cliente, Cliente):
            raise TypeError(f"El cliente debe ser una instancia de Cliente, recibido: {type(cliente).__name__}")

        p = _validar_positivo(precio, "precio")
        c = int(_validar_positivo(cantidad, "cantidad", solo_entero=True))

        # Delegación polimórfica pura (sin 'if tipo == ...' ni condicionales)
        return cliente.calcular_precio(p, c)


if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN COMPLETA - EJERCICIO 5: REFACTORIZACIÓN (OCP)")
    print("=" * 65)

    pedido = Pedido()
    precio_unitario = 100.0
    unidades = 2
    total_base = precio_unitario * unidades  # 200.0€

    print(f"Parámetros de prueba: Precio base = {precio_unitario}€ | Cantidad = {unidades} uds. | Subtotal = {total_base}€\n")

    # Lista de diferentes tipos de clientes
    clientes_a_probar: list[Cliente] = [
        ClienteNormal(),
        ClienteVIP(),
        ClienteEmpleado(),
        ClientePremium(),
        ClienteEstudiante(),  # Nuevo tipo agregado sin modificar Pedido
    ]

    # Cálculos y aserciones esperadas
    resultados_esperados = {
        "Normal": 200.0,
        "VIP (20% descuento)": 160.0,
        "Empleado (50% descuento)": 100.0,
        "Premium (30% descuento)": 140.0,
        "Estudiante (15% descuento)": 170.0,
    }

    for cli in clientes_a_probar:
        total = pedido.calcular_precio(cli, precio_unitario, unidades)
        esperado = resultados_esperados[cli.tipo]
        print(f"Tipo: {cli.tipo:<28} -> Total a pagar: {total:>6.2f}€")
        assert round(total, 2) == round(esperado, 2), f"Error en cálculo para {cli.tipo}: {total} != {esperado}"

    print("\n[OK] Todos los cálculos polimórficos validados correctamente.")

    # Demostración de robustez ante entradas no válidas
    print("\n--- Pruebas de Gestión de Errores ---")
    try:
        pedido.calcular_precio(ClienteNormal(), -50.0, 2)  # type: ignore
        raise AssertionError("Fallo: Debería haber rechazado precio negativo.")
    except ValueError as e:
        print(f"[OK] Rechazado precio negativo: {e}")

    try:
        pedido.calcular_precio(ClienteNormal(), 100.0, 0)  # type: ignore
        raise AssertionError("Fallo: Debería haber rechazado cantidad cero.")
    except ValueError as e:
        print(f"[OK] Rechazada cantidad cero: {e}")

    try:
        pedido.calcular_precio("texto_invalido", 100.0, 2)  # type: ignore
        raise AssertionError("Fallo: Debería haber rechazado tipo de cliente incorrecto.")
    except TypeError as e:
        print(f"[OK] Rechazado cliente no conforme a interfaz: {e}")

    print("\nTodas las pruebas del Ejercicio 5 pasaron satisfactoriamente.")
