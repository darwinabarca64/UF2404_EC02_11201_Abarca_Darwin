"""
Ejercicio 6: Sistema de inventario (Sistema d'inventari).
Módulo: MF0227_3 - Programación orientada a objetos (UF2404).

Este módulo implementa las clases `Producto` e `Inventario` (y sus alias `Producte` e `Inventari`) garantizando:
1. Encapsulación y validación de atributos comerciales (precio > 0, stock >= 0).
2. Unicidad de códigos de producto mediante diccionario hash map O(1).
3. Consistencia transaccional en ventas y reposiciones.
4. Cálculo contable del valor monetario total del inventario.
5. Blindaje de la colección interna de productos para evitar modificaciones externas no autorizadas.
"""

from __future__ import annotations
from typing import Dict, Tuple, Union

Numero = Union[int, float]


def _validar_texto(texto: str, nombre_campo: str) -> str:
    """Valida que una cadena de texto no sea nula ni contenga únicamente espacios en blanco."""
    if not isinstance(texto, str):
        raise TypeError(f"El campo '{nombre_campo}' debe ser de tipo str, recibido: {type(texto).__name__}")
    limpio = texto.strip()
    if not limpio:
        raise ValueError(f"El campo '{nombre_campo}' no puede estar vacío.")
    return limpio


def _validar_entero_positivo(valor: int, nombre_campo: str, permitir_cero: bool = False) -> int:
    """Valida que un número sea un entero mayor que cero (o mayor o igual a cero si permitir_cero=True)."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(f"El campo '{nombre_campo}' debe ser un número entero (int), recibido: {type(valor).__name__}")
    if permitir_cero:
        if valor < 0:
            raise ValueError(f"El campo '{nombre_campo}' no puede ser negativo, recibido: {valor}")
    else:
        if valor <= 0:
            raise ValueError(f"El campo '{nombre_campo}' debe ser estrictamente positivo (> 0), recibido: {valor}")
    return valor


class Producto:
    """Representa un artículo comercial en el catálogo de la tienda.

    Attributes:
        codigo (str): Identificador único del producto.
        nombre (str): Denominación del producto.
        precio (float): Precio unitario (> 0).
        stock (int): Unidades disponibles en almacén (>= 0).
    """

    def __init__(self, codigo: str, nombre: str, precio: Numero, stock: int = 0) -> None:
        self._codigo: str = _validar_texto(codigo, "codigo")
        self._nombre: str = _validar_texto(nombre, "nombre")
        
        if isinstance(precio, bool) or not isinstance(precio, (int, float)):
            raise TypeError(f"El precio debe ser numérico, recibido: {type(precio).__name__}")
        if precio <= 0:
            raise ValueError(f"El precio debe ser estrictamente positivo (> 0), recibido: {precio}")
        self._precio: float = float(precio)

        self._stock: int = _validar_entero_positivo(stock, "stock", permitir_cero=True)

    @property
    def codigo(self) -> str:
        """Identificador único del producto."""
        return self._codigo

    # Alias en catalán
    codi = codigo

    @property
    def nombre(self) -> str:
        """Nombre descriptivo del producto."""
        return self._nombre

    # Alias en catalán
    nom = nombre

    @property
    def precio(self) -> float:
        """Precio unitario del producto."""
        return self._precio

    # Alias en catalán
    preu = precio

    @precio.setter
    def precio(self, nuevo_precio: Numero) -> None:
        """Actualiza el precio garantizando que sea positivo."""
        if isinstance(nuevo_precio, bool) or not isinstance(nuevo_precio, (int, float)):
            raise TypeError(f"El precio debe ser numérico, recibido: {type(nuevo_precio).__name__}")
        if nuevo_precio <= 0:
            raise ValueError(f"El precio debe ser mayor que cero, recibido: {nuevo_precio}")
        self._precio = float(nuevo_precio)

    @property
    def stock(self) -> int:
        """Cantidad de unidades disponibles."""
        return self._stock

    def decrementar_stock(self, cantidad: int) -> None:
        """Reduce el stock en la cantidad especificada."""
        cant = _validar_entero_positivo(cantidad, "cantidad")
        if cant > self._stock:
            raise ValueError(
                f"Stock insuficiente para el producto '{self._nombre}' (Código: {self._codigo}). "
                f"Disponible: {self._stock}, Solicitado: {cant}"
            )
        self._stock -= cant

    def incrementar_stock(self, cantidad: int) -> None:
        """Aumenta el stock en la cantidad especificada."""
        cant = _validar_entero_positivo(cantidad, "cantidad")
        self._stock += cant

    def valor_stock(self) -> float:
        """Retorna el valor económico total de este producto (precio * stock)."""
        return self._precio * self._stock

    def __str__(self) -> str:
        return f"Producto[{self._codigo}] '{self._nombre}' - {self._precio:.2f}€ (Stock: {self._stock})"

    def __repr__(self) -> str:
        return f"Producto(codigo={self._codigo!r}, nombre={self._nombre!r}, precio={self._precio!r}, stock={self._stock!r})"


class Inventario:
    """Gestiona el conjunto de productos del almacén y sus operaciones comerciales."""

    def __init__(self) -> None:
        # Estructura interna protegida: Diccionario con clave 'codigo' para búsquedas O(1)
        self._productos: Dict[str, Producto] = {}

    @property
    def productos(self) -> Tuple[Producto, ...]:
        """Retorna una vista inmutable (tupla) de los productos del inventario.

        Protege la estructura interna contra modificaciones externas directas.
        """
        return tuple(self._productos.values())

    def agregar_producto(self, producto: Producto) -> None:
        """Añade un nuevo producto al catálogo verificando que no exista duplicidad de código.

        Args:
            producto: Instancia de Producto a incorporar.

        Raises:
            TypeError: Si el objeto recibido no es una instancia de Producto.
            ValueError: Si ya existe un producto con el mismo código.
        """
        if not isinstance(producto, Producto):
            raise TypeError(f"El elemento a añadir debe ser una instancia de Producto, recibido: {type(producto).__name__}")

        if producto.codigo in self._productos:
            raise ValueError(
                f"No se puede agregar: Ya existe un producto con el código '{producto.codigo}' "
                f"('{self._productos[producto.codigo].nombre}')."
            )

        self._productos[producto.codigo] = producto

    # Alias en catalán
    afegir_producte = agregar_producto

    def eliminar_producto(self, codigo: str) -> None:
        """Elimina un producto del inventario a partir de su código.

        Args:
            codigo: Código del producto a eliminar.

        Raises:
            ValueError: Si el código no existe en el catálogo.
        """
        cod = _validar_texto(codigo, "codigo")
        if cod not in self._productos:
            raise ValueError(f"No se puede eliminar: No existe ningún producto con el código '{cod}'.")
        del self._productos[cod]

    # Alias en catalán
    eliminar_producte = eliminar_producto

    def buscar(self, codigo: str) -> Producto:
        """Busca y retorna un producto por su código identificador.

        Args:
            codigo: Código a localizar.

        Returns:
            Producto: Instancia del producto encontrado.

        Raises:
            ValueError: Si el producto no se encuentra.
        """
        cod = _validar_texto(codigo, "codigo")
        if cod not in self._productos:
            raise ValueError(f"Búsqueda fallida: No existe ningún producto con el código '{cod}'.")
        return self._productos[cod]

    def vender(self, codigo: str, cantidad: int) -> None:
        """Realiza una venta reduciendo el stock disponible del producto correspondiente.

        Args:
            codigo: Identificador del producto a vender.
            cantidad: Número entero positivo de unidades a vender.

        Raises:
            ValueError: Si el código no existe o no hay suficiente stock.
        """
        producto = self.buscar(codigo)
        producto.decrementar_stock(cantidad)

    # Alias en catalán
    vendre = vender

    def reponer(self, codigo: str, cantidad: int) -> None:
        """Añade existencias al stock de un producto existente.

        Args:
            codigo: Identificador del producto a reponer.
            cantidad: Número entero positivo de unidades a ingresar.

        Raises:
            ValueError: Si el código no existe o la cantidad es inválida.
        """
        producto = self.buscar(codigo)
        producto.incrementar_stock(cantidad)

    # Alias en catalán
    reposar = reponer

    def valor_total(self) -> float:
        """Calcula el valor monetario total de todo el stock almacenado en el inventario.

        Returns:
            float: Suma de (precio * stock) de todos los productos.
        """
        return sum(p.valor_stock() for p in self._productos.values())

    def __len__(self) -> int:
        """Retorna el número de productos distintos en catálogo."""
        return len(self._productos)

    def __str__(self) -> str:
        return f"Inventario({len(self)} productos registrados, Valor Total: {self.valor_total():.2f}€)"

    def __repr__(self) -> str:
        return f"Inventario(items={len(self._productos)}, valor_total={self.valor_total():.2f})"


# Alias bilingües según PDF
Producte = Producto
Inventari = Inventario


if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN COMPLETA - EJERCICIO 6: SISTEMA DE INVENTARIO")
    print("=" * 65)

    inv = Inventario()

    # 1. Creación e incorporación de productos
    p1 = Producto("P001", "Teclado Mecánico", precio=80.0, stock=10)
    p2 = Producto("P002", "Ratón Gaming", precio=40.0, stock=20)
    p3 = Producto("P003", "Monitor 27 pulgadas", precio=250.0, stock=4)

    inv.agregar_producto(p1)
    inv.agregar_producto(p2)
    inv.agregar_producto(p3)

    print(f"Estado inicial del inventario: {inv}")
    # Valor esperado: (80*10) + (40*20) + (250*4) = 800 + 800 + 1000 = 2600.0€
    print(f"Valor monetario total: {inv.valor_total():.2f}€")
    assert inv.valor_total() == 2600.0, f"Error en valor_total: {inv.valor_total()}"
    assert len(inv) == 3
    print("[OK] Incorporación y cálculo de valor total verificados.")

    # 2. Control de duplicados
    print("\n--- Intento de duplicidad de código ---")
    p_duplicado = Producto("P001", "Teclado Alternativo", precio=90.0, stock=5)
    try:
        inv.agregar_producto(p_duplicado)
        raise AssertionError("Fallo: Debería haber impedido agregar un producto con código ya existente.")
    except ValueError as e:
        print(f"[OK] Capturada duplicidad de código correctamente: {e}")

    # 3. Flujo de Venta y Reposición
    print("\n--- Venta y Reposición ---")
    # Venta de 3 teclados (quedan 7)
    inv.vender("P001", 3)
    assert inv.buscar("P001").stock == 7
    print(f"Venta de 3 uds de P001 realizada. Stock resultante: {inv.buscar('P001').stock}")

    # Reposición de 5 ratones (de 20 a 25)
    inv.reponer("P002", 5)
    assert inv.buscar("P002").stock == 25
    print(f"Reposición de 5 uds de P002 realizada. Stock resultante: {inv.buscar('P002').stock}")

    # Nuevo valor total: (80*7) + (40*25) + (250*4) = 560 + 1000 + 1000 = 2560.0€
    print(f"Nuevo valor total del inventario: {inv.valor_total():.2f}€")
    assert inv.valor_total() == 2560.0
    print("[OK] Venta, reposición y recálculo de valor total validados.")

    # 4. Caso límite: Vender más del stock disponible
    print("\n--- Intento de sobrepasar el stock disponible ---")
    try:
        inv.vender("P003", 10)  # Solo hay 4
        raise AssertionError("Fallo: Debería haber impedido vender más de las unidades en stock.")
    except ValueError as e:
        print(f"[OK] Capturado intento de sobreventa correctamente: {e}")

    # 5. Eliminación de productos
    print("\n--- Eliminación de Producto ---")
    inv.eliminar_producto("P003")
    assert len(inv) == 2
    try:
        inv.buscar("P003")
        raise AssertionError("Fallo: El producto P003 debería haber sido eliminado.")
    except ValueError as e:
        print(f"[OK] Confirmada eliminación: {e}")

    # 6. Prueba de Encapsulamiento y Protección de Datos
    print("\n--- Prueba de Inmutabilidad de la Colección Expuesta ---")
    coleccion_externa = inv.productos
    print(f"Tipo retornado por propiedad 'productos': {type(coleccion_externa).__name__}")
    
    try:
        coleccion_externa.append(p3)  # type: ignore[attr-defined]
    except AttributeError:
        print("[OK] Inmutabilidad garantizada: La vista de productos es una tupla y no permite mutación directa.")

    assert len(inv) == 2, "El catálogo interno no debe haberse modificado."
    print("\nTodas las pruebas del Ejercicio 6 pasaron satisfactoriamente.")
