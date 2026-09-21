"""
Ejercicio 8: Código desconocido (Codi desconegut).
Módulo: MF0227_3 - Programación orientada a objetos (UF2404).

Este módulo analiza en profundidad:
1. El Algoritmo de Linealización C3 (C3 Linearization) en herencia múltiple.
2. El Orden de Resolución de Métodos (MRO - Method Resolution Order).
3. El funcionamiento interno y dinámico de `super()` en llamadas cooperativas.
4. Comparativa de resultados entre D(B, C) y D_Invertida(C, B).
"""

from __future__ import annotations
from typing import Type


class A:
    """Clase base raíz de la jerarquía de herencia en diamante."""

    def metodo(self) -> str:
        return "A"


class B(A):
    """Subclase B que extiende a A e invoca a super()."""

    def metodo(self) -> str:
        return "B" + super().metodo()


class C(A):
    """Subclase C que extiende a A e invoca a super()."""

    def metodo(self) -> str:
        return "C" + super().metodo()


class D(B, C):
    """Subclase D con herencia múltiple en orden (B, C)."""

    def metodo(self) -> str:
        return "D" + super().metodo()


class D_Invertida(C, B):
    """Subclase D con orden de herencia invertido (C, B) para la Cuestión 4."""

    def metodo(self) -> str:
        return "D" + super().metodo()


def formatear_mro(cls: Type[object]) -> str:
    """Retorna una representación formateada y visual del MRO de una clase."""
    return " -> ".join([c.__name__ for c in cls.__mro__])


def trazar_resolucion() -> None:
    """Muestra paso a paso cómo se ejecutan las llamadas encadenadas con super()."""
    print("=" * 70)
    print("1. EJECUCIÓN ORIGINAL: class D(B, C)")
    print("=" * 70)

    obj = D()
    resultado = obj.metodo()
    mro_lista = D.mro()

    print(f"Salida de obj.metodo() : '{resultado}'")
    print(f"Salida de D.mro()      : {mro_lista}")
    print(f"Cadena MRO visual      : {formatear_mro(D)}")

    print("\n--- Desglose de la pila de llamadas (Call Stack) ---")
    print("  1. Se invoca 'obj.metodo()' sobre una instancia de D.")
    print("  2. 'D.metodo' retorna 'D' + super().metodo().")
    print("     -> Según el MRO [D, B, C, A, object], la clase siguiente a D es B.")
    print("  3. 'B.metodo' retorna 'B' + super().metodo().")
    print("     -> ¡CLAVE!: Para la instancia obj (de tipo D), la clase siguiente a B en el MRO es C (¡no A!).")
    print("  4. 'C.metodo' retorna 'C' + super().metodo().")
    print("     -> La clase siguiente a C en el MRO es A.")
    print("  5. 'A.metodo' retorna 'A' (caso base terminal, no tiene super).")
    print("  6. La concatenación se resuelve: 'D' + ('B' + ('C' + 'A')) ==> 'DBCA'")

    assert resultado == "DBCA", f"Error: Se esperaba 'DBCA' pero se obtuvo '{resultado}'"

    print("\n" + "=" * 70)
    print("2. ORDEN DE HERENCIA INVERTIDO: class D_Invertida(C, B)")
    print("=" * 70)

    obj_inv = D_Invertida()
    resultado_inv = obj_inv.metodo()
    mro_inv_lista = D_Invertida.mro()

    print(f"Salida de obj_inv.metodo() : '{resultado_inv}'")
    print(f"Salida de D_Invertida.mro(): {mro_inv_lista}")
    print(f"Cadena MRO visual          : {formatear_mro(D_Invertida)}")

    print("\n--- Desglose del nuevo MRO ---")
    print("  Al declarar 'class D_Invertida(C, B)', C tiene precedencia sobre B.")
    print("  MRO resultante: [D_Invertida, C, B, A, object]")
    print("  Secuencia: D -> C -> B -> A ==> 'DCBA'")

    assert resultado_inv == "DCBA", f"Error: Se esperaba 'DCBA' pero se obtuvo '{resultado_inv}'"

    print("\n[OK] Todas las comprobaciones de introspección y MRO pasaron con éxito.")


if __name__ == "__main__":
    trazar_resolucion()
