"""
Ejercicio 3: Figuras sin modificar la función (Figures sense modificar la funció).
Módulo: MF0227_3 - Programación orientada a objetos (UF2404).

Este módulo implementa una jerarquía polimórfica de figuras geométricas utilizando:
1. Una clase base abstracta `Figura` con interfaz obligatoria (`nombre`, `area`, `perimetro`).
2. Clases concretas (`Rectangulo`, `Circulo`, `TrianguloRectangulo`).
3. Especialización sin duplicación de código (`Cuadrado` heredando de `Rectangulo`).
4. Polimorfismo y Principio Abierto/Cerrado (OCP) consumido por la función inmutable `imprimir_informe`.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import math
from typing import Sequence, Union

# Tipo para valores numéricos reales válidos
Numero = Union[int, float]


def _validar_dimension(valor: Numero, nombre_campo: str) -> float:
    """Valida que un valor numérico sea un número real estrictamente positivo (> 0).

    Args:
        valor: Valor a comprobar.
        nombre_campo: Nombre del atributo para mensajes de error.

    Returns:
        float: El valor validado y convertido a float.

    Raises:
        TypeError: Si el valor no es int o float (o si es bool).
        ValueError: Si el valor es menor o igual a cero.
    """
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError(f"El valor de '{nombre_campo}' debe ser numérico (int o float), recibido: {type(valor).__name__}")
    if valor <= 0:
        raise ValueError(f"El valor de '{nombre_campo}' debe ser estrictamente positivo (> 0), recibido: {valor}")
    return float(valor)


class Figura(ABC):
    """Clase base abstracta que define la interfaz común para todas las figuras geométricas."""

    @abstractmethod
    def nombre(self) -> str:
        """Devuelve el nombre representativo de la figura."""
        pass

    @abstractmethod
    def area(self) -> float:
        """Calcula y retorna el área de la figura geométrica."""
        pass

    @abstractmethod
    def perimetro(self) -> float:
        """Calcula y retorna el perímetro de la figura geométrica."""
        pass

    def __str__(self) -> str:
        return f"{self.nombre()} [Área={self.area():.2f}, Perímetro={self.perimetro():.2f}]"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} area={self.area():.2f} perimetro={self.perimetro():.2f}>"


class Rectangulo(Figura):
    """Representa un rectángulo definido por su base y su altura."""

    def __init__(self, base: Numero, altura: Numero) -> None:
        self._base: float = _validar_dimension(base, "base")
        self._altura: float = _validar_dimension(altura, "altura")

    @property
    def base(self) -> float:
        return self._base

    @property
    def altura(self) -> float:
        return self._altura

    def nombre(self) -> str:
        return "Rectángulo"

    def area(self) -> float:
        return self._base * self._altura

    def perimetro(self) -> float:
        return 2 * (self._base + self._altura)


class Circulo(Figura):
    """Representa un círculo definido por su radio."""

    def __init__(self, radio: Numero) -> None:
        self._radio: float = _validar_dimension(radio, "radio")

    @property
    def radio(self) -> float:
        return self._radio

    def nombre(self) -> str:
        return "Círculo"

    def area(self) -> float:
        return math.pi * (self._radio ** 2)

    def perimetro(self) -> float:
        return 2 * math.pi * self._radio


class TrianguloRectangulo(Figura):
    """Representa un triángulo rectángulo definido por sus dos catetos (base y altura)."""

    def __init__(self, base: Numero, altura: Numero) -> None:
        self._base: float = _validar_dimension(base, "base")
        self._altura: float = _validar_dimension(altura, "altura")

    @property
    def base(self) -> float:
        return self._base

    @property
    def altura(self) -> float:
        return self._altura

    def nombre(self) -> str:
        return "Triángulo Rectángulo"

    def area(self) -> float:
        return (self._base * self._altura) / 2.0

    def perimetro(self) -> float:
        # La hipotenusa se calcula de forma exacta con math.hypot
        hipotenusa = math.hypot(self._base, self._altura)
        return self._base + self._altura + hipotenusa


class Cuadrado(Rectangulo):
    """Representa un cuadrado como un caso especial de rectángulo con base == altura.

    Reutiliza el 100% de la lógica de cálculo de Rectángulo mediante super().__init__(lado, lado),
    evitando duplicación de código de área y perímetro.
    """

    def __init__(self, lado: Numero) -> None:
        # Reutiliza el constructor del padre pasando lado como base y altura
        super().__init__(lado, lado)

    @property
    def lado(self) -> float:
        return self._base

    def nombre(self) -> str:
        return "Cuadrado"


# Alias en catalán según requisitos del PDF
Rectangle = Rectangulo
Cercle = Circulo
TriangleRectangle = TrianguloRectangulo
Quadrat = Cuadrado


# =====================================================================
# FUNCIÓN PROPORCIONADA EN EL ENUNCIADO (NO MODIFICAR)
# =====================================================================
def imprimir_informe(figuras: Sequence[Figura]) -> None:
    """Imprime un informe polimórfico con el nombre, área y perímetro de cada figura."""
    for figura in figuras:
        print(
            figura.nombre(),
            round(figura.area(), 2),
            round(figura.perimetro(), 2)
        )


if __name__ == "__main__":
    print("=" * 65)
    print("EJECUCIÓN DEL CASO OFICIAL CON imprimir_informe(figuras)")
    print("=" * 65)

    # Creación de la colección polimórfica de figuras
    figuras_examen: list[Figura] = [
        Rectangulo(base=10, altura=5),
        Circulo(radio=3),
        TrianguloRectangulo(base=4, altura=3),
        Cuadrado(lado=4)
    ]

    # Ejecución de la función requerida
    imprimir_informe(figuras_examen)

    # Verificaciones y aserciones automatizadas
    print("\n" + "=" * 65)
    print("VERIFICACIONES Y PRUEBAS AUTOMATIZADAS")
    print("=" * 65)

    r = figuras_examen[0]
    c = figuras_examen[1]
    t = figuras_examen[2]
    q = figuras_examen[3]

    # Rectángulo: Área = 50, Perímetro = 30
    assert r.area() == 50.0, f"Error en área Rectángulo: {r.area()}"
    assert r.perimetro() == 30.0, f"Error en perímetro Rectángulo: {r.perimetro()}"

    # Círculo: Área = pi * 9 (~28.27), Perímetro = 2 * pi * 3 (~18.85)
    assert round(c.area(), 2) == 28.27, f"Error en área Círculo: {c.area()}"
    assert round(c.perimetro(), 2) == 18.85, f"Error en perímetro Círculo: {c.perimetro()}"

    # Triángulo Rectángulo (3, 4, hip=5): Área = 6.0, Perímetro = 12.0
    assert t.area() == 6.0, f"Error en área Triángulo: {t.area()}"
    assert t.perimetro() == 12.0, f"Error en perímetro Triángulo: {t.perimetro()}"

    # Cuadrado (lado=4): Área = 16.0, Perímetro = 16.0 (Heredado de Rectangulo)
    assert q.area() == 16.0, f"Error en área Cuadrado: {q.area()}"
    assert q.perimetro() == 16.0, f"Error en perímetro Cuadrado: {q.perimetro()}"
    assert isinstance(q, Rectangulo), "Cuadrado debe ser instancia de Rectangulo"
    assert isinstance(q, Figura), "Cuadrado debe ser instancia de Figura"

    print("[OK] Cálculos geométricos verificados con éxito.")

    # Comprobación de que no se puede instanciar la clase base abstracta
    try:
        Figura()  # type: ignore[abstract]
        raise AssertionError("Fallo: La clase abstracta Figura no debería poder instanciarse.")
    except TypeError:
        print("[OK] Verificado: Figura(ABC) no permite instanciación directa (Contrato abstracto seguro).")

    # Comprobación de validación de dimensiones inválidas
    try:
        Rectangulo(-5, 10)
        raise AssertionError("Fallo: Debería rechazar dimensiones negativas.")
    except ValueError:
        print("[OK] Verificado: Rechaza dimensiones <= 0 correctamente.")

    print("\nTodas las pruebas del Ejercicio 3 finalizaron exitosamente.")
