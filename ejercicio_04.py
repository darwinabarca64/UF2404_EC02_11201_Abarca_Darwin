"""
Ejercicio 4: Historial bancario (Historial bancari).
Módulo: MF0227_3 - Programación orientada a objetos (UF2404).

Este módulo implementa la clase `CuentaBancaria` (y su alias `CompteBancari`) garantizando:
1. Encapsulación estricta de saldo e historial de transacciones.
2. Integridad transaccional y atomicidad en operaciones de transferencia entre cuentas.
3. Protección frente al 'Aliasing Bug' mediante devolución de tuplas inmutables en el historial.
4. Validación rigurosa de importes positivos y control de saldo insuficiente.
"""

from __future__ import annotations
from typing import Tuple, Union

# Tipo para cantidades monetarias válidas
Importe = Union[int, float]


def _validar_cantidad_positiva(cantidad: Importe, nombre_param: str = "cantidad") -> float:
    """Valida que un importe monetario sea numérico y estrictamente mayor que cero.

    Args:
        cantidad: Importe a validar.
        nombre_param: Nombre del parámetro para los mensajes de excepción.

    Returns:
        float: El importe validado y convertido a float.

    Raises:
        TypeError: Si la cantidad no es de tipo int o float (o si es un bool).
        ValueError: Si la cantidad es menor o igual a cero.
    """
    if isinstance(cantidad, bool) or not isinstance(cantidad, (int, float)):
        raise TypeError(f"El valor de '{nombre_param}' debe ser numérico (int o float), recibido: {type(cantidad).__name__}")
    if cantidad <= 0:
        raise ValueError(f"El importe de '{nombre_param}' debe ser estrictamente positivo (> 0), recibido: {cantidad}")
    return float(cantidad)


class CuentaBancaria:
    """Representa una cuenta bancaria con saldo y registro de auditoría de movimientos.

    Attributes:
        titular (str): Nombre del titular de la cuenta.
        saldo (float): Saldo actual disponible (solo lectura mediante propiedad).
    """

    def __init__(self, titular: str, saldo_inicial: Importe = 0.0) -> None:
        """Inicializa una nueva cuenta bancaria.

        Args:
            titular: Nombre del titular de la cuenta (cadena no vacía).
            saldo_inicial: Saldo de partida (por defecto 0.0, no puede ser negativo).

        Raises:
            TypeError: Si el titular no es str o el saldo no es numérico.
            ValueError: Si el titular está vacío o el saldo inicial es negativo.
        """
        if not isinstance(titular, str):
            raise TypeError(f"El titular debe ser una cadena (str), recibido: {type(titular).__name__}")
        
        titular_limpio = titular.strip()
        if not titular_limpio:
            raise ValueError("El nombre del titular no puede estar vacío.")

        if isinstance(saldo_inicial, bool) or not isinstance(saldo_inicial, (int, float)):
            raise TypeError(f"El saldo inicial debe ser numérico, recibido: {type(saldo_inicial).__name__}")
        
        if saldo_inicial < 0:
            raise ValueError(f"El saldo inicial no puede ser negativo, recibido: {saldo_inicial}")

        self._titular: str = titular_limpio
        self._saldo: float = float(saldo_inicial)
        self._historial: list[str] = []

        # Registro opcional de apertura si hubo saldo inicial
        if self._saldo > 0:
            self._historial.append(f"APERTURA CUENTA: +{self._saldo:.2f}")

    @property
    def titular(self) -> str:
        """Nombre del titular de la cuenta bancaria."""
        return self._titular

    @property
    def saldo(self) -> float:
        """Saldo actual disponible en la cuenta bancaria (solo lectura)."""
        return self._saldo

    def ingresar(self, cantidad: Importe) -> None:
        """Realiza un depósito de dinero en la cuenta y lo registra en el historial.

        Args:
            cantidad: Cantidad a depositar (> 0).

        Raises:
            TypeError: Si la cantidad no es numérica.
            ValueError: Si la cantidad es menor o igual a cero.
        """
        cant = _validar_cantidad_positiva(cantidad, "cantidad")
        self._saldo += cant
        self._historial.append(f"INGRESO: +{cant:.2f}")

    # Alias en catalán
    ingressar = ingresar

    def retirar(self, cantidad: Importe) -> None:
        """Retira una cantidad de dinero de la cuenta si hay fondos suficientes.

        Args:
            cantidad: Cantidad a retirar (> 0).

        Raises:
            TypeError: Si la cantidad no es numérica.
            ValueError: Si la cantidad es <= 0 o superior al saldo disponible.
        """
        cant = _validar_cantidad_positiva(cantidad, "cantidad")
        if cant > self._saldo:
            raise ValueError(
                f"Saldo insuficiente para retirar {cant:.2f}€. Saldo actual: {self._saldo:.2f}€"
            )

        self._saldo -= cant
        self._historial.append(f"RETIRADA: -{cant:.2f}")

    def transferir(self, cuenta_destino: CuentaBancaria, cantidad: Importe) -> None:
        """Transfiere dinero hacia otra cuenta de forma atómica.

        Actualiza ambos saldos e historiales tras verificar la viabilidad completa.

        Args:
            cuenta_destino: Instancia de CuentaBancaria que recibirá el importe.
            cantidad: Importe monetario a transferir (> 0).

        Raises:
            TypeError: Si cuenta_destino no es una CuentaBancaria o la cantidad no es numérica.
            ValueError: Si la cuenta destino es la misma o el saldo es insuficiente.
        """
        if not isinstance(cuenta_destino, CuentaBancaria):
            raise TypeError(f"La cuenta de destino debe ser CuentaBancaria, recibido: {type(cuenta_destino).__name__}")
        
        if cuenta_destino is self:
            raise ValueError("No se puede realizar una transferencia a la misma cuenta de origen.")

        cant = _validar_cantidad_positiva(cantidad, "cantidad")

        # Comprobación atómica previa antes de cualquier mutación de estado
        if cant > self._saldo:
            raise ValueError(
                f"Saldo insuficiente para transferir {cant:.2f}€. Saldo actual: {self._saldo:.2f}€"
            )

        # Aplicación atómica de cambios en ambas cuentas
        self._saldo -= cant
        cuenta_destino._saldo += cant

        # Registro en los respectivos historiales
        self._historial.append(f"TRANSFERENCIA EMITIDA: -{cant:.2f} a {cuenta_destino.titular}")
        cuenta_destino._historial.append(f"TRANSFERENCIA RECIBIDA: +{cant:.2f} de {self.titular}")

    def obtener_historial(self) -> Tuple[str, ...]:
        """Devuelve una vista inmutable del historial de operaciones de la cuenta.

        Returns:
            Tuple[str, ...]: Tupla con los registros de auditoría.
        """
        return tuple(self._historial)

    # Alias en catalán
    obtenir_historial = obtener_historial

    def __str__(self) -> str:
        """Representación legible de la cuenta bancaria."""
        return f"CuentaBancaria(titular='{self._titular}', saldo={self._saldo:.2f}€)"

    def __repr__(self) -> str:
        """Representación técnica del objeto."""
        return f"CuentaBancaria(titular={self._titular!r}, saldo={self._saldo!r}, movimientos={len(self._historial)})"


# Alias en catalán según requisitos del PDF
CompteBancari = CuentaBancaria


if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN COMPLETA - EJERCICIO 4: HISTORIAL BANCARIO")
    print("=" * 65)

    # 1. Creación de cuentas iniciales
    c1 = CuentaBancaria("Alicia", saldo_inicial=100.0)
    c2 = CuentaBancaria("Bernat", saldo_inicial=50.0)
    print(f"Cuenta 1 creada: {c1}")
    print(f"Cuenta 2 creada: {c2}")
    assert c1.saldo == 100.0
    assert c2.saldo == 50.0

    # 2. Operaciones normales de ingreso y retirada
    print("\n--- Operaciones de Ingreso y Retirada ---")
    c1.ingresar(50.0)
    print(f"Alicia tras ingresar 50€ -> Saldo: {c1.saldo}€")
    assert c1.saldo == 150.0

    c1.retirar(30.0)
    print(f"Alicia tras retirar 30€ -> Saldo: {c1.saldo}€")
    assert c1.saldo == 120.0

    # 3. Operación de transferencia
    print("\n--- Transferencia entre Cuentas ---")
    c1.transferir(c2, 40.0)
    print(f"Alicia transfirió 40€ a Bernat.")
    print(f"Nuevo saldo Alicia: {c1.saldo}€")
    print(f"Nuevo saldo Bernat: {c2.saldo}€")
    assert c1.saldo == 80.0
    assert c2.saldo == 90.0

    # 4. Verificación de Historiales
    print("\n--- Historial de Alicia ---")
    for mov in c1.obtener_historial():
        print(f"  [Alicia] {mov}")

    print("\n--- Historial de Bernat ---")
    for mov in c2.obtener_historial():
        print(f"  [Bernat] {mov}")

    # 5. Comprobación de Casos Límite y Excepciones
    print("\n" + "=" * 65)
    print("PRUEBAS DE ROBUSTEZ Y CASOS LÍMITE")
    print("=" * 65)

    # a) Cantidad negativa o cero en ingreso
    try:
        c1.ingresar(-10)
        raise AssertionError("Fallo: Debería rechazar ingreso negativo.")
    except ValueError as e:
        print(f"[OK] Rechazado ingreso negativo: {e}")

    try:
        c1.ingresar(0)
        raise AssertionError("Fallo: Debería rechazar ingreso cero.")
    except ValueError as e:
        print(f"[OK] Rechazado ingreso de cero: {e}")

    # b) Retirada superior al saldo disponible
    try:
        c1.retirar(500.0)
        raise AssertionError("Fallo: Debería impedir retirada superior al saldo.")
    except ValueError as e:
        print(f"[OK] Rechazada retirada con saldo insuficiente: {e}")

    # c) Transferencia hacia la misma cuenta
    try:
        c1.transferir(c1, 10.0)
        raise AssertionError("Fallo: Debería impedir transferencia a la misma cuenta.")
    except ValueError as e:
        print(f"[OK] Rechazada transferencia a uno mismo: {e}")

    # d) Transferencia sin fondos suficientes
    try:
        c1.transferir(c2, 1000.0)
        raise AssertionError("Fallo: Debería abortar transferencia sin fondos.")
    except ValueError as e:
        print(f"[OK] Rechazada transferencia por falta de fondos: {e}")

    # 6. Prueba explícita de inmutabilidad del historial expuesto (Aliasing bug)
    print("\n--- Prueba de Inmutabilidad del Historial ---")
    historial_alicia = c1.obtener_historial()
    print(f"Tipo retornado por obtener_historial: {type(historial_alicia).__name__}")
    
    try:
        historial_alicia.append("MOVIMIENTO FRAUDULENTO")  # type: ignore[attr-defined]
    except AttributeError:
        print("[OK] Inmutabilidad garantizada: El historial externo es inmutable (tuple) y no permite append().")

    assert len(c1.obtener_historial()) == 4, "El historial interno original no debe haber variado."
    print("\nTodas las pruebas del Ejercicio 4 finalizaron exitosamente.")
