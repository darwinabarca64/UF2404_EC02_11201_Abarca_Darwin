"""
Ejercicio 10: Sistema extensible de pedidos (Sistema extensible de comandes).
Módulo: MF0227_3 - Programación orientada a objetos (UF2404).

Este módulo implementa la arquitectura extensible para gestión de pedidos mediante:
1. Clase base abstracta `Producto` con contrato polimórfico `calcular_precio_final()`.
2. Subclases de negocio: `ProductoFisico`, `ProductoDigital`, `Suscripcion`.
3. Extensión OCP: `ProductoDescuento` integrada sin tocar la clase `Pedido`.
4. Clase `Pedido` con total desacoplamiento (sin 'if type(...)') y unicidad de ID.
5. Preparación para cambios sorpresa en directo de la Segunda Parte del examen.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Union

Numero = Union[int, float]


def _validar_cadena_no_vacia(valor: str, nombre_campo: str) -> str:
    """Valida que una cadena no sea nula ni contenga únicamente espacios."""
    if not isinstance(valor, str):
        raise TypeError(f"El campo '{nombre_campo}' debe ser de tipo str, recibido: {type(valor).__name__}")
    limpio = valor.strip()
    if not limpio:
        raise ValueError(f"El campo '{nombre_campo}' no puede estar vacío.")
    return limpio


def _validar_numero_positivo(valor: Numero, nombre_campo: str) -> float:
    """Valida que un valor sea numérico y estrictamente mayor que cero (> 0)."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError(f"El campo '{nombre_campo}' debe ser numérico, recibido: {type(valor).__name__}")
    if valor <= 0:
        raise ValueError(f"El campo '{nombre_campo}' debe ser estrictamente positivo (> 0), recibido: {valor}")
    return float(valor)


class Producto(ABC):
    """Clase base abstracta que define la estructura y contrato común para todos los productos."""

    def __init__(self, id_producto: str, nombre: str, precio_base: Numero) -> None:
        self._id: str = _validar_cadena_no_vacia(id_producto, "id_producto")
        self._nombre: str = _validar_cadena_no_vacia(nombre, "nombre")
        self._precio_base: float = _validar_numero_positivo(precio_base, "precio_base")

    @property
    def id(self) -> str:
        """Identificador único del producto."""
        return self._id

    # Alias en catalán
    codi = id

    @property
    def nombre(self) -> str:
        """Nombre o descripción del producto."""
        return self._nombre

    # Alias en catalán
    nom = nombre

    @property
    def precio_base(self) -> float:
        """Precio unitario base antes de reglas específicas."""
        return self._precio_base

    # Alias en catalán
    preu_base = precio_base

    @abstractmethod
    def calcular_precio_final(self) -> float:
        """Calcula polimórficamente el precio final facturable del producto."""
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self._id}] '{self._nombre}' -> {self.calcular_precio_final():.2f}€"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self._id!r} base={self._precio_base:.2f} final={self.calcular_precio_final():.2f}>"


class ProductoFisico(Producto):
    """Producto tangible que requiere logística de envío."""

    def __init__(self, id_producto: str, nombre: str, precio_base: Numero, coste_envio: Numero) -> None:
        super().__init__(id_producto, nombre, precio_base)
        self._coste_envio: float = _validar_numero_positivo(coste_envio, "coste_envio")

    @property
    def coste_envio(self) -> float:
        """Coste de transporte y envío."""
        return self._coste_envio

    # Alias en catalán
    cost_enviament = coste_envio

    def calcular_precio_final(self) -> float:
        """Precio final: precio base + coste de envío."""
        return self._precio_base + self._coste_envio


class ProductoDigital(Producto):
    """Producto descargable o intangible sin costes de envío."""

    def __init__(self, id_producto: str, nombre: str, precio_base: Numero) -> None:
        super().__init__(id_producto, nombre, precio_base)

    def calcular_precio_final(self) -> float:
        """Precio final: precio base directo."""
        return self._precio_base


class Suscripcion(Producto):
    """Servicio recurrente facturado por período de meses."""

    def __init__(self, id_producto: str, nombre: str, precio_base: Numero, meses: int) -> None:
        super().__init__(id_producto, nombre, precio_base)
        if isinstance(meses, bool) or not isinstance(meses, int):
            raise TypeError(f"El número de meses debe ser un entero (int), recibido: {type(meses).__name__}")
        if meses <= 0:
            raise ValueError(f"El número de meses debe ser mayor que cero, recibido: {meses}")
        self._meses: int = meses

    @property
    def meses(self) -> int:
        """Duración en meses de la suscripción."""
        return self._meses

    # Alias en catalán
    mesos = meses

    def calcular_precio_final(self) -> float:
        """Precio final: precio base mensual * número de meses."""
        return self._precio_base * self._meses


class ProductoDescuento(Producto):
    """Producto con descuento porcentual directo incorporado mediante extensión."""

    def __init__(self, id_producto: str, nombre: str, precio_base: Numero, porcentaje_descuento: Numero) -> None:
        super().__init__(id_producto, nombre, precio_base)
        if isinstance(porcentaje_descuento, bool) or not isinstance(porcentaje_descuento, (int, float)):
            raise TypeError(f"El descuento debe ser numérico, recibido: {type(porcentaje_descuento).__name__}")
        if not (0 <= porcentaje_descuento <= 100):
            raise ValueError(f"El porcentaje de descuento debe estar entre 0 y 100, recibido: {porcentaje_descuento}%")
        self._porcentaje_descuento: float = float(porcentaje_descuento)

    @property
    def porcentaje_descuento(self) -> float:
        """Porcentaje de rebaja aplicado."""
        return self._porcentaje_descuento

    def calcular_precio_final(self) -> float:
        """Precio final: precio base * (1 - descuento / 100)."""
        factor = 1.0 - (self._porcentaje_descuento / 100.0)
        return self._precio_base * factor


# Alias en catalán según requisitos del PDF
ProducteFisic = ProductoFisico
ProducteDigital = ProductoDigital
Subscripcio = Suscripcion
ProducteDescompte = ProductoDescuento


class Pedido:
    """Gestiona una orden de compra con múltiples productos polimórficos.

    Cumple con:
    1. Unicidad de identificadores de producto en el pedido.
    2. Cálculo de total polimórfico sin 'if type(...)'.
    3. Extensibilidad ante nuevas clases de producto sin modificar esta clase.
    """

    def __init__(self) -> None:
        # Estructura indexada por id para garantizar unicidad y acceso O(1)
        self._productos: Dict[str, Producto] = {}

    @property
    def productos(self) -> Tuple[Producto, ...]:
        """Retorna una vista inmutable (tupla) de los productos del pedido."""
        return tuple(self._productos.values())

    def agregar(self, producto: Producto) -> None:
        """Añade un producto al pedido verificando la unicidad de su ID.

        Args:
            producto: Instancia de cualquier subclase de Producto.

        Raises:
            TypeError: Si el objeto recibido no es una subclase de Producto.
            ValueError: Si ya existe un producto con el mismo ID en el pedido.
        """
        if not isinstance(producto, Producto):
            raise TypeError(f"Solo pueden agregarse objetos derivados de Producto, recibido: {type(producto).__name__}")

        if producto.id in self._productos:
            raise ValueError(
                f"No se puede agregar: Ya existe un producto con el ID '{producto.id}' "
                f"('{self._productos[producto.id].nombre}') en el pedido."
            )

        self._productos[producto.id] = producto

    # Alias en catalán
    afegir = agregar

    def eliminar(self, id_producto: str) -> None:
        """Elimina un producto del pedido por su identificador.

        Args:
            id_producto: Identificador del producto a retirar.

        Raises:
            ValueError: Si el ID no figura en el pedido.
        """
        id_limpio = _validar_cadena_no_vacia(id_producto, "id_producto")
        if id_limpio not in self._productos:
            raise ValueError(f"No se puede eliminar: No existe ningún producto con el ID '{id_limpio}' en este pedido.")
        del self._productos[id_limpio]

    def calcular_total(self) -> float:
        """Calcula el importe total sumando los precios finales polimórficamente.

        ESTRICTAMENTE LIBRE DE 'if type(...)', 'if isinstance(...)'.

        Returns:
            float: Importe total del pedido.
        """
        return sum(p.calcular_precio_final() for p in self._productos.values())

    def __len__(self) -> int:
        """Número de productos en el pedido."""
        return len(self._productos)

    def __str__(self) -> str:
        """Factura detallada del pedido."""
        lineas = [
            f"==================================================",
            f"RESUMEN DE PEDIDO ({len(self)} artículos)",
            f"=================================================="
        ]
        if not self._productos:
            lineas.append("  (El pedido está vacío)")
        else:
            for p in self._productos.values():
                lineas.append(f"  - [{p.id}] {p.nombre:<26} -> {p.calcular_precio_final():>8.2f}€")
        lineas.append("--------------------------------------------------")
        lineas.append(f"TOTAL FACTURABLE:                     {self.calcular_total():>8.2f}€")
        lineas.append("==================================================")
        return "\n".join(lineas)

    def __repr__(self) -> str:
        return f"Pedido(items={len(self._productos)}, total={self.calcular_total():.2f})"


# Alias en catalán según PDF
Comanda = Pedido


if __name__ == "__main__":
    print("=" * 70)
    print("DEMOSTRACIÓN COMPLETA - EJERCICIO 10: SISTEMA EXTENSIBLE DE PEDIDOS")
    print("=" * 70)

    # 1. Creación del pedido inicial con los 3 tipos de productos
    pedido = Pedido()

    fisico = ProductoFisico("F001", "Libro de Python", precio_base=30.0, coste_envio=5.0)       # 35.0€
    digital = ProductoDigital("D001", "E-book Arquitectura POO", precio_base=20.0)             # 20.0€
    suscripcion = Suscripcion("S001", "Plan Mensual Cloud", precio_base=15.0, meses=6)         # 90.0€

    pedido.agregar(fisico)
    pedido.agregar(digital)
    pedido.agregar(suscripcion)

    print("\n--- Factura Inicial ---")
    print(pedido)

    # Total esperado: 35.0 + 20.0 + 90.0 = 145.0€
    total_inicial = pedido.calcular_total()
    print(f"Total calculado: {total_inicial:.2f}€")
    assert round(total_inicial, 2) == 145.0, f"Error en total inicial: {total_inicial}"
    print("[OK] Productos iniciales y cálculo polimórfico validados.")

    # 2. Control de ID duplicado
    print("\n--- Intento de ID duplicado ---")
    prod_duplicado = ProductoDigital("F001", "Curso Express", precio_base=50.0)
    try:
        pedido.agregar(prod_duplicado)
        raise AssertionError("Fallo: Debería haber impedido registrar un producto con ID repetido.")
    except ValueError as e:
        print(f"[OK] Capturado ID duplicado correctamente: {e}")

    # 3. Demostración de OCP: Añadir ProductoDescuento sin modificar Pedido
    print("\n--- Extensión OCP: Añadir ProductoDescuento ---")
    # Precio base 100€ con 25% descuento = 75.0€
    descuento = ProductoDescuento("DESC01", "Pack Monitor Gaming", precio_base=100.0, porcentaje_descuento=25.0)
    pedido.agregar(descuento)

    print(pedido)
    # Nuevo total: 145.0 + 75.0 = 220.0€
    total_con_descuento = pedido.calcular_total()
    print(f"Nuevo total con descuento: {total_con_descuento:.2f}€")
    assert round(total_con_descuento, 2) == 220.0, f"Error con descuento: {total_con_descuento}"
    print("[OK] Extensión OCP de ProductoDescuento verificada sin modificar Pedido.")

    # 4. Eliminación de producto
    print("\n--- Eliminación de Producto ---")
    pedido.eliminar("D001")  # Quitamos el digital de 20€
    # Total esperado: 220.0 - 20.0 = 200.0€
    assert round(pedido.calcular_total(), 2) == 200.0
    print(f"Producto D001 eliminado. Total resultante: {pedido.calcular_total():.2f}€")
    print("[OK] Eliminación y recálculo completados.")

    # 5. SIMULACIÓN DE LA 'SEGUNDA PARTE' (Cambio sorpresa del profesor)
    print("\n" + "=" * 70)
    print("SIMULACIÓN DE LA SEGUNDA PARTE: NUEVO TIPO 'ProductoConIVA'")
    print("=" * 70)

    class ProductoConIVA(Producto):
        """Nueva clase sorpresa creada en directo en 5 líneas."""
        def __init__(self, id_producto: str, nombre: str, precio_base: Numero, tipo_iva: float = 21.0) -> None:
            super().__init__(id_producto, nombre, precio_base)
            self.tipo_iva = tipo_iva

        def calcular_precio_final(self) -> float:
            return self._precio_base * (1.0 + self.tipo_iva / 100.0)

    # Añadimos este nuevo tipo al pedido existente (base 100€ + 21% IVA = 121€)
    item_iva = ProductoConIVA("IVA01", "Licencia Software Empresarial", precio_base=100.0, tipo_iva=21.0)
    pedido.agregar(item_iva)

    print(f"Producto sorpresa agregado: {item_iva}")
    # Total esperado: 200.0 + 121.0 = 321.0€
    assert round(pedido.calcular_total(), 2) == 321.0
    print(f"Total tras cambio en directo: {pedido.calcular_total():.2f}€")
    print("[OK] Arquitectura validada para cambios imprevistos en directo.")

    print("\nTodas las pruebas del Ejercicio 10 concluyeron con máxima calificación.")
